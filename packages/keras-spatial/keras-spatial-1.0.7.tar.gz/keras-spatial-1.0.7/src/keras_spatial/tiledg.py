#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections
from functools import lru_cache
import rasterio
from rasterio.vrt import WarpedVRT
from rasterio.warp import Resampling
from rasterio.windows import Window
import geopandas as gpd
import numpy as np

import keras_spatial.grid as grid

import logging
log = logging.getLogger(__name__)

class TileDataGenerator(object):

    def __init__(self, tindex, tilesrc='TILE',
            indexes=None, width=0, height=0, batch_size=32,
            crs=None, interleave='pixel', resampling=Resampling.nearest,
            preprocess=None):
        """

        Args:
          tindex (GeoDataFrame): tile index
          tilesrc (str): field name with tile URL

          indexes (int|[int,]): raster file band (int) or bands ([int,...])
                  (default=None for all bands)
          width (int): sample width in pixels
          height (int): sample height in pixels
          crs (CRS): produces patches in different crs
          resampling (int): interpolation method used when resampling
          interleave (str): type of interleave, 'pixel' or 'band'
          preprocess (tuple(str, func, list, dict) | list(tuples)): one or
                   more callbacks to each sample during batch creation
        """


        if isinstance(tindex, gpd.GeoDataFrame):
            self._source = None
            self.tindex = tindex
        else:
            self._source = tindex
            self.tindex = gpd.read_file(tindex)

        if indexes is not None:
            self.indexes = indexes
        self.width = width
        self.height = height
        self.batch_size = batch_size
        self.crs=crs
        self.resampling = resampling
        self.interleave = interleave

        self.preprocess = collections.OrderedDict()
        if preprocess and isinstance(preprocess[0], str):
            self.preprocess[preprocess[0]] = preprocess[1:]
        elif preprocess:
            for cb in preprocess:
                self.preprocess[cb[0]] = cb[1:]

    @property
    def extent(self):
        return tuple(self.tindex.total_bounds)

    @property
    def crs(self):
        return self.tindex.crs

    @property
    def source(self):
        return self._source

    @property
    def pixel_res(self):
        """Return pixel resolution based on sample size, width, height

        This is an odd way to calculate the resolution because it uses
        only the first sample. 
        
        Args:
          samples (GeoDataFrame): sample dataframe 
          width (int): target sample width
          height (int): target sample height

        Returns:
          (tuple(int, int)): resx, resy
        """
        minx, miny, maxx, maxy = self._samples.iloc[0].geometry.bounds 
        return ((maxx - minx) / self._width, (maxy - miny) / self._height)

    @property
    def transform(self):
        """Return transform for  
        """
        resx, resy = self.pixel_res

        minx, miny, maxx, maxy = self._samples.total_bounds
        width, height = (maxx - minx) / xres, (maxy - miny) / yres
        return rasterio.transform.form_origin(minx, maxy, resx, resy)

    def find_intersecting_tiles(self, samples):
        """Creates a list of each tile that intersects each sample
        
        Args:
          samples (GeoDataFrame): sample boundaries

        Returns:
          (list of lists): list of intersecting tiles for each sample
        """

        projected = samples.to_crs(self.crs)
        return [list(self.tindex[self.tindex.geometry.intersects(s.geometry)] \
                [self.tilename]) for s in projected.itertuples()]

    @lru_cache(maxsize=64)
    def open_tile(self, source):
        """Open raster dataset and setup a WarpedVRT for transformation

        Args:
        """

        src = rio.open(source)

        # use VRT to ensure correct projection and size
        vrt = WarpedVRT(src, crs=self.crs, 
                width=self.width, height=self.height,
                transform=self.transform, resampling=self.resampling)

        return vrt

    def read_sample(minx, maxy, width, height):

        src = open_tile()


    def 



    def get_batch(self, geometries):
        """Get batch of samples from source raster

        Args:
          geometries (GeoSeries): boundaries to extract from raster

        Returns:
          (numpy array)

        This leverages rasterio's virtual warping to normalize data to
        a consistent grid.
        """

        batch = []
        for bounds in geometries.bounds.itertuples():
            bbox = box(bounds.minx, bounds.miny, bounds.maxx, bounds.maxy)
            batch[-1] = np.zero(shape=(self.width, self.height))
            tiles = self._tindex[self._tindex.geometry.intersects(bbox)]
            for t in tiles:
                src = self.open_tile(t.location)
                top, left = src.index(bounds.minx, bounds.maxy)
                frag = src.read(indexes=self.indexes, 
                        window=Window(left, top, self.width, self.height),
                        masked=True, boundless=True))

            if self.interleave == 'pixel' and len(batch[-1].shape) == 3:
                batch[-1] = np.moveaxis(batch[-1], 0, -1)

            for func,args,kwargs in self.preprocess.values():
                batch[-1] = func(batch[-1], *args, **kwargs)

        return np.stack(batch)


    def flow_from_dataframe(self, samples, width=0, height=0, batch_size=0):
        """extracts data from source based on sample extents

        Args:
          dataframe (GeoDataFrame): dataframe with sample boundaries
          width (int): sample width in units, replaces instance width var
          height (int): sample height in units, replaces instance height var
          batch_size (int): batch size to process

        Returns:
          Iterator[ndarray]
        """

        if width and height:
            self.width, self.height = width, height

        batch_size = batch_size if batch_size else self.batch_size
        if batch_size < 1:
            raise ValueError('batch size must be specified')

        self._samples = samples

        for i in range(0, len(self._samples), batch_size):
            yield self.get_batch(self._samples.iloc[i:i+batch_size]['geometry'])


    def add_preprocess_callback(self, name, func, *args, **kwargs):
        """add a callback function that is applied to every sample array

        The callback function will be invoked on every sample array
        during the during the generation process. The sample array
        will be the first argument passed. Additional arguments
        (args, kwargs) are optional. The callback can alter the
        sample in any way and care must be taken maintain the 
        compatiblity of the results will be merged with other
        SDGs.

        ndarray = func(ndarray, *args, **kwargs)

        Args:
          name (str): name of the callback
          func (function): function to be called
          args (list): arguments to be passed to the callback
          kwargs (dict): keyword arguments to be passed to callback
        """

        self.preprocess[name] = (func, args, kwargs)

    def del_preprocess_callback(self, name):
        """remove a callback function from processing list

        Args:
          name (str): name of callback to be removed
        """

        del self.preprocess[name]

