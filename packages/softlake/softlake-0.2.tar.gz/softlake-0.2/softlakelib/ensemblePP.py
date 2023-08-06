import yaml
import copy
import numpy as np
from softlakelib import primaryProductionModel as primaryProduction

def calculate_models(yamlfile):
    """Calculate Primary Production with the SoftLake library and return a dict with models with names 
       [modelname]_[curvename] as keys

    Args:
        yamlfile (str): the filepath to the configuration file

    Raises:
        ValueError: if Climate series contain null data
    """

    # with open('/home/maxi/GIT/softlake/softlakelib/settings.yml') as f:
    with open(yamlfile) as f:
        settings = yaml.safe_load(f)

    model = primaryProduction.PP(
        period = settings['model']['period'],
        depth = settings['model']['depth'],
        z_res = settings['model']['z_res'],
        location = [
            settings['model']['location']['lat'],
            settings['model']['location']['lon']
        ]
    )

    # set observed profiles
    if settings['model']['verbose']:
        print(f'Setting observed profiles')
    if 'date_parser' in settings['model']['profile_obs']:
        model.set_profiles(
            csvfile=settings['model']['profile_obs']['csv'],
            date_parser=settings['model']['profile_obs']['date_parser']
        )
    else:
        model.set_profiles(
            csvfile=settings['model']['profile_obs']['csv']
        )

    # set climatic time serie
    if settings['model']['verbose']:
        print(f'Setting climatic time serie')
    if 'date_parser' in settings['model']['climatic_series']:
        model.set_climatic_series(
            csvfile=settings['model']['climatic_series']['csv'],
            date_parser=settings['model']['climatic_series']['date_parser']
        )
    else:
        model.set_climatic_series(
            csvfile=settings['model']['climatic_series']['csv']
        )

    # Check and eliminate profiles data with null values
    # --------------------------------------------------
    if model.check_nulls_in_profiles() > 0:
        model.drop_null_profile_rows()

    if model.check_nulls_in_climate() > 0:
        raise ValueError('Climate series contain null data')

    # Estimate the PAR (and optionally all the intermediate filtered irradiance and used parameters)
    # ----------------------------------------------------------------------------------------------
    #model.estimate_PAR(keep_only=['Ia','Iu','Iw','Ic','Io'])
    if settings['model']['verbose']:
        print(f'Estimating PAR')
    model.estimate_PAR()

    # Create grids interpolating profile columns
    # ---------------------------------------------
    if settings['model']['verbose']:
        print(f'Interpolating T & CHL profile columns')
    model.interpolate_profiles(columns=['T','CHL'], method='cubic', extrapolate=True)

    # Standardize Primary Production
    # --------------------------------
    if settings['model']['verbose']:
        print(f'Standardizing PP')
    model.standardizePP()
    model.profiles[['PP','PPn']]

    # Calculate a model for each curve
    models = {}
    for c, curve in settings['model']['curves'].items():
        if settings['model']['verbose']:
            print(f'Calculating {c} curve fitting')
            print('------------------------------')
        # create a copy of the model and set the specific curve
        # ------------------------------------------------
        mn = f"{settings['model']['name']}_{c}"
        models[mn] = copy.deepcopy(model)
        # set assigned weigth
        models[mn]._weigth = curve['weigth']
        models[mn].set_pi_curve(c)
        
        # Estimate best fit of P/I curve for profile data
        # ------------------------------------------------
        models[mn].estimate_params(
            r2_min = curve['r2_min'] if 'r2_min' in curve else None,
            showplots = curve['showplots'] if 'showplots' in curve else False,
            verbose = curve['verbose'] if 'verbose' in curve else False,
        )

        # Calculate light extintion slopes with line regression from profiles
        # --------------------------------------------------------------------
        models[mn].estimate_light_extintion_slope(keep_only=['slope'], showplots=False)
        
        # Interpolate parameters in time with defined methods
        # -----------------------------------------------------
        if settings['model']['verbose']:
            print(f'Interpolating fitted {c} parameters in time')
        models[mn].parameter_interpolate(parameter=[], method=curve['interpolation'])

        # Grid the P/I curves parameters (slope, iopt, pmax, beta)
        # ---------------------------------------------
        models[mn].grid_parameters()

        # Caluclate Eutrophic zone grid
        # ---------------------------------------------
        if settings['model']['verbose']:
            print(f'Calculating euthriphic zone grid')
        models[mn].grid['euf'] = -4.7 / models[mn].grid['slope']

        # calculate the irradiance (PAR, Iz) grids [io,iz]
        # ------------------------
        if settings['model']['verbose']:
            print(f'Calculating irradiance (PAR, Iz) grid')
        models[mn].grid_irradiance()

        # Estimated the standardized Primary Prodution (PPn) in time and depth
        # ---------------------------------------------------------------------
        if settings['model']['verbose']:
            print(f'Estimating standardized Primary Prodution (PPn) grid')
        models[mn].calculate_PPn()

        # Estimate the Primary Production in time and depth
        # ---------------------------------------------------
        if settings['model']['verbose']:
            print(f'Estimating de-standardized Primary Prodution (PP) grid')
        models[mn].destandardizePP()

        # Calculate the photic zone grid [fz] and PP in fz [PPfz]
        # ---------------------------------------------------
        if settings['model']['verbose']:
            print(f'Calculating Primary Prodution (PPfz) in photic zone')
        
        models[mn].calculate_photic_zone()

    return(models)

def ensamble(models, voxnames=['PP'], stats=['average','ptp']):
    """Combine models grids in 3d numpy arrays and calculate grid statistics

    Args:
        models (list): list of SoftLake models objects
        voxnames (list): list of grid name to process with stats
                        ['T', 'CHL', 'slope', 'euf', 'io', 'iz', 'PPn', 'PP', 'fz', 'PPfz']
        stats (list): list of stats to calculate (will result in [gridname]_[statname])
                      ['min','max','ptp','median','average','mean','std'] for more info on
                      statistics see:  https://numpy.org/doc/stable/reference/routines.statistics.html
                      n.b.: in 'average' single model weigth property is used
    """

    if len(models) == 0:
        raise ValueError('Models should not be null list')
    
    mn = list(models.keys())
    mgrids = list(models[mn[0]].grid.keys())
    # copy and empty the base model
    ens = copy.deepcopy(models[mn[0]])
    ens.grid = {}
    ens.parameters = None
    # populate voxels with common grids among models
    for g in mgrids:
        try:
            ens.voxel[g] = np.array([mm.grid[g] for n, mm in models.items()])
            ens._voxcolnames = [n for n, mm in models.items()]
            ens._voxweigths = [mm._weigth for n, mm in models.items()]
        except KeyError as e:
            # print(e)
            continue
    # calculate stats of given voxel
    voxel_stats(ens, voxnames=voxnames, stats=stats)
    return ens

def voxel_stats(ensamble, voxnames=[], stats=[]):
    """Calculate grid statistics from 3d voxels (pile of grids) along columns

    Args:
        ensamble (obj): primaryProduction.PP objects resulting from ensamble
        voxname (list): list of voxel name to process with stats
                        ['T', 'CHL', 'slope', 'euf', 'io', 'iz', 'PPn', 'PP', 'fz', 'PPfz']
        stats (list): list of stats to calculate (will result in [gridname]_[statname])
                      ['min','max','ptp','median','average','mean','std'] for more info on
                      statistics see:  https://numpy.org/doc/stable/reference/routines.statistics.html
                      n.b.: in 'average' statistics the weigths set in the ensamble._voxweigths are used
    """
    for v in voxnames:
        if v not in ensamble.voxel:
            raise ValueError(f'Provided voxname {v} not found in ensamble')
    for s in stats:
        if s not in ['min','max','ptp','median','average','mean','std']:
            raise ValueError(f'Statistics {s} not supported')
    
    for v in voxnames:
        for s in stats:
            # print(f'{v}_{s}')
            if s == 'average':
                ensamble.grid[f'{v}_{s}'] = getattr(np, s)(ensamble.voxel[v],axis=0, weights=ensamble._voxweigths)
            else:
                ensamble.grid[f'{v}_{s}'] = getattr(np, s)(ensamble.voxel[v],axis=0)

    
def plot_models_grid(models, gridname, title=None, size=[10,5], contours=False, labelsize=None, showpoints=False, limits=None, cmap='PiYG', savefile=None):
        """
        Plot the specified grid calculated with the different models

        Args:
            models (dict): dict of named primaryProduction.PP objects
            gridname (str): name of the variable gridded
            title (str): title of the plot
            size (list): width and height of the plot (dafault is [10,5])
            contours (bool): display contours?
            labelsize (float): size of the contour labels (applies only if contours is True)
            showpoints (bool): show sampling points of the profiles
            limits (list): interval for data plotting (e.g.: [1600,2000])
            cmap (str): name of color map to apply
            savefile (str): is not null save the image in the given filename
        """
        
        for mn, mi in models.items():
            mi.plot_grid(
                name=gridname, 
                title=f"{title} [{mn}]", 
                size=size, 
                contours=contours, 
                labelsize=labelsize, 
                showpoints=showpoints, 
                limits=limits, 
                cmap=cmap, 
                savefile=savefile
            )


    
    
    

# np.average([array_1, array_2], weights=[weight_1, weight_2], axis=0)