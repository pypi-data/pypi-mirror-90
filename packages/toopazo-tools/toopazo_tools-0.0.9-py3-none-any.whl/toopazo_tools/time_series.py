#!/usr/bin/env python

import numpy as np
from scipy import signal


class TimeseriesTools:

    @staticmethod
    def test_window(arr, n):
        return np.std(TimeseriesTools.rolling_window(arr, n), 1)

    @staticmethod
    def rolling_window(a, window):
        shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
        strides = a.strides + (a.strides[-1],)
        return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)

    @staticmethod
    def get_window(arr, i, nwindow):
        # size = np.shape(arr)
        # nmax = len(arr) - 1
        ifirst = i
        ilast = i + nwindow
        # if ilast > nmax:
        #     ilast = nmax
        #     sarr = arr[ifirst:ilast]
        # else:
        sarr = arr[ifirst:ilast]
        return sarr

    @staticmethod
    def apply_to_window(arr, fun, nwindow):

        nmax = len(arr) - 1

        # arg = '[apply_to_window] %s' % arr
        # print(arg)
        arg = '[apply_to_window] nwindow %s' % nwindow
        print(arg)
        arg = '[apply_to_window] nmax %s' % nmax
        print(arg)

        ilast = nmax - nwindow + 1
        res_arr = []
        for i in range(0, ilast + 1):
            sarr = TimeseriesTools.get_window(arr, i, nwindow)
            res = fun(sarr)
            res_arr.append(res)
            # arg = '[apply_to_window] ui %s, sarr %s, res %s' % (ui, sarr, res)
            # print(arg)
        return np.array(res_arr)

    @staticmethod
    def add_sarr(sarr):
        return np.sum(sarr)

    @staticmethod
    def add_abs_sarr(sarr):
        return np.std(sarr)

    @staticmethod
    def test_iterate_window():
        marr = np.arange(0, 15)
        mwindow = 5
        TimeseriesTools.apply_to_window(marr, TimeseriesTools.add_sarr, mwindow)

    @staticmethod
    def time_statistics(t_arr, verbose):
        t_arr = np.array(t_arr)
        t_nsamples = len(t_arr)

        # dt = delta times between samples
        t_diff = np.diff(t_arr)
        # Mean
        t_dt_mean = np.mean(t_diff)
        # Standard deviation
        t_dt_std = np.std(t_diff)
        # Signed deviation
        t_dt_sgndev = t_diff - t_dt_mean
        # Unsigned deviation
        t_dt_usgndev = np.abs(t_diff - t_dt_mean)
        # Mean signed deviation
        t_dt_meansgndev = np.mean(t_dt_sgndev)
        # Max unsigned deviation
        t_dt_maxusgndev = np.max(t_dt_usgndev)
        # Min unsigned deviation
        t_dt_minusgndev = np.min(t_dt_usgndev)

        res = [t_nsamples, t_dt_mean, t_dt_std, t_dt_meansgndev,
               t_dt_minusgndev, t_dt_maxusgndev]

        if verbose:
            print('[time_statistics] t_nsamples %s' % res[0])
            print('[time_statistics] t_dt_mean %s' % res[1])
            print('[time_statistics] t_dt_std %s' % res[2])
            print('[time_statistics] t_dt_meansgndev %s' % res[3])
            print('[time_statistics] t_dt_minusgndev %s' % res[4])
            print('[time_statistics] t_dt_maxusgndev %s' % res[5])

        return res

    @staticmethod
    def resample(t1_arr, x1_arr, t2_arr, dt_maxusgndev, verbose):
        t1_arr = np.array(t1_arr)
        t2_arr = np.array(t2_arr)
        x1_arr = np.array(x1_arr)

        [t1_nsamples, t1_dt_mean, t1_dt_std, t1_dt_meansgndev, t1_dt_minusgndev,
         t1_dt_maxusgndev] = TimeseriesTools.time_statistics(t1_arr, verbose)
        _ = [t1_dt_mean,  t1_dt_std, t1_dt_meansgndev, t1_dt_minusgndev]

        [t2_nsamples, t2_dt_mean, t2_dt_std, t2_dt_meansgndev, t2_dt_minusgndev,
         t2_dt_maxusgndev] = TimeseriesTools.time_statistics(t2_arr, verbose)
        _ = [t2_dt_mean, t2_dt_std, t2_dt_meansgndev, t2_dt_minusgndev]

        x1_nsamples = len(x1_arr)

        if x1_nsamples != t1_nsamples:
            print('[resample] t1_arr: x1_nsamples = %s != t1_nsamples = %s'
                  % (x1_nsamples, t1_nsamples))
            return x1_arr
        if t1_dt_maxusgndev > dt_maxusgndev or t2_dt_maxusgndev > dt_maxusgndev:
            print('[resample] t1_arr:')
            TimeseriesTools.time_statistics(t1_arr, True)
            print('[resample] t1_arr:')
            TimeseriesTools.time_statistics(t2_arr, True)
            return x1_arr

        x2_arr = signal.resample(x1_arr, t2_nsamples, t=None)
        # (x2_arr, t2_arr) =
        # scipy.signal.resample(x1_arr, t2_nsamples, t=t1_arr)

        if verbose:
            print('[resample] t1_arr:')
            TimeseriesTools.time_statistics(t1_arr, True)
            print('[resample] t1_arr:')
            TimeseriesTools.time_statistics(t2_arr, True)
            x2nsamples = len(x2_arr)
            print('[resample] x1_arr: x1_nsamples %s' % x1_nsamples)
            print('[resample] x2_arr: x2nsamples %s' % x2nsamples)

        return [t2_arr, x2_arr]


if __name__ == '__main__':
    TimeseriesTools.test_iterate_window()
