# -*- coding: utf-8 -*-
"""
Contains objects for interfacing ``gridwxcomp`` with gdal command line tools
used for spatial interpolation of scattered point data.
"""
import os
import subprocess
import xml.etree.cElementTree as ET
from copy import copy
from pathlib import Path
from xml.dom import minidom

import numpy as np
import pandas as pd

# allows for CL script usage if gridwxcomp not installed
try:
    from .spatial import get_subgrid_bounds, zonal_stats, calc_pt_error
    from .plot import station_bar_plot
except:
    from spatial import get_subgrid_bounds, zonal_stats, calc_pt_error
    from plot import station_bar_plot

class InterpGdal(object):
    """
    Usage of gdal command line tools within ``gridwxcomp``, currently
    utilizes the `gdal_grid <https://www.gdal.org/gdal_grid.html>`_ 
    command line tool. 
    
    Arguments:
        summary_csv_path (str): path to [var]_summary_comp CSV file created 
            by :mod:`gridwxcomp.calc_bias_ratios` containing point bias ratios,
            lat, and long. 
            
    Attributes:
        CELL_SIZE (float): resolution of gridMET dataset in decimal degrees.
        interp_methods (tuple): gdal_grid interpolation algorithms.
        default_layers (tuple): layers to interpolate created by 
            :mod:`gridwxcomp.calc_bias_ratios`, e.g. "Jan_mean", found in 
            ``summary_csv_path``.
        default_params (dict): dictionary with default parameters for each
            interpolation algorithm, slightly modified from gdal defaults.
            Keys are interpolation method names, keys are dictionaries with
            parameter names keys and corresponding values.
        var_residual_names (dict): dictionary that maps names of bias ratios 
            to the name of their intepolated residual if they are too long for
            storing as a field name in an ESRI shapefile (i.e. > 10 chars).
        summary_csv_path (:obj:`pathlib.Path`): absolute path object to 
            input ``summary_csv_path``.
        layers (list): list of layers in ``summary_csv_path`` to interpolate
            e.g. when using :meth:`InterpGdal.gdal_grid` with ``layer="all"``
            defaults to :attr:`InterpGdal.default_layers`.
        grid_bounds (tuple or None): default None. Extent for interpolation
            raster in order (min long, max long, min lat, max lat).
        interp_meth (str): default 'invdist'. gdal_grid interpolation method.
        interped_rasters (list): empty list that is appended with 
            :obj:`pathlib.Path` objects to interpolated rasters after using
            :meth:`InterpGdal.gdal_grid`.
        params (dict or None): default None. After :meth:`InterpGdal.gdal_grid`
            ``params`` is updated with the last used interpolation parameters
            in the form of a dictionary with parameter names as keys.

    Example:
        The :class:`InterpGdal` class is useful for experimenting with multiple 
        interpolation algorithms provided by gdal which are optimized and
        often sensitive to multiple parameters. We can use the object
        to loop over a range of parameter combinations to test how algorithms
        perform, we might pick a single layer to test, in this case the
        growing season bias ratios between station and gridMET reference
        evapotranspiration (etr_mm). Below is a routine to conduct a
        basic sensitivity analysis of the power and smooth parameters of the 
        inverse distance to a power interpolation method,
        
        >>> from gridwxcomp import InterpGdal
        >>> import os
        >>> # create instance variable from summary csv
        >>> summary_file = 'PATH/TO/etr_mm_summary_comp.csv'
        >>> # create a InterpGdal instance
        >>> test = InterpGdal(summary_file)
        >>> layer = 'growseason_mean' # could be a list
        >>> # run inverse distance interpolation with different params
        >>> for p in range(1,10):
        >>>     for s in [0, 0.5, 1, 1.5, 2]:
        >>>         # build output directory based on parameter sets
        >>>         out_dir = os.path.join('spatial', 'invdist', 
        >>>             'power={}_smooth={}'.format(p, s))
        >>>         params = {'power': p, 'smooth': s}
        >>>         test.gdal_grid(out_dir=out_dir, layer=layer, params=params)

        Note, we did not assign the interpolation method 'invdist' because it 
        is the default. To use another interpolation method we would
        assign the ``interp_meth`` kwarg to :meth:`InterpGdal.gdal_grid`.
        Similarly, we could experiment with other parameters which all can be
        found in the class attribute :attr:`InterpGdal.default_params`. The
        instance variable :attr:`InterpGdal.params` can also be used to save
        metadata on parameters used for each run.
        
    """
    # constant gridMET cell size in degrees
    GRIDMET_RES = 0.041666666666666664
    # gdal_grid interpolation methods
    interp_methods = ('average',
                     'invdist',
                     'invdistnn',
                     'linear',
                     'nearest')
    
    # default layers calculated by calc bias ratios module
    default_layers = ('Jan_mean',
                     'Feb_mean',
                     'Mar_mean',
                     'Apr_mean',
                     'May_mean',
                     'Jun_mean',
                     'Jul_mean',
                     'Aug_mean',
                     'Sep_mean',
                     'Oct_mean',
                     'Nov_mean',
                     'Dec_mean',
                     'growseason_mean',
                     'annual_mean',
                     'summer_mean')
    
    # interp params, method key, param dic as values
    default_params = {
        'invdist':{
            'power': 2,
            'smoothing': 0,
            'radius1': 0,
            'radius2': 0,
            'angle': 0,
            'max_points': 0,
            'min_points': 0,
            'nodata': -999
        },
        'invdistnn':{
            'power': 2,
            'smoothing': 0,
            'radius': 10,
            'max_points': 12,
            'min_points': 0,
            'nodata': -999
        },
        'average':{
            'radius1': 0,
            'radius2': 0,
            'angle': 0,
            'min_points': 0,
            'nodata': -999
        },
        'linear':{
            'radius': -1,
            'nodata': -999
        },
        'nearest':{
            'radius1': 0,
            'radius2': 0,
            'angle': 0,
            'nodata': -999
        }
    }

    # maps bias ratio variables names to residual names for point shapefile
    # which must be shorter (< 11 characters) to be stored as fields
    var_residual_names = {
        'annual_mean': 'annual_res',
        'growseason_mean': 'grow_res',
        'summer_mean': 'summer_res'
    }

    def __init__(self, summary_csv_path):
        
        if not Path(summary_csv_path).is_file():
            raise FileNotFoundError(
                'Summary CSV file: {} not found!'.format(
                    Path(summary_csv_path).absolute())
            )
            
        self.summary_csv_path = Path(summary_csv_path).absolute()
        self.layers = list(self.default_layers) # mutable instance attr.
        self.grid_bounds = None
        self.interp_meth = 'invdist'
        self.interped_rasters = [] # appended with Path objects
        self.params = None # to hold last used interp. parameters as dict
        
        
    def _make_pt_vrt(self, layer_name, out_dir):
        """
        Make a vrt file for station point ratios in summary CSV for a 
        specific layer or field name. Save to out_dir. Used for gdal_grid 
        interpolation commands of scatter point data.
        """
        if not Path(out_dir).is_dir():
            os.makedirs(out_dir)
        
        point_data = Path(self.summary_csv_path).name.replace(
                '.csv', '_tmp.csv')

        # make tmp point data csv for given layer, drop missing values
        df = pd.read_csv(self.summary_csv_path)
        df = df[['STATION_LAT', 'STATION_LON', layer_name]]
        df = df[df[layer_name] != -999]
        tmp_out_path = str(Path(self.summary_csv_path).parent / point_data)
        df.to_csv(tmp_out_path, index=False)

        # if out_dir adjust summary CSV path by prepending parent dirs 
        tmp = copy(Path(out_dir))
        n_parent_dirs = 0
        while len(Path(tmp).parents) > 0:    
            if tmp.name == self.summary_csv_path.parent.name:
                break
            tmp = Path(tmp).parent
            n_parent_dirs+=1
        
        path_to_data = str(
            Path(
                '..{}'.format(os.sep)*n_parent_dirs
            ).joinpath(point_data)
        )
        
        out_file = '{}.vrt'.format(layer_name) # keep it simple just layer name

        # VRT format for reading CSV point data
        root = ET.Element('OGRVRTDataSource')
        OGRVRTLayer = ET.SubElement(root, 'OGRVRTLayer', 
                                    name=point_data.replace('.csv', ''))
        # set all fields, SRS WGS84, point geom
        ET.SubElement(OGRVRTLayer, 'SrcDataSource').text = path_to_data
        ET.SubElement(OGRVRTLayer, 'LayerSRS').text = 'epsg:4326'
        ET.SubElement(OGRVRTLayer, 'GeometryType').text = 'wkbPoint'
        ET.SubElement(OGRVRTLayer, 'GeometryField', encoding='PointFromColumns',
                     x='STATION_LON', y='STATION_LAT', z=layer_name)
        
        tree = ET.ElementTree(root)
        # indent xml, save to out_dir
        out_xml_str = _prettify(root)
        
        out_path = os.path.join(out_dir, out_file)
        with open(out_path, 'w') as outf:
            outf.write(out_xml_str)
        
    def _str_to_params(self, param_str):
        """ 
        Convert parameter string for gdal interpolation arguments
        into a dictionary. 
        
        Example:
        
            >>> in_str = ":power=2:smoothing=.1:nodata=-999"
            >>> _str_to_params(in_str)
                {'power': '2', 'smoothing': '.1', 'nodata': '-999'}
    
        """
        param_tmp = param_str.split(':')
        param_dict = {}
        for pair in param_tmp:
            if pair and pair.count('=') == 1:
                name, val = pair.split('=')[0], pair.split('=')[1]
                param_dict[name] = val
            elif not pair:
                continue
            else:
                raise ValueError('{} is not a valid interpolation argument'\
                        .format(param_str))
        
        return param_dict
    

    def gdal_grid(self, layer='all', out_dir='', interp_meth='invdist', 
                  params=None, bounds=None, nx_cells=None, ny_cells=None, 
                  scale_factor=1, z_stats=True, res_plot=True, grid_res=None,
                  grid_id_name='GRIDMET_ID', options=None):
        """
        Run gdal_grid command line tool to interpolate point ratios.
        
        For further information on theinterpolation algorithms including 
        their function, parameters, and options see 
        `gdal_grid <https://www.gdal.org/gdal_grid.html>`_.
        
        Keyword Arguments:
            layer (str or list): default 'all'. Name of summary file column
                to interpolate, e.g. 'Jan_mean', or list of names. If 'all'
                use all variables in mutable instance attribute "layers".
            out_dir (str): default ''. Output directory to save rasters and
                zonal stats CSV, always appended to the root dir of the
                input summary CSV parent path that contains point ratios.
            interp_meth (str): default 'invdist'. gdal interpolation algorithm
            params (dict, str, or None): default None. Parameters for 
                interpolation algorithm. See examples for format rules.
            bounds (tuple or None): default None. Tuple of bounding coordinates 
                in the following order (min long, max long, min lat, max lat) 
                which need to be in decimal degrees. If None, get extent from 
                locations of climate stations in input summary CSV with 25 cell
                buffer.
            nx_cells (int): default None. Number of pixels in x dim. of raster,
                if None calculated from ``bounds``.
            ny_cells (int): default None. Number of pixels in y dim. of raster,
                if None calculated from ``bounds``.
            scale_factor (float, int): default 1. Scaling factor to apply to 
                original gridMET fishnet to create resampling resolution. If 
                scale_factor = 0.1, the resolution will be one tenth gridMET 
                resolution or 400 m.
            z_stats (bool): default True. Calculate zonal means of 
                interpolated surface to gridMET cells in fishnet and save to a 
                CSV file. The CSV file will be saved to the same directory as 
                the interpolated raster file(s).
            res_plot (bool): default True. Make bar plot for residual (error)
                between interpolated and station value for ``layer``.
            options (str or None): default None. Extra command line options for
                gdal_grid spatial interpolation.
                
        Returns:
            None
                
        Examples:
            The default interpolation algorithm 'invdist' or inverse distance 
            weighting to a power to interpolate bias ratios in a summary CSV 
            file that was first created by :mod:`gridwxcomp.calc_bias_ratios`. 
            The default option will interpolate all layers in :obj:`InterpGdal.default_layers` 
            and calculate zonal statistics for all layers. It will also assume 
            the boundaries of the rasters are defined by the centroid locations 
            of the *outer* station locations in the input summary CSV plus a 25 
            gridMET cell buffer, the pixel size will be 400m (scale_factor=0.1).            We also limit the interpolation to two layers, growing season and 
            annual mean bias ratios,
            
            >>> from gridwxcomp import InterpGdal
            >>> summary_file = 'PATH/TO/[var]_summary_comp.csv'
            >>> out_dir = 'default_params'
            >>> layers = ['growseason_mean', 'annual_mean']
            >>> # create a InterpGdal instance
            >>> test = InterpGdal(summary_file)
            >>> # run inverse distance interpolation
            >>> test.gdal_grid(out_dir=out_dir, layer=layers)
            
            Note, zonal statistics to gridMET cells and interpolated residual 
            plots are computed by default. A gridMET fishnet must have been
            previously created using :func:`gridwxcomp.spatial.make_grid`. 
            
            After running the code above the following files will be created 
            in the 'default_params' directory which will be build in the same 
            location as the input summary CSV::

                default_params/           
                ├── annual_mean.tiff
                ├── annual_mean.vrt
                ├── etr_mm_summary_comp_all_yrs.csv
                ├── etr_mm_summary_pts.cpg
                ├── etr_mm_summary_pts.dbf
                ├── etr_mm_summary_pts.prj
                ├── etr_mm_summary_pts.shp
                ├── etr_mm_summary_pts.shx
                ├── zonal_stats.csv
                ├── growseason_mean.tiff
                ├── growseason_mean.vrt
                └── residual_plots/
                    ├── annual_res.html
                    └── grow_res.html

            GeoTiff interpolated raster files are now created for select layers
            as well as VRT (virtual raster) meta files that store info
            on each raster's data source. The file "gridMET_stats.csv" contains
            gridMET ID as an index and each layer zonal mean as columns. For
            example,
            
                ========== ================== ================== 
                GRIDMET_ID growseason_mean    annual_mean        
                ========== ================== ================== 
                511747     0.9650671287940088 0.9078723876243023 
                510361     0.9658465063428492 0.9097255715561022 
                508975     0.9667075970344162 0.9117676407214926 
                ========== ================== ================== 
                
            There are several :class:`InterpGdal` instance attributes that 
            may be useful, for example to see the parameters that were used 
            for the last call to :meth:`InterpGdal.gdal_grid`
            
            >>> test.params
            {'power': 2,
             'smoothing': 0,
             'radius1': 0,
             'radius2': 0,
             'angle': 0,
             'max_points': 0,
             'min_points': 0,
             'nodata': -999}
                 
            Or to find the paths to the interpolated raster files that
            have been created by the instance (all), the "interped_rasters"
            instance attribute is a list of all :obj:`pathlib.Path` objects
            of absolute paths of raster files. To get them as strings,
            
            >>> list(map(str, test.interped_rasters))
            ['PATH/TO/growseason_mean.tiff',
             'PATH/TO/annual_mean.tiff']
             
            Similary, the raster extent that was used and will be used again for
            any subsequent calls of :meth:`InterpGdal.gdal_grid` can be 
            retrieved by
             
            >>> test.grid_bounds 
            (-111.74583329966664,
             -108.74583330033335,
             38.21250000003333,
             40.462499999966674)
             
        Note:
            The ``nx_cells`` and ``ny_cells`` arguments are an option for 
            defining the output raster's resolution. If these arguments are 
            passed then the ``scale_factor`` argument has no effect. The latter
            assumes raster resolution is relative to gridMET (4 km). 
            
        Raises:
            KeyError: if interp_meth is not a valid gdal_grid interpolation
                algorithm name. 
        """
        
        cwd = os.getcwd()
        
        # user provided uniform grid, cell size should be in dec. degrees
        if grid_res is not None:
            CS = grid_res
        else: # assume gridMET
            CS = self.GRIDMET_RES
        self.grid_res = CS
        
        # grid resolution in decimal degrees
        res = scale_factor * CS
        # file structure to match gridwxcomp.spatial.interpolate
        grid_var = str(self.summary_csv_path).split('_summary')[0]
        
        # out_dir as subdir from dir with summary CSV 
        out_dir = (Path(self.summary_csv_path).parent/Path(out_dir)).resolve()

        if not out_dir.is_dir():
            print('{}\nDoes not exist, creating directory'.format(str(out_dir)))
            out_dir.mkdir(parents=True, exist_ok=True)
    
        source_file = Path(self.summary_csv_path).name
        source = source_file.replace('.csv', '_tmp')
        
        if interp_meth not in InterpGdal.interp_methods:
            err_msg = '{} not a valid interpolation method'.format(interp_meth)
            raise KeyError(err_msg)
        self.interp_meth = interp_meth
            
        # look up default parameters for interpolation method
        if not params:
            params = InterpGdal.default_params.get(self.interp_meth)
        # if run from command line, params is string to be parsed
        if isinstance(params, str):
            params = self._str_to_params(params)
        # avoid zero NA values for zonal_stats, set default NA rep to -999
        if not params.get('nodata'):
            params['nodata'] = -999
        # update instance parameters for later reference
        self.params = params
        # parameters to command line input str :name=value:name=value ...
        param_str = ':'+':'.join('{}={}'.format(key,val) 
                                 for (key,val) in params.items()) 
        # get boundary info and update instance attribute
        if not bounds and not self.grid_bounds:
            # use gridwxcomp.spatial function, assume 25 cell buffer
            self.grid_bounds = get_subgrid_bounds(self.summary_csv_path, 
                buffer=25, grid_res=CS)
        elif bounds:
            self.grid_bounds = bounds
        # raster extent
        xmin,xmax,ymin,ymax = self.grid_bounds

        # if not given get pixels in lon lat 
        # add one cell to avoid unfilled extent in case of large upscaling
        if not nx_cells:
            nx_cells = int(np.abs(xmin - xmax) / \
                    (CS * scale_factor)) + 1
        if not ny_cells:
            ny_cells = int(np.abs(ymin - ymax) / \
                    (CS * scale_factor)) + 1
        # fix any minor adjustments to make raster fit gridMET fishnet extent
        # if scale_factor=1 make sure raster pixels align exactly w/gridcells
        xmax = xmin + nx_cells * CS * scale_factor
        ymin = ymax - ny_cells * CS * scale_factor

        # to parse options, like --config GDAL_NUM_THREADS update here
        if not options:
            options = ''
                
        def _run_gdal_grid(layer):
            """reuse if running multiple layers"""
            existing_layers = pd.read_csv(self.summary_csv_path).columns
            if not layer in existing_layers:
                print('\nError: {} does not exist in input CSV:\n {}'.format(
                   layer, self.summary_csv_path),
                     '\nSkipping interpolation.'
               )
                return
            
            # move to out_dir to run gdal command
            os.chdir(out_dir)
            # build vrt files in out_dir 
            self._make_pt_vrt(layer, out_dir)
            
            vrt_file = '{}.vrt'.format(layer)
            tiff_file = '{}.tiff'.format(layer)
            # add raster path to instance if not already there (overwritten)
            out_file = out_dir.joinpath(tiff_file)
            # print message to console/logging about interpolation
            grid_var = Path(self.summary_csv_path).name.split('_summ')[0]
            _interp_msg(grid_var, layer, self.interp_meth, res, out_file)
            # build command line arguments
            cmd = (r'gdal_grid -a {meth}{p} -txe {xmin} {xmax} -tye {ymax}' 
                  ' {ymin} -outsize {nx} {ny} -of GTiff -ot Float32 -l {source}'
                  ' {vrt} {out} {options}'.format(meth=interp_meth, p=param_str,
                      xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, nx=nx_cells, 
                      ny=ny_cells, source=source, vrt=vrt_file, out=tiff_file, 
                      options=options))
            # run gdal_grid with arguments, x-platform
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            out, err = p.communicate()
            if err:
                print(err)
            else:
                if not out_file in self.interped_rasters:
                    self.interped_rasters.append(out_file)

            p.stdout.close()
            p.stderr.close()    
         
            os.chdir(cwd)

            # calculate interpolated values and error at stations
            # only calc residuals for mean bias ratios, i.e. not std dev, etc.
            if layer in InterpGdal.default_layers:
                calc_pt_error(self.summary_csv_path, out_dir, layer, grid_var,
                    grid_id_name=grid_id_name
                )
            else:
                # delete tmp summary csv used in interpgdal _make_pt_vrt method 
                # normally deleted in calc_pt_error
                tmp_csv = str(self.summary_csv_path).replace('.csv','_tmp.csv')
                if Path(tmp_csv).resolve().is_file():
                    Path(tmp_csv).resolve().unlink()

            # zonal means extracted to GRIDMET_ID (cell index) 
            if z_stats:
                zonal_stats(self.summary_csv_path, out_file,
                    grid_id_name=grid_id_name
                )
            # residual (error) bar plot, only for mean bias ratios
            if res_plot and layer in InterpGdal.default_layers:
                layer = self.var_residual_names.get(
                    layer, 
                    layer.replace('mean','res')
                )
                y_label = 'residual (interpolated minus station value)'
                title = 'layer: {} algorithm: {} (gdal_grid) res: {} deg.'.\
                        format(layer, self.interp_meth, res)
                res_plot_dir = Path(out_dir)/'residual_plots'
                subtitle = 'parameters: {}'.format(params)
                source_file =  Path(out_dir)/Path(self.summary_csv_path).name

                station_bar_plot(source_file, layer, out_dir=res_plot_dir,
                    y_label=y_label, title=title, subtitle=subtitle)

            
        # run interpolation and zonal statistics depending on layer kwarg
        if layer == 'all': # potential for multiprocessing 
            for l in self.layers:
                _run_gdal_grid(l)
        # run single field
        elif isinstance(layer, str):
            _run_gdal_grid(layer)
        # run select list or tuple of layers
        elif isinstance(layer, (list, tuple)):
            for l in layer:
                _run_gdal_grid(l)
                
                
def _prettify(elem):
    """
    Return an indented, multiline XML string for a XML element tree.
    """
    rough_string = ET.tostring(elem, 'utf-8', method='xml')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent='  ')

def _interp_msg(grid_var, layer, function, res, out_file):
    print(
        '\nInterpolating {g} point bias ratios for: {t}\n'.\
            format(g=grid_var, t=layer),
        'Using the "{}" method\n'.format(function),
        'Resolution (pixel size) of output raster: {} degrees'.format(res)
    )
    print(
        'GeoTIFF raster will be saved to: \n',
        os.path.abspath(out_file)
    )
