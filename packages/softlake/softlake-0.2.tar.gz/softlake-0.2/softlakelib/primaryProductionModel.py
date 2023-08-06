# -*- coding: utf-8 -*-
# ===============================================================================
#
# Authors: Massimiliano Cannata, Fabio Lepori, Camilla Capelli
#
# Copyright (c) 2020 IST-SUPSI (www.supsi.ch/ist)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#
# ===============================================================================

import pandas as pd
import numpy as np
from scipy.interpolate import griddata
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from scipy.stats import linregress
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
from datetime import datetime

import warnings
warnings.filterwarnings("ignore")

# functions of general utilities
def is_monotonic(x):
        dx = np.diff(x)
        return np.all(dx <= 0) or np.all(dx >= 0)


# PrimaryProduction Model
class PP():
    """General Class for Primary Production estimates"""
    
    def __init__(self, period, depth, z_res, location):
        r"""
        Class initializer
        
        Args:
            self (obj): the class
            period (str): start and end datetime period to model (e.g.: 2017-01-01/2018-02-31)
            depth (float): maximum depth to model (in meters from the lake surface)
            z_res (float): vertical resolution in meters
            location (list): [latitude, longitude]

        note:
            model time resolution is 1 hour
        """

        self.start, self.stop = period.split("/")
        self.depth = depth
        self.t_res = 1
        self.z_res = z_res
        self.profiles = None
        self.climate = None
        self.irradiance = None
        self.location = location
        self.grid = {}
        # number of steps in time (t) and depth (z)
        self.n_tsteps = int(((pd.to_datetime(self.stop) - pd.to_datetime(self.start))/pd.Timedelta(self.t_res,unit='h')))
        self.n_zsteps = int(self.depth/self.z_res)
        # PP standardization constant
        self._q10 = None
        self._tn = None        
        # values to calculate interpolation
        self.grid_t, self.grid_z = np.mgrid[0:self.n_tsteps+1, 0:self.depth:complex(self.n_zsteps-1)]
        self.date_rng =  pd.date_range(start=self.start, end=self.stop, freq=f'{self.t_res}T')
        # weigth for future statistics in ensabmble
        self._weigth = 1
        # storage of grid layers named (3d voxels)
        self.voxel = {}
        self._voxcolnames = []
        self._voxweigths = []

    def __repr__(self, lines=10):
        pd.set_option('display.max_rows', lines)
        rep  = f"period: {self.start}/{self.stop}\n"
        rep += f"location: {self.location}\n"
        rep += f"depth: {self.depth} [meters]\n"
        rep += f"time res: {self.t_res} [hours]\n"
        rep += f"depth res: {self.z_res} [meters]\n"
        rep += f"profiles: {self.profiles}\n"
        rep += f"irradiance: {self.irradiance}\n"
        rep += f"climate: {self.climate}\n"
        rep += f"grids: {list(self.grid.keys())}\n" 
        rep += f"voxels: {list(self.voxel.keys())}\n" 
        rep += ""
        return rep

    def date2step(self, date):
        """
        Convert a datetime with hour to the model timestep

        Args:
            date (datetime): datetime with hour

        Returns:
            step (int): model timestep at given date and hour
        """
        if date >= self.start and date <= self.stop:
            if isinstance(date, pd.DatetimeIndex):
                return int(((date - pd.to_datetime(self.start)).total_seconds()//3600)/(self.t_res/60))
            else:
                #return int(((pd.to_datetime(date) - pd.to_datetime(self.start)).total_seconds()//3600)/(self.t_res/60))
                return int((pd.to_datetime(date) - pd.to_datetime(self.start))/pd.Timedelta(self.t_res,unit='h'))
        else:
            raise ValueError("provided date and hour is not with the model period")
    
    def step2date(self, step, num=None):
        return pd.to_datetime(self.start) + int(step)*pd.Timedelta(self.t_res,unit='h')

    def step2datestr(self, step, num=None):
        return (pd.to_datetime(self.start) + step*pd.Timedelta(self.t_res,unit='h')).strftime("%d/%m/%Y, %H:%M")#isoformat()

    def period2step(self, period=[]):
        """
        convert a deatetime period to model time step interval
        """
        return [self.date2step(period[0]), self.date2step(period[1])]

    def step2period(self, period=[]):
        """
        convert a model time step interval to deatetime period
        """
        return [self.step2date(period[0]), self.step2date(period[1])]

    def set_pi_curve(self, curve='parker64'):
        """
        Set the P/I curve to be used by the model

        Args:
            curve (str): name of the P/I curve to use for modelling
        """
        curves = {
            'parker74': {
                'names':['pmax', 'iopt', 'beta'],
                'ranges' : {'pmax': (0,5),'iopt': (0,1000), 'beta': (0.2,1)},
                'init_val' : {'pmax': 2.2,'iopt': 100.1, 'beta': 0.80}
            },
            'steele62': {
                'names': ['pmax', 'iopt'],
                'ranges' : {'pmax': (0,5),'iopt': (0,1000)},
                'init_val' : {'pmax': 2.2,'iopt': 100.1}
                # 'init_val' : {'pmax': 0.877,'iopt': 57.1}
            },
            'platt80':{
                'names': ['ps', 'alpha', 'beta'],
                'ranges' : {'ps': (0,5),'alpha': (0,1000), 'beta': (0.2,1)},
                'init_val' : {'ps': 2.0,'alpha': 0.01, 'beta': 0.01}
            }
        }
        if curve in curves:
            self.pi_curve = curve
            self.pi_pars = curves[curve]
        else:
            raise ValueError(f'P/I curve not implemented: accepted curves are: {curves.keys()}')

    def set_profiles(self, csvfile, date_parser=None):
        """
        | Set the observed profiles data formatted as a CSV with the following structure:
        |    t,z,PP,T,CHL,I
        | 
        | where:
        |   t = date [multiple format supported, example DD-MM-YYYY, YYYY/MM/DD]
        |   z = depth :math:`[m]`
        |   PP = Primary Production :math:`[µg \cdot C \cdot L^{-1} \cdot hq^{-1}]`
        |   T = Temperature :math:`[°C]`
        |   CHL = Chlorophyll-a :math:`[µg \cdot L^{-1}]`
        |   I = Irradiance :math:`[µmol \cdot m^{-2} \cdot s^{-1}]`

        Args:
            csvfile (str): filepath to csv data file
            date_parser (str): datetime format for strptime reader

        Note:
            | This methods add the following columns to the *self.profile* element:
            | - **step** = associated model timestep
            | - **day** = associated day
        """
        if not date_parser:
            self.profiles = pd.read_csv(
                                csvfile, 
                                index_col=0, 
                                names=['t','z','PP','T','CHL','I'], 
                                parse_dates=True, 
                                infer_datetime_format=True, 
                                dayfirst=True, 
                                sep=",", 
                                header = 0)
        else: 
            dateparse = lambda x: datetime.strptime(x, date_parser)
            self.profiles = pd.read_csv(
                                csvfile, 
                                index_col=0, 
                                names=['t','z','PP','T','CHL','I'], 
                                parse_dates=True, 
                                infer_datetime_format=False, 
                                date_parser=dateparse,
                                dayfirst=True, 
                                sep=",", 
                                header = 0)
        # append a column with time step index (number of t_res from start)

        # adjust time to meet midday (12:00) if time is not given
        if self.profiles.index.hour[0]==0:
            self.profiles = self.profiles.shift(12, freq='H')
        
        # clip on model period
        #self.profiles = self.profiles[self.start:self.stop]
        
        self.profiles['step'] = (self.profiles.index - pd.to_datetime(self.start))/pd.Timedelta(self.t_res,unit='h')
        self.profiles['day'] = self.profiles.index.day

    def set_climatic_series(self, csvfile, usecols=None, sep=',', date_parser=""):
        """
        | Set the climatic hourly data, it should be a CSV with the follwoing structure:
        |    t,GI,WS = (time, Global Irradiance, Wind Speed)
        | 
        | where:
        |   t = datetime
        |   GI = Global Irradiation :math:`[µmol \cdot m^{-2} \cdot s^{-1}]`
        |   WS = Wind Speed :math:`[m^{2} \cdot s^{-1}]`
        
        Args:
            usecols (listl): specify csv columns names to parse
            sep (str):specify column separator
            date_parser (str): datetime format for strptime reader
        
        Note:
            This method stores climatic data in a pandas dataframe in the *self.climate* element
        """
        if not date_parser:
            self.climate = pd.read_csv(
                                csvfile, 
                                index_col=0, 
                                names=['t','GI','WS'], 
                                parse_dates=True, 
                                infer_datetime_format=True, 
                                dayfirst=True,
                                usecols=usecols,
                                sep=sep,
                                header = 0)
        else: 
            dateparse = lambda x: datetime.strptime(x, date_parser)
            self.climate = pd.read_csv(
                                csvfile, 
                                index_col=0, 
                                names=['t','GI','WS'], 
                                parse_dates=True, 
                                infer_datetime_format=False, 
                                dayfirst=True,
                                usecols=usecols,
                                date_parser=dateparse,
                                sep=sep,
                                header = 0)

        # take only model time interval data
        self.climate = self.climate.loc[self.start:self.stop]
        
        #self.climate['step'] = (self.climate.index - pd.to_datetime(self.start))/pd.Timedelta(self.t_res,unit='h')

    def drop_null_profile_rows(self, verbose=True):
        """
        Drop rows with any null values from the profile dataframe

        Args:
            verbose (bool): verbose outputs
        """
        if self.profiles.isnull().values.any():
            n = np.count_nonzero(self.profiles.isnull())
            self.profiles = self.profiles.dropna()
            if verbose:
                return f"Removed {n} lines from profiles dataframe"
        else:
            if verbose:
                return f"No nulls were found"

    def check_nulls_in_profiles(self):
        """
        Count null values in the profile dataframe
        """
        if self.profiles.isnull().values.any():
            return np.count_nonzero(self.profiles.isnull())
        else:
            return 0
    
    def check_nulls_in_climate(self):
        """
        Count null values in the profile dataframe
        """
        if self.climate.isnull().values.any():
            return np.count_nonzero(self.climate.isnull())
        else:
            return 0

    def make_grid(self):
        """
        Create the model grid in the (time, depth) dimensions
        
        Note: 
            | This method istantiates the following elements:
            | - **self.n_tsteps** = number of model timesteps
            | - **self.n_zsteps** = number of depth-steps
            | - **self.grid_t** = grid with the correct time values for each cell
            | - **self.grid_z** = grid with the correct depth values for each cell
        """
        if self.profiles == None:
            raise ValueError("model profiles are not set!")

        # number of steps in time (t) and depth (z)
        self.n_tsteps = int(((pd.to_datetime(self.stop) - pd.to_datetime(self.start))/pd.Timedelta(self.t_res,unit='h')))
        self.n_zsteps = int(self.depth/self.z_res)         

        # values to calculate interpolation
        self.grid_t, self.grid_z = np.mgrid[0:self.n_tsteps+1, 0:self.depth:complex(self.n_zsteps)]

    def interpolate_profiles(self,columns=['T','CHL'], method='cubic', extrapolate=True):
        """
        Interpolates profile data in time and depth and save the results in the self.grid element, 
        which is a dictionary of named grids

        Args:
            columns (list): list of column names from the profile variables to interpolate
            method (str): method of interpolation, select one of: ‘linear’, ‘nearest’, ‘cubic’ (default is 'cubic')
            extrapolate (bool): extrapolate from min to max depth the interpolation

        Note:
            if extrapolate i sset to *False* the interpolation is limited within the convex hull given by observed data
            (e.g.: if first observed depth is at 1 m, from 0 to 1 m you'll have NaN values)

        References:
            https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.griddata.html
        """
        for d in columns:
            if extrapolate:
                points = None
                #  unique_id = np.unique(self.points.index)
                for t in np.unique(self.profiles.index):   
                    min_z = self.profiles.loc[t]['z'].min()
                    max_z = self.profiles['z'].max()
                    # extract the single profile
                    X = self.profiles.loc[t][['step','z',d]].values
                    if min_z > 0:
                        # prepend a null value
                        prep_val = np.interp(0, X[:,1], X[:,2])
                        X = np.insert(X, 0, [X[0,0],0,prep_val], axis=0)
                    if max_z < self.depth: 
                        # append a null value
                        app_val = np.interp(self.depth, X[:,1], X[:,2])
                        X = np.append(X, [[X[0,0],self.depth,np.nan]], axis=0)
                    if points is None:
                        points = X
                    else:
                        points = np.concatenate([points, X])
                #print(points)
                self.grid[d] = griddata(points[:,0:2], points[:,2], (self.grid_t, self.grid_z), method=method)
            # if method != 'nearest':
            #     fill = griddata(points, values, (self.grid_t, self.grid_z), method='nearest')
            #     self.grid[d] = np.where(np.isnan(interp),fill,interp)

            # df = pd.DataFrame(self.grid[d])
            # df.fillna(method='ffill', axis=1, inplace=True)
            # self.grid[d] = df.as_matrix()

    def estimate_light_extintion_slope(self, keep_only=None, showplots=False, r_limits=[-0.95,0.95]):
        """
        Estimation of Irradiance (I) extintion parameters using linear regression of depth vs log(I)
        
        Args:
            keep_only (list): list of column names (str) to be saved, others are deleted
            showplots (bool): if true, plots of data and regression line are shown
            r_limits (list): list of two bounding limits [min,max] for r_value to accept the results

        Note:
            | This method appends the following columns to the *self.parameters* element:
            | - **slope**: the slope coefficient of the regression line
            | - **intercept**: the intercept of the regression line
            | - **r_value**: R of the regression (Correlation coefficient)
            | - **p_value**: P of the regression (Two-sided p-value)
            | - **std_err**: STD of the regression (Standard error of the estimated gradient)

        Refrences:
            https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.linregress.html
            
        """

        existing_columns = list(self.parameters.columns)
        keep_only = existing_columns + keep_only
        
        self.parameters['slope'] = np.nan
        self.parameters['intercept'] = np.nan
        self.parameters['r_value'] = np.nan
        self.parameters['p_value'] = np.nan
        self.parameters['std_err'] = np.nan

        # all measures grouped day by day
        steps = self.profiles.groupby(['step'])
        for step, profs in steps:
            d = int(step)
            pro = profs[(profs['I'] > 0)]
            slope, intercept, r_value, p_value, std_err = linregress(pro['z'],np.log(pro['I']))
            self.parameters.at[d,['slope','intercept','r_value','p_value','std_err']] = np.float64([slope, intercept, r_value, p_value, std_err])

            if showplots:
                col = 'blue'
                plt.figure(figsize=(6, 4))
                mn = pro['z'].min()
                mx = pro['z'].max()
                x1 = np.linspace(mn,mx,500)
                y1 = slope * x1 + intercept
                
                plt.xlabel("depth (m)")
                plt.ylabel("Log of Irradiance (I)")
                tit = f"Irrdiance extintion at step {step}\n"
                tit += f"(R: {r_value}; P: {p_value}; STD: {std_err})"
                if (r_limits[0] < r_value < r_limits[1]):
                    tit += "WARNING: low correlation coefficient"
                    col = 'red'
                
                plt.title(tit)
                plt.plot(pro['z'],np.log(pro['I']),'ob', color=col)
                plt.plot(x1,y1,'-r', color=col)

        if keep_only:
            self.parameters.drop(self.parameters.columns.difference(keep_only), 1, inplace=True)
        
        return plt.show()

    def estimate_PAR(self, ws_xyz=[0.6225, 0.8291, 0.235145], ratio = 0.45*4.6, Is = 2111.5, keep_only=None):
        """
        Calculate PAR in time from GI and WS and store in *self.irradiance* element according to Walsby (1997)

        Args:
            ws_xyz (list): wind speed parameters 
            ratio (float): Ratio Ia/I :math:`[μmol/J]`
            Is (float): Solar irradiation coefficient [μmol m-2 s-1]
            keep_only (list): list of column names (str) to be saved

        Returns:
            updated table *self.climate*

        Note:
            | Append the following columns to the self.parameters element:
            | - **doy**: day of the year (Y) expressed as the orbital angle of the Earth
            | - **phi**: day of the years in radians (ψ)
            | - **sdec**: solar declination (𝛿) [rad]
            | - **lst**: local solar time (t) [h]
            | - **lst_rad**: local solar time in radians (τ)
            | - **selev**: Solar elevation above the horizon (ε) [rad]
            | - **zenit**: Zenit angle (θ) [rad]
            | - **r**: Proportion reflected (r)
            | - **eff_zenit**: Effective zenital angle (θw) [rad] (considering wind factors)
            | - **rw**: Proportion reflected (r) (considering wind factors)
            | - **Ia**: PAR irradiance without correction (Ia) [μmol m-2 s-1]
            | - **Iu**: PAR irradiance with correction for reflection (Iu) [μmol m-2 s-1]
            | - **Ic**: PAR irradiance with correction for sine curve - estimate of the maximum possible surface PAR (Ic) [μmol m-2 s-1]
            | - **Io**: PAR irradiance with correction for reflection + wind + cloud (Io) [μmol m-2 s-1]

        References:
            Walsby, A.E. Numerical integration of phytoplankton photosynthesis through time and depth in a water column. The New Phytologist 1997, 136, 189–209.

        """

        # convert location to radians
        lat_rad = self.location[0] * np.pi / 180
        lon_rad = self.location[1] * np.pi / 180

        # wind speed 
        ws_x, ws_y, ws_z = ws_xyz

        # day of the year (Y) expressed as the orbital angle of the Earth (from 0 to...) Y
        self.climate['doy'] = self.climate.index.dayofyear - 1

        # orbital angle of the Earth, ψ = 2 PI doy / 365
        # day of the years in radians (ψ)
        self.climate['phi'] = 2 * np.pi * self.climate['doy'] / 365

        # solar declination (𝛿) [rad]
        self.climate['sdec'] = (
                                    0.39637 \
                                    - 22.9133 * np.cos(self.climate['phi']) \
                                    + 4.02543 * np.sin(self.climate['phi']) \
                                    - 0.3872 * np.cos(2*self.climate['phi']) \
                                    + 0.052 * np.sin(2*self.climate['phi'])
                                ) * np.pi / 180

        # local solar time (t) [h]
        #self.climate['lst'] = self.climate.index.hour +  self.climate.index.minute/60

        # Equation of Time 
        self.climate['B'] = 360/365*(self.climate['doy']+1-81)
        self.climate['EoT'] = 9.87*np.sin(2*self.climate['B'])-7.53*np.cos(self.climate['B'])-1.5*np.sin(self.climate['B'])

        # Local Standard Time Meridian
        self.time_zone = 1
        self.climate['lst'] = self.climate.index.hour + ((4*(self.location[1]-(15*self.time_zone))+self.climate['EoT'])/60)

        # local solar time in radians (τ)
        self.climate['lst_rad'] = 2 * np.pi * self.climate['lst'] / 24

        # Solar elevation above the horizon (ε) [rad]
        # max (0,selev)
        self.climate['selev'] = np.arcsin(
                                        (np.sin(lat_rad) * np.sin(self.climate['sdec'])) \
                                        - (np.cos(lat_rad) * np.cos(self.climate['sdec']) * np.cos(self.climate['lst_rad']) )
                                    ) 
        self.climate['selev'] = np.where(self.climate['selev'] < 0, 0, self.climate['selev'])

        # Zenit angle (θ) [rad]
        self.climate['zenit'] = (np.pi/2) - self.climate['selev']

        # Proportion reflected (r)
        self.climate['as'] = np.arcsin(np.sin(self.climate['zenit'])/1.33)
        self.climate['r'] =  (
                                (0.5 * (np.square(np.sin(self.climate['zenit'] - self.climate['as'])))) \
                                / (np.square(np.sin(self.climate['zenit'] + self.climate['as']))) + \
                                (0.5 * np.square(np.tan(self.climate['zenit'] - self.climate['as']))) \
                                / (np.square(np.tan(self.climate['zenit'] + self.climate['as'])))
                            )

        # Effective zenital angle (θw) [rad]
        self.climate['eff_zenit'] = self.climate['zenit'] * (ws_y + (1 - ws_y) * (np.exp(-ws_z * np.power(self.climate['WS'],ws_x))))

        # Proportion reflected (r)
        self.climate['asr'] = np.arcsin(np.sin(self.climate['eff_zenit']) / 1.33)
        # self.climate['rw'] = 0.5 * (np.square(np.sin(self.climate['eff_zenit'] - self.climate['asr']))) \
        #                     / (np.square((np.sin(self.climate['eff_zenit'] + self.climate['asr'])))) \
        #                      + 0.5 * (np.square(np.tan(self.climate['eff_zenit'] - self.climate['asr']))) \
        #                     / (np.square((np.tan(self.climate['eff_zenit'] + self.climate['asr']))))
        self.climate['rw'] =  (
                                (0.5 * (np.square(np.sin(self.climate['eff_zenit'] - self.climate['asr'])))) \
                                / (np.square(np.sin(self.climate['eff_zenit'] + self.climate['asr']))) + \
                                (0.5 * np.square(np.tan(self.climate['eff_zenit'] - self.climate['asr']))) \
                                / (np.square(np.tan(self.climate['eff_zenit'] + self.climate['asr'])))
                            )

        self.climate.drop(columns=['asr','as'], inplace=True)

        # PAR irradiance without correction (Ia) [μmol m-2 s-1]
        self.climate['Ia'] = self.climate['GI'] * ratio

        # PAR irradiance with correction for reflection (Iu) [μmol m-2 s-1]
        self.climate['Iu'] = self.climate['Ia'] * ( 1 - self.climate['r'])

        # PAR irradiance with correction for reflection + wind (Iw) [μmol m-2 s-1]
        self.climate['Iw'] = self.climate['Ia'] * ( 1 - self.climate['rw'])

        # Correction sine curve - estimate of the maximum possible surface PAR (Ic) [μmol m-2 s-1]
        self.climate['Ic'] = np.sin(self.climate['selev']) * Is

        # PAR irradiance with correction for reflection + wind + cloud (Io) [μmol m-2 s-1]
        self.climate['Io'] = np.where( (self.climate['Ia']/self.climate['Ic'])< 0.5, 0.948*self.climate['Ia'], self.climate['Iw'])
        self.climate['Io'] = np.where( self.climate['Ic'] == 0, self.climate['Iw'], self.climate['Io'])

        self.irradiance = self.climate.copy(deep=True)
        # self.irradiance = self.climate.resample(f'{self.t_res}T').mean().asfreq(f'{self.t_res}T')
        # self.irradiance.reindex(self.date_rng, method='nearest')

        if keep_only:
            self.irradiance.drop(self.irradiance.columns.difference(keep_only), 1, inplace=True)

        self.irradiance['step'] = (self.irradiance.index - pd.to_datetime(self.start))/pd.Timedelta(self.t_res,unit='h')
        
        self.climate.drop(self.climate.columns.difference(['GI', 'WS', 'step']), 1, inplace=True)
 
    def plot_grid(self, name, title=None, size=[10,5], contours=True, labelsize=None, showpoints=False, limits=None, cmap='PiYG', savefile=None, voxel=False):
        """
        Plot the interpolated grid specified with the column name

        Args:
            name (str): name of the variable gridded
            title (str): title of the plot
            size (list): width and height of the plot (dafault is [10,5])
            contours (bool): display contours?
            labelsize (float): size of the contour labels (applies only if contours is True)
            showpoints (bool): show sampling points of the profiles
            limits (list): interval for data plotting (e.g.: [1600,2000])
            cmap (str): name of color map to apply
            savefile (str): is not null save the image in the given filename
            voxel (bool): is the varable gridded name in voxel?
        """
        # pick the desired colormap, sensible levels, and define a normalization
        # instance which takes data values and translates those into levels.
        #levels = MaxNLocator(nbins=15).tick_values(self.grid[name].T.min(), self.grid[name].T.max())

        if voxel:
            grids = self.voxel[name]
        else:
            grids = [self.grid[name]]
        
        i = -1
        for grid in grids:
            i += 1
            fig, ax = plt.subplots()
            plt.cla()
            plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: self.step2datestr(x+limits[0])))
            plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: str(x*self.z_res)))
            plt.gca().invert_yaxis()
            colmap = plt.get_cmap(cmap)
            
            if size:
                plt.gcf().set_size_inches(size[0], size[1])

            if limits:
                if not isinstance(limits[0], int):
                    limits = [self.date2step(limits[0]),self.date2step(limits[1])]
                im = plt.pcolormesh(grid[limits[0]:limits[1]].T, cmap=colmap)
            
            else:
                im = plt.pcolormesh(grid.T, cmap=colmap)
                limits = [0, self.n_zsteps]
            plt.gcf().colorbar(im, orientation='horizontal')

            if contours:
                cs = plt.contour(grid.T, colors='black')
                if labelsize: 
                    plt.clabel(cs, inline=1, fontsize=labelsize)
            if title:
                if voxel:
                    plt.title(f'{title} - {self._voxcolnames[i]}')
                else:
                    plt.title(title)
            
            # TODO: adjust z ticks based on z_res
            # plt.yticks = plt.yticks * self.z_res

            plt.ylabel(f'depth [m]')
            plt.xlabel('time', labelpad=8)
                    
            if showpoints:
                points = (self.profiles[['step','z']].values)
                plt.plot(points[:,0], points[:,1]*10, 'k.', ms=2)
            if savefile:
                plt.savefig(savefile)
            plt.show()

    def standardizePP(self, q10=2, tn=10):
        r"""
        | Standardize Primary Production by standardizing by phyto-plankton biomass (Chl-a) and then reducing to a standard temperature.   
        | Requires profiles column data CHL and T to be set.  
        
        | :math:`P_{norm}^b(z) = P^b(z) \cdot e^{ (\frac{ \ln{(Q_10)} \cdot (T_{norm} - T(z)) } {10} )}`

        Args:
            q10 (float): coefficient (from Finger et al. 2013 the default value is 2) :math:`\equiv Q_10`
            tn (float): reference temperature (from Finger et al. 2013 the default value is 10 °C) :math:`\equiv T_{norm}`

        Note:
            It produce a new column named PPn in the profiles dataframe.
        
        References:
            Finger D, Wüest A, Bossard P. 2013. Effects of oligotrophication
            on primary production in peri-alpine lakes. Water Resour Res. 49:4700–4710
        """
        if not type(self.profiles):
            raise ValueError('profile element should be set (see set_profiles method)')
        if not (
                'PP' in self.profiles.columns and 
                'CHL' in self.profiles.columns and 
                'T' in self.profiles.columns):
            raise ValueError('PP, CHL and T attribute must be set in the *self.profile* element')

        self._q10 = q10
        self._tn=tn
        self.profiles['PPn'] = (self.profiles['PP']/self.profiles['CHL']) * np.exp((np.log(q10)*(tn-self.profiles['T']))/10)
    
    def parker74(self, Iz, pmax, iopt, beta):
        r"""
        Curve for standardized Primary Production estimation based on the Irradiance at given depth (Iz)
        according the formulation proposed by Steel (1962) and modified by Parker (1974) 

        Args:
            Iz (float): irradiance at depth z [µmol m-2 s-1]
            pmax (float): maximum possible production rate [µg C (µg Chl-a)-1 h-1]
            Iopt: optimal light instensity [µmol m-2 s-1]
            beta: shape coefficient [-]
        
        Returns:
            float: standardized Primary Production [µg C (µg Chl-a)-1 h-1]
        
        References:
            Parker RA. 1974. Empirical functions relating metabolic
            processes in aquatic systems to environmental variables. J
            Fish Board Can. 31:1550–1552
        """
        return pmax * np.power((Iz / iopt * np.exp(1-Iz/iopt)), beta)

    def steele62(self, Iz, pmax, iopt):
        """
        Curve for standardized Primary Production estimation based on the Irradiance at given depth (Iz)
        according the formulation proposed by Steel (1962)

        Args:
            Iz (float): irradiance at depth z [µmol m-2 s-1]
            pmax (float): maximum possible production rate [µg C (µg Chl-a)-1 h-1]
            Iopt: optimal light instensity [µmol m-2 s-1]
        
        Returns:
            float: standardized Primary Production [µg C (µg Chl-a)-1 h-1]

        References:
            Steele JH. 1962. Environmental control of photosynthesis in
            the sea. Limnol Oceanogr. 7:137–150.
        """
        return pmax * (Iz / iopt) * np.exp(1-Iz/iopt)

    def platt80(self, Iz, ps, alpha, beta):
        """
        Curve for standardized Primary Production estimation based on the Irradiance at given depth (Iz)
        according the formulation proposed by Platt et al. (1980)

        Args:
            Iz (float): irradiance at depth z [µmol m-2 s-1]
            ps (float): maximum possible production rate related parameter [µg C (µg Chl-a)-1 h-1]
            alpha (float): photoinibhition parameter [-]
            beta (float): photoinibhition parameter [-]

        Returns:
            float: standardized Primary Production [µg C (µg Chl-a)-1 h-1]
            
        References:
            Platt, T. G. C. L., Gallegos, C. L., & Harrison, W. G. (1981). Photoinhibition of photosynthesis in natural assemblages of marine phytoplankton.
        """
        return ps * (1 - np.exp((alpha*Iz)/ps)) * np.exp((beta*Iz)/ps)

    def grid_parameters(self):
        """
        Create the grids of model's parameters

        Note:
            | This methods create the following grids in the *sel.grid* element:
            | - **slope** = slope of light extintion [-]
            | - **iopt** = the optimum light intensity :math:`[μmol \cdot m^{-2} \cdot s^{−1}]`
            | - **pmax** = the maximum photosynthetic potential :math:`[μmol \cdot m^{-2} \cdot s^{−1}]``
            | - **beta** = exponential coefficient [-]
        """

        self.grid['slope'] = np.nan * np.empty(self.grid_t.shape)
        for par in self.pi_pars['names']:
            self.grid[par] = np.nan * np.empty(self.grid_t.shape)
        
        
        for index, row in self.parameters.iterrows():
            try:
                self.grid['slope'][int(index)-1,:] = row['slope']
            except:
                pass
            for par in self.pi_pars['names']:
                try:
                    self.grid[par][int(index)-1,:] = row[par]
                except:
                    pass

    def grid_irradiance(self):
        """
        Create a grid of the irradiance values

        Note:
            | This methods create the following two grids in the *self.grid* element:
            | - **io** = PAR-0 :math:`[μmol \cdot m^{-2} \cdot s^{−1}]`
            | - **iz** = Irradiance estimated at timestep ts and depth z :math:`[μmol \cdot m^{-2} \cdot s^{−1}]`
        """
        self.grid['io'] = np.nan * np.empty(self.grid_t.shape)
        for index, row in self.irradiance.iterrows():
            try:
                self.grid['io'][int(row.step),:] = row.Io
            except:
                pass
        self.grid['iz'] = np.exp(self.grid['slope'] * self.grid_z + np.log(self.grid['io']) )

    def calculate_PPn(self):
        """
        Estimates the standardized Primary Production

        Note:
            This method requires the
        """
        # TODO: make an ensable of different curves
        pars = {}
        for p in self.pi_pars['names']:
            pars[p] = self.grid[p]
        
        self.grid['PPn'] = getattr(self, self.pi_curve)(self.grid['iz'], **pars)

    def destandardizePP(self, q10=None, tn=None):
        """
        Calculates the grid of Primary Production values starting from standardized Primary Production (PPn) and Chlorophill-a (CHL) grids

        note:
            This method store the new grid *PP* in the *self.grid* element
        """
        if not q10:
            if self._q10:
                q10 = self._q10
            else:
                q10 = 2 # coefficient from Finger et al. 2013
        if not tn:
            if self._tn:
                tn = self._tn
            else:
                tn = 10 # reference temperature from Finger et al. 2013

        self.grid['PP'] =  (self.grid['PPn']*self.grid['CHL']) * np.exp( ( np.log(q10) *( self.grid['T'] - tn)) / 10)

        #a = np.log(Q10) * (Tn * self.grid['T']) / 10
        #self.grid['PP'] = np.exp(np.log(self.grid['PPn']) - a) * self.grid['CHL']
        #=$I3*((AX3/$H3*EXP(1-AX3/$H3))^$G3)*EXP((LN($'P-I curves'.$E$2)*($PP.J3-$'P-I curves'.$E$3))/10)

    def Iz(self, s, z, io):
        """
        Calculate Irradiance at given location

        Args:
            s (int): light slope gradient
            z (float): depth at wich calculate the Irradiance
            io (float): irradiance at zero level (PAR)
        Returns:
            Irradiance :math:`[μmol \cdot m^{-2} \cdot s^{−1}]`
        """
        return np.exp( s*z + np.log(io))

    def estimate_params(self, r2_min = None, verbose=False, showplots=False):
        r"""
        Estimates the parameter of the P-I equation proposed by Steel (1962) and modified by Parker (1974) and 
        populate the model element parameters with a dataframe of best fit of the pmax, iopt and beta parameters

        Args:
            par_ranges (dict): dictionary of min,max values of the parameters (default is {'pmax': (0,5),'iopt': (0,1000), 'beta': (0.2,1)})
            par_init (dict): dictionary of start values of the parameters (default is {'pmax': 2.2,'iopt': 100.1, 'beta': 0.80})
            r2_min (float): if set, identifies the maximum r-squared (coefficient of determination) value to consider valid the fitting;
            verbose (bbol): if True print additional information on parameters values and errors
            showplots (bool): if True plot the data and the fitting curve to bettee understand goodness of fit

        Note:
            |This method create the following columns in the *self.parameters* element:
            | - **slope** = slope of light extintion [-]
            | - **iopt** = the optimum light intensity :math:`[μmol \cdot m^{-2} \cdot s^{−1}]`
            | - **pmax** = the maximum photosynthetic potential :math:`[μmol \cdot m^{-2} \cdot s^{−1}]`
        
        Reference: 
            Parker RA. 1974. Empirical functions relating metabolic processes in aquatic systems to environmental variables. J Fish Board Can. 31:1550–1552.
        """

        # TODO: add dict of parameters df with P/I curve name as key
        self.parameters = pd.DataFrame(
                                    index = range(1, self.n_tsteps+1), 
                                    columns=self.pi_pars['names'],
                                    dtype=np.int64)
        
        pinit = [self.pi_pars['init_val'][p] for p in self.pi_pars['names']]
        
        steps = self.profiles.groupby(['step'])

        func = getattr(self, self.pi_curve)

        # iterate steps
        for step, profs in steps:
            # select only positive I and PPn
            pro = profs[(profs['I'] > 0) & (profs['PPn']>0)]
            nopro = profs[(profs['I'] < 0) | (profs['PPn']<0)]
            monotonic = False
            col = 'blue'

            try:
                if verbose:
                    print(f"function: {self.pi_curve}")
                    print(f"parmeters: {self.pi_pars['names']}")
                    print(f"ranges: {self.pi_pars['ranges']}")
                    print(f"initial values: {self.pi_pars['init_val']}")
                
                # TODO: add parameters bounds([min],[max]) & method(‘lm’, ‘trf’)
                params, params_covariance = curve_fit(func, pro['I'], pro['PPn'], p0=pinit)
                
                if verbose:
                    print(f'curve fitted: {params}')
                
                if is_monotonic(func(pro['I'], *params)):
                    if verbose:
                        print(f"step {step}: MONOTONIC FUNCTION, is not possible to estimate the parameters")
                    monotonic = True
                    self.parameters.at[int(step)]= [np.nan] * len(self.pi_pars['names'])
                    
                else:
                    if r2_min:
                        r2 = 0
                        # from: https://stackoverflow.com/questions/29003241/how-to-quantitatively-measure-goodness-of-fit-in-scipy
                        #----------------------------------------------------------------------------------------------------------
                        # residual sum of squares
                        # ss_res = np.sum((pro['PPn'] - self.P74(profs['I'], params[0], params[1], params[2])) ** 2)
                        ss_res = np.sum((pro['PPn'] - func(pro['I'], *params)) ** 2)
                        # total sum of squares
                        ss_tot = np.sum((pro['PPn'] - np.mean(pro['PPn'])) ** 2)
                        # r-squared
                        r2 = 1 - (ss_res / ss_tot)
                        if verbose:
                            print(f"r2: {r2}") 
                        if r2 > r2_min:
                            self.parameters.at[int(step)]= np.float64(params)
                        else:
                            self.parameters.at[int(step)]= [np.nan] * len(self.pi_pars['names'])
                    else:
                        self.parameters.at[int(step)]= np.float64(params)
                    
                    if verbose:
                        print(f"step: {step}," + ",".join([f"{p}: {params[i]}" for i, p in enumerate(self.pi_pars['names'])]))
                
                if showplots:
                    plt.figure(figsize=(6, 4))
                    #plt.scatter(profs['PPn'], profs['I'], label='Data', color='red')
                    plt.scatter(pro['PPn'], pro['I'], color='green')
                    plt.scatter(nopro['PPn'], nopro['I'], color='red', marker='x')
                    plt.xlabel("Normalized Primary Production (PPn)")
                    plt.ylabel("Irradiance (I)")
                    tit = f'Curve fitting at step {step}\n'
                    tit += ",".join([f"{p}: {params[i]}" for i, p in enumerate(self.pi_pars['names'])])+"\n"
                    if r2_min and not monotonic:
                        tit += f"r2: {r2}"
                    if monotonic:
                        tit = tit + ' (Function is MONOTONE: parameters are not saved)'
                        col = 'red'

                    plt.title(tit)
                    x_fit = np.linspace(np.min(profs['I']), np.max(profs['I']), 100)
                    plt.plot(func(x_fit, *params), x_fit,
                            label='Fitted function', color=col)
                    # plt.plot(self.P74(profs['I'], params[0], params[1], params[2]), profs['I'],
                    #         label='Fitted function', color=col)
                    
             
            except Exception as e:
                if verbose:
                    print("EEROR:",e)
                if showplots:
                    plt.figure(figsize=(6, 4))
                    plt.scatter(profs['PPn'], profs['I'], label='Data', color='green')
                    plt.xlabel("Normalized Primary Production (PPn)")
                    plt.ylabel("Irradiance (I)")
                    plt.title(e)
        
        self.parameters['t'] = pd.to_datetime(self.start) + self.parameters.index * pd.Timedelta(self.t_res,unit='h')
        
    def parameters_interpolation_test(self, parameter, methods=None, exclude=None):
        #fig, x = plt.subplots()
        available_methods = {
                'linear': {'method': 'linear', 'order': None},
                'bspline': {'method': 'spline','order': 2},
                'cubic_spline': {'method': 'spline','order': 3},
                'nearest': {'method': 'nearest'}, 
                '2ord_poly': {'method': 'polynomial', 'order': 2},
                '3ord_poly': {'method': 'polynomial', 'order': 3},
                '5ord_poly': {'method': 'polynomial', 'order': 5},
                'pchip': {'method': 'pchip'}
            }
        if not methods:
            m = available_methods
        else:
            m = {}
            for k in methods:
                if k in available_methods:
                    m[k] = available_methods[k]
                else:
                    raise ValueError(f'method {k} is not defined, choose among {list(available_methods.keys())}')

        if exclude:
            for e in exclude:
                if e in m:
                    del m[e]

        f = pd.DataFrame()
        
        self.parameters.sort_index(inplace=True)
        
        for k in m.keys():
            f[f'{k}'] = (self.parameters[parameter]*100).interpolate(**m[k], axis=0, inplace=False, limit_direction='both')

        (f/100).plot()

        return self.parameters[parameter].plot(style='.',color='black')

    def parameter_interpolate(self, parameter=[], method=None):
        #fig, x = plt.subplots()
        available_methods = {
                'linear': {'method': 'linear', 'order': None},
                'bspline': {'method': 'spline','order': 2},
                'cubic_spline': {'method': 'spline','order': 3},
                'nearest': {'method': 'nearest'}, 
                '2ord_poly': {'method': 'polynomial', 'order': 2},
                '3ord_poly': {'method': 'polynomial', 'order': 3},
                '5ord_poly': {'method': 'polynomial', 'order': 5},
                'pchip': {'method': 'pchip'}
            }
        if method not in available_methods.keys():
            raise ValueError(f'method {method} is not defined, choose among {list(available_methods.keys())}')
        
        if isinstance(parameter, str):
            self.parameters[parameter] = (self.parameters[parameter]*100).interpolate(**available_methods[method], axis=0, inplace=False, limit_direction='both')/100
        elif not parameter:
            for p in self.parameters.columns.difference(['t']):
                self.parameters[p] = (self.parameters[p]*100).interpolate(**available_methods[method], axis=0, inplace=False, limit_direction='both')/100
        else:
            for p in parameter:
                self.parameters[p] = (self.parameters[p]*100).interpolate(**available_methods[method], axis=0, inplace=False, limit_direction='both')/100

    def PP_stats(self, grid='PP', period=[], colstat='sum', timestat=[('D','sum'),('M','sum')]):
        """
        Calculate statistics of a grid

        Returns:
            Pandas' time series with time and aggregated statistics
        """
        if period:
            if not isinstance(period[0],int):
                speriod = self.period2step(period)
                tperiod = period
            else:
                speriod = period
                tperiod = step2period(period)
        else:
            speriod = [0,self.n_tsteps]
            tperiod = [self.start,self.stop]

        # calculate column statistics
        column_aggregated = getattr(np, colstat)(self.grid[grid][speriod[0]:speriod[1]].T, axis=0)*self.z_res
        
        # create pandas time series
        data = pd.Series(column_aggregated, 
                        index=pd.date_range(start=pd.to_datetime(tperiod[0]), end=pd.to_datetime(tperiod[1]), freq='h')[:-1]
                        )
        
        # aggregate in time statistics
        for t in timestat:
            data = getattr(data.resample(t[0]), t[1])()
        
        return data

    def calculate_photic_zone(self):
        """
        Calculate Photic Zone mask (filtered where 1% of PAR) and apply to Primary Production grid
        """
        def photic_zone_depth(a):
            try:
                r = np.where(a > (0.01*a[0]), 1, np.nan)
            except:
                r = a
            return r
        self.grid['fz'] = np.apply_along_axis(photic_zone_depth, 1, self.grid['iz'])
        self.grid['PPfz'] = self.grid['PP'] * self.grid['fz']

    def summary_results(self, tperiod=None):
        """
        Print statistics of model results

        Args:
            tperiod (list): list of begin,end datetime to extract statistics (e.g.: ['2016-01-01T00:00','2017-12-01T00:00'])
            figsize (tuple): tuple of width,height of result plot (e.g.: (30,10))
        """
        if not tperiod:
            tperiod = [f"{self.start}" f"{self.stop}"]
        # Primary Production stats
        self.monthly_sum = self.PP_stats(grid='PP', period=tperiod, colstat='sum', timestat=[('D','sum'),('M','sum')])
        self.monthly_mean = self.PP_stats(grid='PP', period=tperiod, colstat='sum', timestat=[('D','sum'),('M','mean')])
        self.yearly_sum = self.PP_stats(grid='PP', period=tperiod, colstat='sum', timestat=[('Y','sum')])
        
        # Photic Primary Production
        self.monthly_sum_fz = self.PP_stats(grid='PPfz', period=tperiod, colstat='nansum', timestat=[('D','sum'),('M','sum')])
        self.monthly_mean_fz = self.PP_stats(grid='PPfz', period=tperiod, colstat='nansum', timestat=[('D','sum'),('M','mean')])
        self.yearly_sum_fz = self.PP_stats(grid='PPfz', period=tperiod, colstat='nansum', timestat=[('Y','sum')])

    def plot_summary_results(self, figsize):
        """
        Print statistics of model results

        Args:
            tperiod (list): list of begin,end datetime to extract statistics (e.g.: ['2016-01-01T00:00','2017-12-01T00:00'])
            figsize (tuple): tuple of width,height of result plot (e.g.: (30,10))
        """
        # # Primary Production stats
        # monthly_sum = self.PP_stats(grid='PP', period=tperiod, colstat='sum', timestat=[('D','sum'),('M','sum')])
        # monthly_mean = self.PP_stats(grid='PP', period=tperiod, colstat='sum', timestat=[('D','sum'),('M','mean')])
        # yearly_sum = self.PP_stats(grid='PP', period=tperiod, colstat='sum', timestat=[('Y','sum')])
        
        # Photic Primary Production
        # monthly_sum_fz = self.PP_stats(grid='PPfz', period=tperiod, colstat='nansum', timestat=[('D','sum'),('M','sum')])
        # monthly_mean_fz = self.PP_stats(grid='PPfz', period=tperiod, colstat='nansum', timestat=[('D','sum'),('M','mean')])
        # yearly_sum_fz = self.PP_stats(grid='PPfz', period=tperiod, colstat='nansum', timestat=[('Y','sum')])

        fig, axs = plt.subplots(nrows=2, ncols=3, figsize=figsize)

        self.monthly_sum.plot(kind="bar",ax=axs[0,0], title='monthly PP sum', color='g')
        self.monthly_mean.plot(kind="bar",ax=axs[0,1], title='monthly mean of PP daily sum', color='g')
        self.yearly_sum.plot(kind="bar",ax=axs[0,2], title='yearly PP sum', color='g')

        axs[0,0].get_xaxis().set_visible(False)
        axs[0,1].get_xaxis().set_visible(False)
        axs[0,2].get_xaxis().set_visible(False)

        self.monthly_sum_fz.plot(kind="bar",ax=axs[1,0], title='monthly Photic Zone PP sum', color='g')
        self.monthly_mean_fz.plot(kind="bar",ax=axs[1,1], title='monthly Photic Zone  mean of PP daily sum', color='g')
        self.yearly_sum_fz.plot(kind="bar",ax=axs[1,2], title='yearly Photic Zone  PP sum', color='g')

        return plt.show(fig)
        

