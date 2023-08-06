# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 21:00:21 2016

@author: MaxBohnet
"""

import os
import sys
import logging
import runpy
import tempfile
import pytest
from typing import Dict

import numpy as np
import orca
from wiver.wiver_python import (WIVER, InvalidWiverInputData,
                                DestinationChoiceError, DataConsistencyError)
import wiver.run_wiver
from netCDF4 import __hdf5libversion__


@pytest.fixture(scope='class', params=range(2))
def group(request) -> int:
    """
    different values for groups
    """
    return request.param


@pytest.fixture(scope='class', params=[-0.1, -0.5, -0.01])
def param_dist(request) -> float:
    """
    different values for distance parameters
    """
    return request.param


@pytest.fixture(scope='class', params=[1.01, 1.1, 1.5, 2, np.inf])
def param_savings_param(request):
    """
    different values for savings parameter
    """
    return request.param


@pytest.fixture(scope='class', params=range(5))
def zone_h(request) -> int:
    """
    different values for home zone
    """
    return request.param

@pytest.fixture(scope='module')
def folder(tmpdir_factory) -> str:
    """return a tempdir managed by pytest"""
    return tmpdir_factory.mktemp('Wiver').strpath


@pytest.fixture(scope='module',
                params=['Wiver',
                        pytest.param('ÄÖÜß', marks=pytest.mark.xfail(
                                     __hdf5libversion__ < '1.12',
                            reason='Bug in HDF5'))])
def result_folder(request, folder: str) -> str:
    """Temp folder to store the results"""
    result_folder = os.path.join(folder, f'results_{request.param}')
    os.makedirs(result_folder, exist_ok=True)
    return result_folder


@pytest.fixture()
def params_file(folder: str) -> str:
    """ The params-file"""
    fn = 'params'
    file_path = os.path.join(folder, '{}.h5'.format(fn))
    return file_path


@pytest.fixture()
def matrix_file(folder: str) -> str:
    """ The params-file"""
    fn = 'matrices'
    file_path = os.path.join(folder, '{}.h5'.format(fn))
    return file_path


@pytest.fixture()
def zones_file(folder: str) -> str:
    """ The params-file"""
    fn = 'zonal_data'
    file_path = os.path.join(folder, '{}.h5'.format(fn))
    return file_path


@pytest.fixture()
def result_file(folder: str) -> str:
    """ The params-file"""
    fn = 'results'
    file_path = os.path.join(folder, '{}.h5'.format(fn))
    return file_path


@pytest.fixture()
def balancing_file(folder: str) -> str:
    """ The params-file"""
    fn = 'balancing'
    file_path = os.path.join(folder, '{}.h5'.format(fn))
    return file_path


@pytest.fixture()
def wiver_files(params_file: str, matrix_file: str, zones_file: str,
                result_file: str, balancing_file: str) -> Dict[str, str]:
    files = {'params': params_file,
             'matrices': matrix_file,
             'zonal_data': zones_file,
             'results': result_file,
             'balancing': balancing_file,}
    return files


@pytest.fixture(scope='function')
def wiver(request) -> WIVER:
    """
    WIVER-instance
    """
    sector_name = np.array(['DL', 'IND'])
    sectors = np.array(['S55', 77])

    wiver = WIVER(n_groups=3,
                  n_zones=5,
                  n_time_slices=3,
                  n_modes=3,
                  n_sectors=len(sector_name))

    # mode of group
    wiver.mode_g = np.array([2, 2, 1])
    # define centroids of zones
    # 2 zones at the same spot
    x = np.array([2, 1, 1, 6, 10])
    y = np.array([5, 3, 3, 1, 7])
    # calc travel time between zones
    dx = x - x[:, np.newaxis]
    dy = y - y[:, np.newaxis]
    dist = np.sqrt(dx**2 + dy**2)
    wiver.km_ij = dist
    t = dist * 3

    # travel time is identical for all modes
    wiver.travel_time_mij[:] = t
    # define savings parameters
    wiver.savings_param_g = [2, 1.1, 1.01]

    wiver.source_potential_gh = np.array([[10, 20, 10, 0, 10],
                                         [100, 20, 10, 0, 0],
                                         [20, 10, 5, 0, 10],
                                         ])
    wiver.sink_potential_gj = np.array([[0, 100, 10, 0, 100],
                                        [0, 20, 10, 0, 0],
                                        [0, 0, 10, 0, 100],
                                        ])
    wiver.tour_rates_g = np.array([2, 3, 1])
    wiver.stops_per_tour_g = np.array([3, 2, 4])

    wiver.time_series_starting_trips_gs = np.array([[5, 3, 1],
                                                    [6, 2, 0],
                                                    [10, 0, 0]])
    wiver.time_series_linking_trips_gs = np.array([[2, 3, 2],
                                                   [1, 6, 1],
                                                   [2, 5, 3]])
    wiver.time_series_ending_trips_gs = np.array([[0, 3, 6],
                                                  [1, 2, 8],
                                                  [0, 0, 9]])

    wiver.zone_no = np.arange(10, 60, 10)
    wiver.zone_name = np.array(['{}-Stadt'.format(i)
                                for i in 'ABCDE'])

    wiver.sectors = sectors
    wiver.sector_short = sector_name
    wiver.sector_g = np.array([0, 1, 0])

    wiver.mode_name = np.array(['Rad', 'Pkw', 'OV'])
    wiver.modes = np.array(['R', 'P', 'O'])
    wiver.groups = np.array([200, 201, 999])
    wiver.group_names = np.array([f'Gruppe {i}' for i in wiver.groups])

    return wiver


class Test01_WiverData:
    """Test the WiverData"""
    def test_01_test_definitions(self, wiver: WIVER):
        """Test the WiverData creation"""
        wiver.define_datasets()
        print(wiver.params)
        print(wiver.zonal_data)
        print(wiver.matrices)
        print(wiver.results)
        # assert that the group names are set correctly
        np.testing.assert_array_equal(wiver.group_names,
                                      ['OV_DL', 'OV_IND', 'Pkw_DL'])

    def test_02_test_merge_definitions(self, wiver: WIVER):
        """Test the WiverData creation"""
        wiver.define_datasets()
        wiver.merge_datasets()
        print(wiver.data)
        dims = wiver.data.dims
        assert dims['origins'] == wiver.n_zones
        assert dims['destinations'] == wiver.n_zones
        assert dims['modes'] == wiver.n_modes
        assert dims['groups'] == wiver.n_groups
        assert dims['time_slices'] == wiver.n_time_slices

    def test_03_save_data(self, wiver: WIVER, wiver_files: Dict[str, str]):
        """Dave data as test data"""
        folder = os.path.dirname(wiver_files['params'])
        print('save to {}'.format(folder))
        wiver.define_datasets()
        wiver.calc()
        wiver.save_all_data(wiver_files)

    def test_04_read_data(self, wiver: WIVER, wiver_files: Dict[str, str]):
        """read model from test data and compare results with original data"""
        folder = os.path.dirname(wiver_files['params'])
        print('read from {}'.format(folder))
        wiver_from_file = WIVER.read_from_netcdf(wiver_files)
        wiver_from_file.calc()
        wiver.calc()
        np.testing.assert_almost_equal(wiver.trips_msij,
                                       wiver_from_file.trips_msij)

    def test_05_data_consistency(self, wiver: WIVER):
        """Test the data consistency"""
        wiver.assert_data_consistency()
        # introduce unfeasable data to mode_g
        wiver.mode_g[0] = 3
        with pytest.raises(DataConsistencyError) as e:
            wiver.assert_data_consistency()
        print(e.value)

        wiver.mode_g[:] = (1, -1, 1)
        with pytest.raises(DataConsistencyError) as e:
            wiver.assert_data_consistency()
        print(e.value)

    def test_06_save_data_as_visum(self, wiver: WIVER, folder: str):
        """Dave results as Visum data"""
        print('save to {}'.format(folder))
        wiver.define_datasets()
        wiver.calc()
        wiver.save_results_to_visum(folder, visum_format='B')
        wiver.save_results_to_visum(folder, visum_format='V')
        wiver.save_results_to_visum(folder, visum_format='BK')

    def test_07_validate_data(self, wiver: WIVER):
        """Test the validation"""
        wiver.stops_per_tour_g[:] = [1, 2, 3]
        wiver.validate_input_data
        # no values < 1 allowed
        wiver.stops_per_tour_g[:] = [0.8, 2, 3]
        with pytest.raises(InvalidWiverInputData) as e:
            wiver.validate_input_data()


class Test02_Wiver:
    """Test Wiver Model"""

    def test_01_calc_tours(self, wiver: WIVER, zone_h: int):
        """Test the tour rates and linking trips
        from different home zones (parameter: zone_h)"""
        g = 0
        tours = wiver.calc_tours(g, zone_h)
        target = wiver.source_potential_gh[g, zone_h] * wiver.tour_rates_g[g]
        assert tours == target
        linking_trips = wiver.calc_linking_trips(g, tours)
        assert linking_trips == tours * (wiver.stops_per_tour_g[g] - 1)
        print('{h}: {t}, {l}'.format(h=zone_h, t=tours, l=linking_trips))

    def test_02_destination_choice(self, wiver: WIVER, group: int, param_dist: float):
        """Test the destination choice model"""
        h = 0
        t = 0
        wiver.calc_destination_choice(t, group, h)
        before = wiver.p_destination_tj[t].copy()
        print(before)

        wiver.param_dist_g[group] = param_dist
        wiver.calc_destination_choice(t, group, h)
        after = wiver.p_destination_tj[t].copy()
        print(after)

        m = wiver.mode_g[group]
        res = np.zeros((wiver.n_zones))
        for j in range(wiver.n_zones):
            res[j] = wiver.calc_p_destination(group, m, h, j)
        res /= res.sum()
        print(res)
        np.testing.assert_allclose(res, wiver.p_destination_tj[t])

    def test_03_savings(self, wiver: WIVER, zone_h: int):
        """Test the savings function for closeby points 1 and 3
        from different home zones (parameter: zone_h)"""
        g = 0
        i = 1
        j = 3
        m = wiver.mode_g[g]
        s = wiver.calc_savings(g, m, zone_h, i, j)
        t_ki = wiver.travel_time_mij[m, zone_h, i]
        t_jk = wiver.travel_time_mij[m, j, zone_h]
        t_ij = wiver.travel_time_mij[m, i, j]
        s_target = (t_ki + t_jk - t_ij) / (t_ki + t_jk)
        print(s)
        assert s == s_target

        # edge case where t_hi and t_jh are 0
        wiver.travel_time_mij[m, zone_h, i] = 0
        wiver.travel_time_mij[m, j, zone_h] = 0
        wiver.travel_time_mij[m, i, j] = 0
        s = wiver.calc_savings(g, m, zone_h, i, j)
        assert s == 0
        #  linking trip is a detour and longer than the trip back to the depot
        wiver.travel_time_mij[m, i, j] = 1
        s = wiver.calc_savings(g, m, zone_h, i, j)
        assert s == -99

    def test_04_savings_factor(self, wiver: WIVER,
                               zone_h: int,
                               param_savings_param: float):
        """Test the savings factor function"""
        g = 0
        i = 1
        j = 3
        m = wiver.mode_g[g]
        wiver.savings_param_g[g] = param_savings_param
        sf = wiver.calc_savings_factor(g, m, zone_h, i, j)
        print(sf)

    def test_05_linking_trip_choice(self, wiver: WIVER, group: int):
        """Test the destination choice model"""
        h = 0
        t = 0
        wiver.calc_destination_choice(t, group, h)
        wiver.calc_linking_trip_choice(t, group, h)
        print(wiver.p_links_tij[t])

    def test_06_calc_trips(self, wiver: WIVER, group: int):
        """Test the destination choice model"""
        h = 0
        t = 0
        tours = 100
        linking_trips = 200
        wiver.calc_destination_choice(t, group, h)
        wiver.calc_linking_trip_choice(t, group, h)
        wiver.calc_trips(t, group, h, tours, linking_trips)
        np.testing.assert_almost_equal(wiver.home_based_trips_gij[group].sum(),
                                       tours)
        np.testing.assert_almost_equal(wiver.linking_trips_gij[group].sum(),
                                       linking_trips)

    def test_07_savings_influence(self, wiver: WIVER):
        """Test the destination choice model"""

        def check_trips_with_savings(wiver, group, h, t, tours, linking_trips):
            wiver.home_based_trips_gij[group] = 0
            wiver.linking_trips_gij[group] = 0
            wiver.calc_linking_trip_choice(t, group, h)
            wiver.calc_trips(t, group, h, tours, linking_trips)
            link_matrix = wiver.linking_trips_gij[group]
            print(link_matrix.astype(int))
            np.testing.assert_almost_equal(link_matrix.sum(),
                                           linking_trips)
            print(link_matrix[0].sum())
            print(link_matrix[1].sum())
            zone_interior_link_trips = link_matrix.diagonal().sum()
            return zone_interior_link_trips

        h = 2
        t = 0
        group = 0
        tours = 100
        linking_trips = 200
        wiver.param_dist_g[group] = -0.02
        wiver.calc_destination_choice(t, group, h)

        # test first without any savings
        wiver.savings_param_g[group] = np.inf
        interior_trips_no_savings = check_trips_with_savings(
            wiver, group, h, t, tours, linking_trips)

        # test first with low savings
        wiver.savings_param_g[group] = 2
        interior_trips_low_savings = check_trips_with_savings(
            wiver, group, h, t, tours, linking_trips)

        # test first with medium savings
        wiver.savings_param_g[group] = 1.1
        interior_trips_medium_savings = check_trips_with_savings(
            wiver, group, h, t, tours, linking_trips)

        # test first with strong savings
        wiver.savings_param_g[group] = 1.01
        interior_trips_high_savings = check_trips_with_savings(
            wiver, group, h, t, tours, linking_trips)

        # make sure that the zonal interior trips should be more used
        # the higher the savings are

        print(interior_trips_no_savings, interior_trips_low_savings,
              interior_trips_medium_savings, interior_trips_high_savings)

        assert (interior_trips_no_savings < interior_trips_low_savings <
                interior_trips_medium_savings < interior_trips_high_savings)

    def test_08_calc_time_series(self, wiver: WIVER):
        """Test the time_series"""
        for g in range(wiver.n_groups):
            wiver.calc_daily_trips(g)
            wiver.adjust_linking_trips(g)
            wiver.trips_gij[g] = (wiver.home_based_trips_gij[g] +
                                wiver.linking_trips_gij[g] +
                                wiver.return_trips_gij[g])
            wiver.trips_to_destination_gj[g] = (wiver.home_based_trips_gij[g] +
                                               wiver.linking_trips_gij[g]).sum(0)
        wiver.calc_time_series()

        # test the normalisation of the time series
        np.testing.assert_almost_equal(
            wiver.time_series_starting_trips_gs.sum(-1), 1)
        np.testing.assert_almost_equal(
            wiver.time_series_linking_trips_gs.sum(-1), 1)
        np.testing.assert_almost_equal(
            wiver.time_series_ending_trips_gs.sum(-1), 1)

        # test that the trips of the time slices add up to the daily matrix
        actual = wiver.trips_gsij.sum(1)
        desired = wiver.trips_gij
        np.testing.assert_array_almost_equal(actual, desired)

    def test_09_trips_gij(self, wiver: WIVER):
        """Test if the arrays are not overwritten"""
        arr_gij_before = wiver.trips_gij.__array_interface__
        for g in range(wiver.n_groups):
            wiver.calc_daily_trips(g)
        arr_gij_after = wiver.trips_gij.__array_interface__
        assert arr_gij_before == arr_gij_after

    def test_10_wiver_calc(self, wiver: WIVER):
        """Test the whole model with different number of threads"""
        wiver.calc()
        res = wiver.trips_gsij
        print(wiver.trips_gsij.sum(-1).sum(-1))

        wiver.set_n_threads(1)
        wiver.calc()
        res2 = wiver.trips_gsij
        np.testing.assert_allclose(res, res2)

        wiver.set_n_threads(16)
        wiver.calc()
        res3 = wiver.trips_gsij
        np.testing.assert_allclose(res, res3)

        # test if group without linking trips (only one stop) works
        g = 2
        wiver.stops_per_tour_g[g] = 1
        wiver.calc()
        res = wiver.trips_gij[g]
        assert np.isfinite(res).all()


    def test_21_no_destinations(self, wiver: WIVER):
        """Test exceptions when there is demand
        but no destinations accessible"""

        h = 0

        # normal execution without error
        t = 0
        group = 0
        wiver.calc_destination_choice(t, group, h)
        print(wiver.p_destination_tj[t])

        # now set sink_potential for group 0 to 0
        wiver.sink_potential_gj[0] = 0

        # this should raise a DestinationChoiceError, because no destinations
        # exists for group 0
        with pytest.raises(DestinationChoiceError) as e:
            wiver.calc_destination_choice(t, group, h)
        print(e.value)

        # make no destinations available
        t = 1
        group = 1
        m = wiver.mode_g[group]
        # infinitive travel times from home zone 0
        wiver.travel_time_mij[m, h, :] = np.inf
        # this should raise a Destination Choice Error, because there are
        # destinations for group 1, but they cannot be reached
        with pytest.raises(DestinationChoiceError) as e:
            wiver.calc_destination_choice(t, group, h)
        print(e.value)

    def test_22_no_accessible_linking_trips(self, wiver: WIVER):
        """Test exceptions when there linking trips find no accessible destinations
        but no destinations accessible"""
        # make no destinations available
        h = 0
        t = 1
        group = 1
        m = wiver.mode_g[group]
        # infinitive travel times for linking trips
        wiver.travel_time_mij[m, 1:3, 1:3] = np.inf
        wiver.calc_destination_choice(t, group, h)
        # calculating the linking trips should raise an error
        # because of lack of accessibility between the destinations
        with pytest.raises(DestinationChoiceError) as e:
            wiver.calc_linking_trip_choice(t, group, h)
        print(e.value)

        # one accessible linking trip is suffitient
        wiver.travel_time_mij[m, 2, 1] = 10
        wiver.calc_destination_choice(t, group, h)
        wiver.calc_linking_trip_choice(t, group, h)
        assert wiver.p_links_tij[t, 2, 1] == 1

    def test_23_test_raises_destination_choice_error(self, wiver: WIVER):
        """Test if the error is raised in the calc function"""
        wiver.calc()

        g = 0
        wiver.sink_potential_gj[g] = 0
        # this should raise a DestinationChoiceError, because no destinations
        # exists for group 0
        with pytest.raises(DestinationChoiceError) as e:
            wiver.calc()
        print(e.value)
        # reset sink_potential
        wiver.sink_potential_gj[g] = np.array([0, 100, 10, 0, 100])
        wiver.calc()

        g = 1
        m = wiver.mode_g[g]
        # infinitive travel times from home zone 0
        backup = wiver.travel_time_mij[m].copy()
        wiver.travel_time_mij[m, :, [1, 2]] = np.inf
        # this should raise a Destination Choice Error, because there are
        # destinations for group 1, but they cannot be reached
        with pytest.raises(DestinationChoiceError) as e:
            wiver.calc()
        print(e.value)
        # reset travel times
        wiver.travel_time_mij[m, :] = backup
        wiver.calc()

        # infinitive travel times for linking trips
        wiver.travel_time_mij[m, 1:3, 1:3] = np.inf
        # calculating the linking trips should raise an error
        # because of lack of accessibility between the destinations
        with pytest.raises(DestinationChoiceError) as e:
            wiver.calc()
        print(e.value)

    def test_31_aggregate_to_modes(self, wiver: WIVER):
        """aggregate to modes"""
        wiver.calc()
        wiver.aggregate_to_modes()

        for m, mode in enumerate(wiver.modes):
            # test for daily matrix
            actual = wiver.trips_mij[m]
            # both groups are of mode 2
            desired = wiver.trips_gij[wiver.mode_g==m].sum(0)
            np.testing.assert_array_almost_equal(actual, desired)

            # test for matrix by time-slices
            actual = wiver.trips_msij[m]
            desired = wiver.trips_gsij[wiver.mode_g==m].sum(0)
            np.testing.assert_array_almost_equal(actual, desired)

        # modes without group should be 0
        np.testing.assert_array_equal(wiver.trips_mij[0], 0)
        np.testing.assert_array_equal(wiver.trips_msij[0], 0)

    def test_40_mean_distance_beta(self, wiver: WIVER, param_dist: float):
        """
        Test the mean distance calculation
        with different distance parameters
        """
        wiver.param_dist_g[0] = param_dist
        wiver.calc()
        after = wiver.mean_distance_g
        print(after)

    def test_41_mean_distance_savings(self, wiver: WIVER, param_savings_param: float):
        """
        Test the mean distance calculation
        with different savings optimizations
        """
        wiver.savings_param_g[0] = param_savings_param
        wiver.calc()
        after = wiver.mean_distance_g
        print(after)

    def test_42_mean_distance_modes(self, wiver: WIVER, param_dist: float):
        """
        Test the mean distance modes calculation
        with different distance parameters
        """
        wiver.param_dist_g[0] = param_dist
        wiver.calc()
        after = wiver.mean_distance_m
        print(after)

    def test_50_balancing(self, wiver: WIVER):
        """
        Test if the trip distribution equals the sink_potential
        and that the total number of trips stay constant
        """
        wiver.define_datasets()
        sp = wiver.zonal_data.sink_potential
        target_share = sp / sp.sum('destinations')
        wiver.calc_with_balancing(max_iterations=100, threshold=0.001)
        trips = wiver.balancing.trips_to_destination
        actual_share = trips / trips.sum('destinations')
        np.testing.assert_allclose(actual_share, target_share, rtol=.1)

        target_total_trips = wiver.trips_gij.sum()
        actual_total_trips = wiver.trips_gij.sum()
        np.testing.assert_allclose(actual_total_trips,
                                   target_total_trips,
                                   rtol=.01)
        for g, group in enumerate(wiver.groups):
            print(f'Group {group} converged after {wiver.converged_g[g]} iterations.')

    def test_51_test_starting_equals_ending_trips(self, wiver: WIVER):
        """Test that starting and ending trips per zone are equal"""
        wiver.calc()
        starting_trips = wiver.trips_gij.sum(axis=2)
        ending_trips = wiver.trips_gij.sum(axis=1)
        np.testing.assert_almost_equal(starting_trips,
                                       ending_trips)

        # introduce an asymetry into the travel time matrix
        wiver.travel_time_mij[:, 0, :] *= 0.8
        wiver.travel_time_mij[:, 1, :] *= 1.2
        wiver.calc()
        starting_trips = wiver.trips_gij.sum(axis=2)
        ending_trips = wiver.trips_gij.sum(axis=1)
        np.testing.assert_almost_equal(starting_trips,
                                           ending_trips)


class Test03_TestExport:
    """Test export results"""
    def test_10_wiver_results(self, wiver: WIVER, wiver_files: Dict[str, str]):
        """Test export of the results"""
        wiver.calc()
        wiver.define_datasets()
        wiver.save_results(wiver_files)

    def test_11_wiver_detailed_results(self, wiver: WIVER, result_folder: str):
        """Test export of the results to visum"""
        wiver.calc()
        wiver.define_datasets()
        wiver.save_detailed_results_to_visum(result_folder)

    def test_12_calc_starting_ending_trips(self, wiver: WIVER):
        """Test calculation of starting and ending trips"""
        wiver.define_datasets()
        wiver.merge_datasets()
        wiver.calc_with_balancing()
        df = wiver.calc_starting_and_ending_trips()
        actual = df['start_end']
        target = df['modelled_trips']
        # test if with balancing the target trips and the actuals trips
        # do not differ more than 10 %
        np.testing.assert_allclose(actual, target, rtol=0.1)
        print(df)

    def test_21_run_orca(self, wiver: WIVER, folder: str):
        """Test the execution with orca"""
        with tempfile.TemporaryDirectory(dir=folder) as tmpfolder:
            orca.add_injectable('project_folder', tmpfolder)
            result_folder = orca.get_injectable('result_folder')
            os.makedirs(result_folder, exist_ok=True)
            orca.add_injectable('wiver', wiver)
            steps = [
                'save_input_data',
                'run_wiver',
                'save_results',
                'calc_starting_ending_trips',
                #  rund calc_starting_and_ending_trips a second time,
                # to see if the file is kept,
                # and only the sheet "data" is overwritten
                'calc_starting_ending_trips',
            ]

            orca.run(steps)

    def test_22_run_wiver(self, folder: str,
                          wiver: WIVER,
                          wiver_files: Dict[str, str]):
        """Test wiver.run_wiver with command line parameters"""
        backup_sys_argv = sys.argv
        os.makedirs(folder, exist_ok=True)
        matrix_folder = os.path.join(folder, 'matrices')
        os.makedirs(matrix_folder, exist_ok=True)

        # create input data
        orca.add_injectable('project_folder', folder)
        orca.add_injectable('wiver', wiver)
        steps = [
            'save_input_data',
            ]
        orca.run(steps)
        del sys.modules['wiver.run_wiver']
        sys.argv = ['', '-f={}'.format(folder), '-m={}'.format(matrix_folder)]
        try:
            gl = runpy.run_module('wiver.run_wiver', run_name='__main__')
        finally:
            sys.argv = backup_sys_argv

    def test_23_run_orca_selected_groups(self,
                                         wiver: WIVER,
                                         wiver_files: Dict[str, str]):
        """Test the execution with orca"""
        scenario = orca.get_injectable('scenario')
        max_iterations = orca.get_injectable('max_iterations')
        reset_balancing = orca.get_injectable('reset_balancing')
        groups_to_calculate = orca.get_injectable('groups_to_calculate')
        groups = [200, 999]

        with tempfile.TemporaryDirectory() as folder:
            orca.add_injectable('project_folder', folder)
            result_folder = orca.get_injectable('result_folder')
            os.makedirs(result_folder, exist_ok=True)

            orca.add_injectable('reset_balancing', True)
            # run only one group
            orca.add_injectable('scenario', 'my_scenario')
            orca.add_injectable('groups_to_calculate', groups)
            orca.add_injectable('project_folder', folder)
            orca.add_injectable('wiver', wiver)
            steps = [
                'save_input_data',
                'run_wiver_for_selected_groups',
                'save_detailed_results',
            ]

            orca.run(steps)

            result_folder = orca.get_injectable('result_folder')
            files = os.listdir(result_folder)
            for group in groups:
                group_idx = wiver.groups.searchsorted(group)
                sector_id = wiver.sector_g[group_idx]
                sector = wiver.sectors[sector_id]
                name = wiver.sector_short[sector_id]
                fn = 'wiver_{sector}_{name}.mtx'.format(sector=sector,
                                                        name=name)
                assert fn in files, \
                       'there should be a result matrix with name {}'.format(fn)

            print(files)

    def test_24_run_orca(self, wiver: WIVER, folder: str):
        """Test the execution with orca"""
        orca.add_injectable('wiver', wiver)
        orca.add_injectable('project_folder', folder)
        matrix_folder = os.path.join(folder, 'matrices')
        os.makedirs(matrix_folder, exist_ok=True)
        steps = [
            'add_logfile',
            'save_input_data',
            'run_wiver',
            'save_results',
        ]

        orca.run(steps)
        print(os.listdir(os.path.join(folder, 'log')))
        assert os.path.exists(os.path.join(folder, 'log'))
        orca.run(['close_logfile'])
