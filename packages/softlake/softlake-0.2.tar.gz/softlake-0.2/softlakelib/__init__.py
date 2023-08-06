
# -*- coding: utf-8 -*-
# ===============================================================================
#
#
# Copyright (c) 2015 IST-SUPSI (www.supsi.ch/ist)
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

"""
    [![](https://img.shields.io/static/v1?logo=gitlab&label=repo&message=on GitLab&color=orange)](https://gitlab.com/ist-supsi/softlake.git)

    Python packege `softlakelib` provides class and methods to estimate 
    the primary production in lakes starting from:

    * monthly profile observations time series: time (t), depth (z), primary production (PP), temperature (T), chlorophil-a (CHL), irradiance (I)
    * hourly climatic parameter time series: time (t), global irradinece (GI), wind speed (WS)

    ![Primary Production](./img/pp_example.png)

    `primaryProductionModel` offers basic class and methods to perform step by step estimations controlling inputs/outputs at every stage
    
    `ensamblePP` offers the ability to quickly set-up model configuration in a YAML file and calculate one or more models using different curves
    for fitting P/I curve (Primary Production based on the Irradiance at given depth). 
    
    Currently the library implements the following P/I curves, but it is already designed to be extended with other equations:

    * [`parker74`](./primaryProductionModel.html#softlakelib.primaryProductionModel.PP.parker74)

        *Ref:* Parker RA. 1974. Empirical functions relating metabolic
        processes in aquatic systems to environmental variables. J
        Fish Board Can. 31:1550–1552)

    * [`platt80`](./primaryProductionModel.html#softlakelib.primaryProductionModel.PP.platt80)

        *Ref:* Platt, T. G. C. L., Gallegos, C. L., & Harrison, W. G. (1981). 
        Photoinhibition of photosynthesis in natural assemblages of marine phytoplankton.

    * [`steele62`](./primaryProductionModel.html#softlakelib.primaryProductionModel.PP.steele62)

        *Ref:* Steele JH. 1962. Environmental control of photosynthesis in
        the sea. Limnol Oceanogr. 7:137–150.

    ## Install
        > pip install softlake

    ## Quick start
    ```python
        from softlakelib import ensemblePP

        # run the model according the specified settings
        m = ensamblePP.calculate_models('/home/settings.yml')

        # calculate the ensamble of the different curves
        en = ensamblePP.ensamble(m)

        # plot the Primary Production estimates for the given location in time and depth
        en.plot_grid(
            'PP',
            title=f'Estimated PP [µgC/h*m2]', 
            contours=False, 
            size=[20,10], 
            limits=['2006-04-01T00:00','2006-04-11T00:00'],
            voxel=True)
        
    ```

    ## YAML setting

    ```yaml
    model:
      name: esempio
      period: 2006-01-01T00:00/2007-12-31T00:00
      depth: 20
      z_res: 0.1
      verbose: True
      location: 
        lat: 45.944277
        lon: 8.954515
      profile_obs: 
        csv: data/profiles.csv
        date_parser:
      climatic_series: 
        csv: data/data_GI_VS_h.csv
        date_parser: "%Y%m%d%H"
      curves:
        parker74:
          showplot: False
          r2_min: 0.65
          verbose: False
          interpolation: linear
          weigth: 0.5
        platt80:
          showplot: False
          r2_min: 0.65
          verbose: False
          interpolation: linear
          weigth: 0.25
        steele62:
          showplot: False
          r2_min: 0.65
          verbose: False
          interpolation: linear
          weigth: 0.25
    ```
    
    
    ## License 
    
    `oatlib` is licensed under the terms of GNU GPL-2 or later, 
    meaning you can use it for any reasonable purpose and remain in 
    complete ownership of all the documentation you produce, 
    but you are also encouraged to make sure any upgrades to `oatlib` 
    itself find their way back to the community. 
    
    [GPL](https://www.gnu.org/licenses/licenses.html#GPL)
"""

# __all__ = ["modelPP","ensemblePP"]
__all__ = []
__version__ = "0.2"
