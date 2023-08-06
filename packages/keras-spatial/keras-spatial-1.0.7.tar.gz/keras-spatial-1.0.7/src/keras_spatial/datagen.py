#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import collections
import rasterio
from rasterio.vrt import WarpedVRT
from rasterio.warp import Resampling
import geopandas as gpd
import numpy as np

import keras_spatial.grid as grid

import logging
log = logging.getLogger(__name__)

class SpatialDataGenerator(object):

    def __init__(self, source=None, indexes=None, 
            width=0, height=0, batch_size=32,
            crs=None, interleave='band', resampling=Resampling.nearest,
            preprocess=None):
        """

        Args:
          source (str): raster file path
          width (int): sample width in pixels
          height (int): sample height in pixels
          indexes (int|[int]): raster file band (int) or bands ([int,...])
                  (default=None for all bands)
          crs (CRS): produces patches in different crs
          resampling (int): interpolation method used when resampling
          interleave (str): type of interleave, 'pixel' or 'band'
          preprocess (tuple(str, func, list, dict) | list(tuples)): one or
                   more callbacks to each sample during batch creation
        """

        self.src = None
        if source: 
            self.source = source
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

    def _close(self):
        if self.src:
            self.src.close()
            self.src = None

    @property
    def extent(self):
        if self.src:
            return tuple(self.src.bounds)
        else:
            return None

    @property
    def profile(self):
        """Return dict of parameters that are likely to re-used."""

        return dict(width=self.width, height=self.height, crs=self.crs, 
                interleave=self.interleave, resampling=self.resampling)

    @profile.setter
    def profile(self, profile):
        """Set parameters from profile dictionary."""

        self.width = profile['width']
        self.height = profile['height']
        self.crs = profile['crs']
        self.interleave = profile['interleave']
        self.resampling = profile['resampling']

    @property
    def crs(self):
        if self._crs:
            return self._crs
        elif self.src:
            return self.src.crs
        else:
            return None

    @crs.setter
    def crs(self, crs):
        self._crs = crs

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, source):
        """Save and open the source string

        Args:
          source (str): local file path or URL using dap
        """

        self._close()
        self._source = source

        self.src = rasterio.open(source)

        idx = getattr(self, 'indexes', None)
        if idx is None or idx == -1:
            self.indexes = list(range(1, self.src.count+1))

    def regular_grid(self, width, height, overlap=0.0, units='native'):
        """Create a dataframe that defines the a regular grid of samples.

        When units='native', width and height are given in projection
        units (i.e. meters, feet, etc). The number of pixels within this
        area would depend on the pixel size. If units='pixel', width
        and height are multiplied by the pixel size to compute the
        sample boundaries.

        Note: width and height are unrelated to the DL model inputs.

        Args:
          width (int): sample size 
          height (int): sample size
          units (str): units applied to sample sizes ('native' or 'pixels')
          overlap (float): percentage overlap (default=0.0)

        Returns:
          (GeoDataframe)
        """

        if not self.src:
            raise RuntimeError('source not set or failed to open')

        if units == 'pixels':
            dims = width * self.src.res[0], height * self.src.res[1]
        elif units == 'native':
            dims = width, height
        else:
            raise ValueError('units must be "native" or "pixels"')

        gdf = grid.regular_grid(*self.src.bounds, *dims, overlap=overlap)
        gdf.crs = self.src.crs
        return gdf

    def random_grid(self, width, height, count, units='native'):
        """Create a dataframe that defines a random set of samples.

        When units='native', width and height are given in projection
        units (i.e. meters, feet, etc). The number of pixels within this
        area would depend on the pixel size. If units='pixel', width
        and height are multiplied by the pixel size to compute the
        sample boundaries.

        Note: width and height are unrelated to the DL model inputs.

        Args:
          width (int): sample size in pixels
          height (int): sample size in pixels
          units (str): units applied to sample sizes ('native' or 'pixels')
          count (int): number of samples

        Returns:
          (GeoDataframe)
        """

        if not self.src:
            raise RuntimeError('source not set or failed to open')

        if units == 'pixels':
            dims = width * self.src.res[0], height * self.src.res[1]
        elif units == 'native':
            dims = width, height
        else:
            raise ValueError('units must be "native" or "pixels"')

        gdf = grid.random_grid(*self.src.bounds, *dims, count)
        gdf.crs = self.src.crs
        return gdf

    def get_batch(self, src, geometries):
        """Get batch of patches from source raster

        Args:
          src (rasterio): data source opened with rasterio
          geometries (GeoSeries): boundaries to extract from raster

        Returns:
          (numpy array)

        This leverages rasterio's virtual warping to normalize data to
        a consistent grid.
        """

        batch = []
        for bounds in geometries.bounds.itertuples():
            bot, left = src.index(bounds[1], bounds[2])
            top, right = src.index(bounds[3], bounds[4])
            window = rasterio.windows.Window(left, top, right-left, bot-top)
            batch.append(src.read(indexes=self.indexes, window=window))

            # single band reads return a 2d array, expand to 3d
            if self.interleave == 'band' and len(batch[-1].shape) == 2:
                batch[-1] = np.expand_dims(batch[-1], axis=0)

            # pixel interleave with multiple bands move axis
            if self.interleave == 'pixel' and batch[-1].shape[0] > 1:
                batch[-1] = np.moveaxis(batch[-1], 0, -1)

            for func,args,kwargs in self.preprocess.values():
                batch[-1] = func(batch[-1], *args, **kwargs)

        return np.stack(batch)

    def flow_from_dataframe(self, dataframe, width=0, height=0, batch_size=0):
        """extracts data from source based on sample extents

        Args:
          dataframe (geodataframe): dataframe with spatial extents
          width (int): array width
          height (int): array height
          batch_size (int): batch size to process

        Returns:
          Iterator[ndarray]
        """

        width = width if width else self.width
        height = height if height else self.height
        if width < 1 or height < 1:
            raise ValueError('desired sample size must be set')
        batch_size = batch_size if batch_size else self.batch_size
        if batch_size < 1:
            raise ValueError('batch size must be specified')

        # TODO should reprojection be handled here or externally?
        # TODO Is there equivelancy check for projections?
        #df = dataframe.to_crs(self.crs) if self.crs else dataframe
        df = dataframe

        # TODO this finds the average sample area and computes the desired
        #  resolution based on it and sample size. Probably not what is
        #  needed. Assume uniform sized samples for now.
        # TODO the apply seems VERY slow but other options seem slower
        #  including, oddly, the vectorized version
        #  i.e. xres = (df.bounds.maxx - df.bounds.minx).mean() / width
        #xres = df.bounds.apply(lambda row: row.maxx - row.minx, 
        #        axis=1).mean() / width
        #yres = df.bounds.apply(lambda row: row.maxy - row.miny, 
        #        axis=1).mean() / height
        #xres = (df.bounds.iloc[0].maxx - df.bounds.iloc[0].minx) / width
        #yres = (df.bounds.iloc[0].maxy - df.bounds.iloc[0].miny) / height
        minx, miny, maxx, maxy = df.iloc[0].geometry.bounds
        xres, yres = (maxx - minx) / width, (maxy - miny) / height

        minx, miny, maxx, maxy = df.total_bounds
        width = (maxx - minx) / xres
        height = (maxy - miny) / yres
        transform = rasterio.transform.from_origin(minx, maxy, xres, yres)

        # use VRT to ensure correct projection and size
        vrt = WarpedVRT(self.src, crs=df.crs, 
                width=width, height=height,
                transform=transform,
                resampling=self.resampling)

        for i in range(0, len(df), batch_size):
            yield self.get_batch(vrt, df.iloc[i:i+batch_size]['geometry'])

        vrt.close()

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

