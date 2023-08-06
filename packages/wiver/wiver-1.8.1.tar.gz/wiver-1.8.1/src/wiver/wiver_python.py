# -*- coding: utf-8 -*-

import multiprocessing
import os
import logging
from collections import defaultdict
from typing import Dict
import numpy as np
import pandas as pd
import xarray as xr

from cythoninstallhelpers.configure_logger import get_logger
from cythonarrays.array_properties import _ArrayProperties
from matrixconverters.save_ptv import SavePTV
from matrixconverters.xarray2netcdf import xr2netcdf
import pyximport; pyximport.install()
from wiver.wiver_cython import (_WIVER,
                                DestinationChoiceError,
                                DataConsistencyError)

np.seterr(divide='ignore', invalid='ignore')


class InvalidWiverInputData(ValueError):
    """Invalid input data for Wiver model"""


class WIVER(_WIVER, _ArrayProperties):
    """WIVER Business Trip Model"""
    _coordinates = {'n_groups': 'groups',
                    'n_modes': 'modes',
                    'n_zones': 'zone_name',
                    'n_time_slices': 'lbl_time_slice',
                    'n_sectors': 'sector_short',
                    }

    def __init__(self,
                 n_groups: int,
                 n_zones: int,
                 n_time_slices: int=5,
                 n_modes: int=4,
                 n_sectors: int=2,
                 n_threads: int=None,
                 logger: logging.Logger=None):
        """
        Parameters
        ----------
        n_groups:
            the number of groups
        n_zones:
            the number of zones
        n_time_slices:
            the number of time slices
        n_modes:
            the number of transport modes
        n_sectors:
            the number of economic sectors
        n_threads:
            the maximum number of threads to use for calculation
        logger:
            an optional logger to use from within wiver. If not provided,
            a logger is created
        """
        super().__init__()

        self.logger = logger or get_logger(self)

        self.n_modes = n_modes
        self.n_groups = n_groups
        self.n_zones = n_zones
        self.n_sectors = n_sectors
        self.n_time_slices = n_time_slices
        self.set_n_threads(n_threads=n_threads)

        self.define_arrays()
        self.init_arrays()

    def set_n_threads(self, n_threads: int=None):
        """
        Set the number of threads

        Parameters
        ----------
        n_threads:
            the maximum number of threads to use for calculation
        """
        if n_threads:
            n_threads = min(n_threads, multiprocessing.cpu_count())
        else:
            n_threads = multiprocessing.cpu_count()
        self.n_threads = min(n_threads, self.n_groups)

    @classmethod
    def read_from_netcdf(cls,
                         files: Dict[str, str],
                         n_threads: int=None) -> 'WIVER':
        """
        Read a Wiver Model
        from a set of netcdf-Filename defined in files

        Parameters
        ----------
        files:
            dict with the file names of the input data
        n_threads:
            the maximum number of threads to use for calculation
        """
        # create instance of self
        self = cls(n_groups=0, n_zones=0, n_threads=n_threads)
        # add datasets
        self.read_all_data(files)
        self.data = xr.merge((self.params, self.matrices, self.zonal_data,
                              self.balancing))

        # set the dimensions
        dims = self.data.dims
        self.n_zones = dims['origins']
        self.n_groups = dims['groups']
        self.n_modes = dims['modes']
        self.n_time_slices = dims['time_slices']
        self.set_n_threads()

        # resize the arrays to the right dimensions
        self.init_arrays()

        self.set_arrays_from_dataset()

        return self

    def set_arrays_from_dataset(self):
        """Sets the arrays with values from the dataset"""
        ds = self.data

        # params
        self.modes = ds.modes.data
        self.groups = ds.groups.data
        self.mode_g = ds.mode_of_groups.data

        self.n_sectors = len(ds.sector_short)

        self.sector_g = ds.sector_of_groups.data
        self.mode_name = ds.mode_name.data
        self.sector_short = ds.sector_short.data
        self.param_dist_g = ds.param_dist.data
        self.savings_param_g = ds.savings_param.data
        self.tour_rates_g = ds.tour_rates.data
        self.stops_per_tour_g = ds.stops_per_tour.data
        self.time_series_starting_trips_gs = ds.time_series_starting_trips.data
        self.time_series_linking_trips_gs = ds.time_series_linking_trips.data
        self.time_series_ending_trips_gs = ds.time_series_ending_trips.data

        # zonal data
        self.source_potential_gh = ds.source_potential.data
        self.sink_potential_gj = ds.sink_potential.data
        self.zone_no = ds.zone_no.data
        self.zone_name = ds.zone_name.data

        # matrices
        self.travel_time_mij = ds.travel_time.data
        self.km_ij = ds.distance_matrix.data

        self.set_arrays_from_balancing_ds(ds)

        # results
        self.results = self.define_results()

    def set_arrays_from_balancing_ds(self, ds: xr.Dataset):
        """
        Set arrays from balancing dataset

        Parameters
        ----------
        ds:
            Dataset with the balancing factors
        """
        # balancing factors
        self.balancing_factor_gj = ds.balancing_factor.data
        self.trips_to_destination_gj = ds.trips_to_destination.data

    def define_arrays(self):
        """Define the arrays"""
        self.init_object_array('groups', 'n_groups')
        self.init_object_array('group_names', 'n_groups')
        self.init_object_array('modes', 'n_modes')
        self.init_object_array('mode_name', 'n_modes')
        self.init_object_array('sector_short', 'n_sectors')
        self.init_object_array('sectors', 'n_sectors')
        self.init_array('zone_no', 'n_zones')
        self.init_object_array('zone_name', 'n_zones')
        self.init_object_array('lbl_time_slice', 'n_time_slices')

        self.init_array('mode_g', 'n_groups', 0)
        self.init_array('sector_g', 'n_groups', 0)
        self.init_array('active_g', 'n_groups', 1)
        self.init_array('converged_g', 'n_groups', 0)

        self.init_array('savings_param_g', 'n_groups', 1.1)

        self.init_array('km_ij', 'n_zones, n_zones')
        self.init_array('travel_time_mij', 'n_modes, n_zones, n_zones')
        self.init_array('mean_distance_g', 'n_groups')
        self.init_array('mean_distance_m', 'n_modes')
        self.init_array('param_dist_g', 'n_groups', -0.1)
        self.init_array('tour_rates_g', 'n_groups', 1)
        self.init_array('stops_per_tour_g', 'n_groups', 2)

        self.init_array('source_potential_gh', 'n_groups, n_zones')
        self.init_array('sink_potential_gj', 'n_groups, n_zones')
        self.init_array('balancing_factor_gj', 'n_groups, n_zones', 1)
        self.init_array('trips_to_destination_gj', 'n_groups, n_zones', 0)

        self.init_array('trips_gij', 'n_groups, n_zones, n_zones', 0)
        self.init_array('home_based_trips_gij',
                        'n_groups, n_zones, n_zones', 0)
        self.init_array('linking_trips_gij', 'n_groups, n_zones, n_zones', 0)
        self.init_array('return_trips_gij', 'n_groups, n_zones, n_zones', 0)
        self.init_array('p_destination_tj', 'n_threads, n_zones', 0)
        self.init_array('p_links_tij', 'n_threads, n_zones, n_zones', 0)

        self.init_array('trips_gsij',
                        'n_groups, n_time_slices, n_zones, n_zones', 0)

        self.init_array('trips_mij',
                        'n_modes, n_zones, n_zones', 0)
        self.init_array('trips_msij',
                        'n_modes, n_time_slices, n_zones, n_zones', 0)

        self.init_array('time_series_starting_trips_gs',
                        'n_groups, n_time_slices', 1)
        self.init_array('time_series_linking_trips_gs',
                        'n_groups, n_time_slices', 1)
        self.init_array('time_series_ending_trips_gs',
                        'n_groups, n_time_slices', 1)

    def validate_input_data(self):
        """make checks on the input data"""
        if (self.stops_per_tour_g < 1).any():
            raise InvalidWiverInputData('Stops per Tour < 1.0 are not allowed')

    def define_datasets(self):
        """Define the datasets"""
        self.params = self.define_params()
        self.matrices = self.define_matrices()
        self.zonal_data = self.define_zonal_data()
        self.balancing = self.define_balancing()
        self.results = self.define_results()

    def define_params(self) -> xr.Dataset:
        """
        Define the params and return them as dataset
        """
        ds = xr.Dataset()
        ds['modes'] = self.modes
        ds['mode_name'] = (('modes'), self.mode_name)
        ds['groups'] = self.groups
        ds['mode_of_groups'] = (('groups'),
                                self.mode_g)
        ds['sector_of_groups'] = (('groups'),
                                    self.sector_g)
        ds['sectors'] = (('sectors'),
                         self.sectors)
        ds['sector_short'] = (('sectors'), self.sector_short)

        # assign group names
        for g in range(self.n_groups):
            self.group_names[g] = '{}_{}'.format(
                self.mode_name[self.mode_g[g]],
                self.sector_short[self.sector_g[g]])

        ds['group_names'] = (('groups'), self.group_names)

        ds['param_dist'] = (('groups'),
                            self.param_dist_g)
        ds['savings_param'] = (('groups'),
                              self.savings_param_g)
        ds['tour_rates'] = (('groups'),
                            self.tour_rates_g)
        ds['stops_per_tour'] = (('groups'),
                                self.stops_per_tour_g)
        ds['time_series_starting_trips'] = (
            ('groups', 'time_slices'), self.time_series_starting_trips_gs)
        ds['time_series_linking_trips'] = (
            ('groups', 'time_slices'), self.time_series_linking_trips_gs)
        ds['time_series_ending_trips'] = (
            ('groups', 'time_slices'), self.time_series_ending_trips_gs)
        return ds

    def define_balancing(self) -> xr.Dataset:
        """Define the balancing factors and return them as dataset"""
        ds = xr.Dataset()
        ds['balancing_factor'] = (('groups', 'destinations'),
                                    self.balancing_factor_gj)
        ds['trips_to_destination'] = (('groups', 'destinations'),
                                      self.trips_to_destination_gj)
        return ds

    def define_zonal_data(self) -> xr.Dataset:
        """Define the zonal data and return them as dataset"""
        ds = xr.Dataset()
        ds['groups'] = self.groups
        ds['zone_no'] = self.zone_no
        ds['zone_name'] = (('zone_no'), self.zone_name)
        ds['origins'] = self.zone_no
        ds['destinations'] = self.zone_no
        ds['source_potential'] = (('groups', 'origins'),
                                  self.source_potential_gh)
        ds['sink_potential'] = (('groups', 'destinations'),
                                self.sink_potential_gj)
        return ds

    def define_matrices(self) -> xr.Dataset:
        """Define the matrices and return them as dataset"""
        ds = xr.Dataset()
        ds['modes'] = self.modes
        ds['origins'] = self.zone_no
        ds['destinations'] = self.zone_no
        ds['zone_no'] = self.zone_no
        ds['zone_name'] = (('zone_no'), self.zone_name)
        ds['travel_time'] = (('modes', 'origins', 'destinations'),
                             self.travel_time_mij)
        ds['distance_matrix'] = (('origins', 'destinations'),
                                 self.km_ij)

        return ds

    def define_results(self) -> xr.Dataset:
        """Define the results and return them as dataset"""
        ds = xr.Dataset()
        # resulting arrays
        ds['modes'] = self.modes
        ds['groups'] = self.groups
        ds['origins'] = self.zone_no
        ds['destinations'] = self.zone_no
        ds['zone_no'] = self.zone_no
        ds['zone_name'] = (('zone_no'), self.zone_name)
        ds['trips_gij'] = (('groups', 'origins', 'destinations'),
                           self.trips_gij)
        ds['trips_gsij'] = (('groups', 'time_slices',
                             'origins', 'destinations'),
                            self.trips_gsij)
        ds['trips_mij'] = (('modes', 'origins', 'destinations'),
                           self.trips_mij)
        ds['trips_msij'] = (('modes', 'time_slices',
                             'origins', 'destinations'),
                            self.trips_msij)
        ds['mean_distance_groups'] = (('groups',),
                                      self.mean_distance_g)
        ds['mean_distance_modes'] = (('modes',),
                                     self.mean_distance_m)

        return ds

    def merge_datasets(self):
        """Merge the datasets"""
        self.data = xr.merge((self.params, self.zonal_data,
                              self.matrices, self.balancing,
                              self.results))

    def save_all_data(self, wiver_files: Dict[str, str]):
        """
        Save Dataset to netcdf-files

        Parameters
        ----------
        wiver_files:
            dict with the input and output filenames
        """
        datasets = ('params', 'zonal_data', 'matrices',
                    'balancing', 'results')
        for dataset_name in datasets:
            fn = wiver_files[dataset_name]
            self.save_data(dataset_name, fn)

    def save_data(self, dataset_name: str, fn: str):
        """
        Save Dataset to netcdf-file

        Parameters
        ----------
        dataset_name:
            the dataset that should be saved
        fn:
            filename to write to
        """
        ds = getattr(self, dataset_name)
        self.logger.info('write {}'.format(fn))
        dirname = os.path.dirname(fn)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        xr2netcdf(ds, fn)
        ds.close()

    def read_all_data(self, datasets: Dict[str, str]):
        """
        Read Datasets from netcdf-file

        Parameters
        ----------
        datasets:
            dict with the filenames of the input and output data
        """
        for dataset_name in ('params', 'matrices', 'zonal_data' ,
                             'balancing'):
            fn = datasets[dataset_name]
            self.read_data(dataset_name, fn)

    def read_data(self, dataset_name: str, fn: str):
        """
        read single dataset from file

        Parameters
        ----------
        dataset_name:
            the dataset that should be read
        fn:
            filename to read from
        """
        self.logger.info('read {}'.format(fn))
        ds = xr.open_dataset(fn).load()
        ds.close()
        setattr(self, dataset_name, ds)

    def save_results(self, wiver_files: Dict[str, str]):
        """
        Save results except trips_gsij to folder

        Parameters
        ----------
        wiver_files:
            dict with the filenames of the input and output data
        """
        del self.results['trips_gsij']
        dataset_name = 'results'
        fn = wiver_files[dataset_name]
        self.save_data(dataset_name, fn)
        dataset_name = 'balancing'
        fn = wiver_files[dataset_name]
        self.save_data(dataset_name, fn)

    def save_results_to_visum(self, folder: str, visum_format: str='BK'):
        """
        Save the results to VISUM-Format

        Parameters
        ----------
        folder:
            the folder where the Visum-Matrices will be written
        visum_format:
            the Visum-Matrix format (Default=Binary Compressed (BK))
        """
        for m, mode in enumerate(self.modes):
            visum_ds = xr.Dataset()
            visum_ds['matrix'] = self.results.trips_mij[m]
            visum_ds['zone_no'] = self.zone_no
            visum_ds['zone_name'] = self.zone_name
            #visum_ds['zone_names2'] = self.zone_name
            s = SavePTV(visum_ds)
            file_name = os.path.join(
                folder, '{m}.mtx'.format(m=mode))
            self.logger.info('save matrix for mode {m} to {f}'.format(
                m=mode, f=file_name
            ))
            s.savePTVMatrix(file_name, file_type=visum_format)

    def save_detailed_results_to_visum(self,
                                       folder: str,
                                       visum_format: str='BK'):
        """
        Save the detailed results to VISUM-Format including the matrices for each group

        Parameters
        ----------
        folder:
            the folder where the Visum-Matrices will be written
        visum_format:
            the Visum-Matrix format (Default=Binary Compressed (BK))
        """
        sectors = defaultdict(list)
        for g, group in enumerate(self.groups):
            if self.active_g[g]:
                sector_id = self.sector_g[g]
                sectors[sector_id].append(g)
        self.logger.info('sectors: {}'.format(sectors))
        for sector_id, sector_groups in sectors.items():
            self.logger.info('sector_id: {}, groups: {}'.format(sector_id,
                                                                sector_groups))
            sector = self.params.sectors.data[sector_id]
            name = self.params.sector_short.sel(sectors=sector).values
            self.logger.info('name: {}'.format(name))
            visum_ds = xr.Dataset()
            visum_ds['zone_no'] = self.zone_no
            visum_ds['zone_names'] = self.zone_name
            matrix = np.zeros((self.n_zones, self.n_zones), dtype='d')
            self.logger.info('Sector {s}_{n}: add wiver-groups'.format(
                s=sector, n=name))
            for g in sector_groups:
                mat = self.results.trips_gij[g]
                mode = self.mode_g[g]
                mode_descr = self.modes[mode]
                group_name = self.group_names[g]
                self.logger.info(
                    'add group {g} {m}: {s:.0f}'.format(g=group_name,
                                                        m=mode_descr,
                                                        s=float(mat.sum())))
                matrix += mat
            visum_ds['matrix'] = matrix
            self.logger.info('Sector {s}_{n}: {t:.0f} trips'.format(
                s=sector, t=float(matrix.sum()), n=name,
            ))
            s = SavePTV(visum_ds)
            file_name = os.path.join(
                folder, 'wiver_{sector}_{n}.mtx'.format(
                    sector=sector, n=name))
            self.logger.info('save matrix for sector {s}_{n} to {f}'.format(
                s=sector, n=name, f=file_name
            ))
            s.savePTVMatrix(file_name, file_type=visum_format)
            self.logger.info('matrix_saved')

    def adjust_balancing_factor(self, iteration: int, threshold: float=0.1):
        """
        adjust the balancing factor for the destination choice model

        Parameters
        ----------
        threshold:
            if the difference between the modelled and the target trips is < threshold,
            the model converges
        """
        not_converged = ~ self.converged_g.astype(bool)
        sp = self.zonal_data.sink_potential
        target_share = sp / sp.sum('destinations')
        trips = self.balancing.trips_to_destination
        actual_share = trips / trips.sum('destinations')
        kf = target_share / actual_share
        kf[not_converged] = kf[not_converged].fillna(1)
        bf = self.balancing.balancing_factor
        # adjust balancing factor
        bf[not_converged] = bf[not_converged].fillna(1)
        bf[not_converged] = bf[not_converged] * kf[not_converged]
        # normalize balancing factor
        bf[not_converged] = bf[not_converged] / bf.mean('destinations')[not_converged]
        for g, group in enumerate(self.groups):
            if not_converged[g]:
                if (np.abs(kf[g] - 1) < threshold).all():
                    self.converged_g[g]= iteration
                    self.logger.info(
                        f'group {group} converged after {iteration} iterations')
                else:
                    self.logger.debug(f'group {group} not converged yet')
            else:
                self.logger.debug(f'group {group} was already converged')

    def calc(self):
        """calc the daily trips and the trips by time slice"""
        for g in range(self.n_groups):
            if self.converged_g[g] or not self.active_g[g]:
                continue
            self.calc_daily_trips(g)
            self.adjust_linking_trips(g)
            self.trips_gij[g] = (self.home_based_trips_gij[g] +
                                self.linking_trips_gij[g] +
                                self.return_trips_gij[g])
            self.trips_to_destination_gj[g] = (self.home_based_trips_gij[g] +
                                               self.linking_trips_gij[g]).sum(0)
        self.calc_time_series()
        self.aggregate_to_modes()
        self.calc_mean_distance()
        self.calc_mean_distance_mode()

    def calc_with_balancing(self,
                            max_iterations: int=10,
                            threshold: float=0.1):
        """
        calculate with balancing the destination choice model

        Parameters
        ----------
        max_iterations:
            the maximum number of iterations
        threshold:
            if the difference between the modelled and the target trips is < threshold,
            the model converges
        """
        self.converged_g[:] = 0
        iteration = 0
        while (not self.converged_g.all()) and iteration < max_iterations:
            iteration += 1
            self.logger.info(f'calculate trips in iteration {iteration}')
            self.calc()
            self.logger.info(f'Total trips: {self.trips_gij.sum():0.2f}')
            self.adjust_balancing_factor(iteration, threshold)

    def calc_starting_and_ending_trips(self) -> pd.DataFrame:
        """
        calculate the starting trips per zone and group and return them as Dataframe
        """
        trips_ij = self.results.trips_gij.sum('groups')
        modelled_trips = (trips_ij.sum('origins').\
            rename({'destinations': 'zone_no',}) + \
            trips_ij.sum('destinations').rename({'origins': 'zone_no',})) / 2

        df_modelled = modelled_trips.to_dataframe(name='modelled_trips')

        group_labels = []
        for g, group in enumerate(self.groups):
            sn = self.data.sector_short[int(self.data.sector_of_groups[g])].data
            mn = self.data.mode_name[int(self.data.mode_of_groups[g])].data
            group_label = '{}_{}'.format(mn, sn).replace(' ', '')
            group_labels.append(group_label)

        sp = self.data.sink_potential

        starting_trips_gh = (self.data.source_potential * self.data.tour_rates)
        if 'zone_no' in starting_trips_gh.coords:
            starting_trips_gh = starting_trips_gh.drop(['zone_no'])
        starting_trips_gh = starting_trips_gh.rename(
            {'origins': 'zone_no',})

        ending_trips_g = (starting_trips_gh.sum('zone_no')
                          * self.data.stops_per_tour)
        ending_trips_gh = sp * (ending_trips_g / sp.sum('destinations'))

        starting_trips_i = starting_trips_gh.sum('groups')
        ending_trips_i = ending_trips_gh.sum('groups')

        df_balancing = self.data.balancing_factor.to_dataframe(name='balance')
        df_balancing = df_balancing.reset_index().pivot(
            index='destinations', columns='groups', values='balance')
        df_balancing.columns =['Bal_{}'.format(col)
                                  for col in group_labels]

        df_s = starting_trips_i.to_dataframe(name='starting_trips')
        df_e = ending_trips_i.to_dataframe(name='ending_trips')
        df_e.index.name = 'zone_no'
        df_modelled['start_end'] = df_s.starting_trips + df_e.ending_trips

        df_ending = ending_trips_gh.to_dataframe(name='ending_trips_g')
        df_ending = df_ending.reset_index().pivot(
            index='destinations', columns='groups', values='ending_trips_g')

        df_ending.index.name = 'zone_no'
        df_ending.columns =['End_{}'.format(col)
                            for col in group_labels]

        df_starting = starting_trips_gh.to_dataframe(name='starting_trips_g')
        df_starting = df_starting.reset_index().pivot(
            index='zone_no', columns='groups', values='starting_trips_g')
        df_starting.columns =['Start_{}'.format(col)
                              for col in group_labels]

        df_sp = self.data.sink_potential.to_dataframe(name='sink_potential')
        df_sp = df_sp.reset_index().\
            rename(columns={'destinations': 'zone_no',}).\
            pivot(index='zone_no', columns='groups', values='sink_potential')
        df_sp.columns =['SP_{}'.format(col)
                        for col in group_labels]

        df_name = self.data.zone_name.to_dataframe()

        df = pd.concat([df_name,
                        df_modelled,
                        df_s,
                        df_e,
                        df_starting,
                        df_ending,
                        df_sp,
                        df_balancing],
                       axis=1)
        return df

