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
    def resample(t1arr, x1arr, t2arr, dtmax, verbose):
        t1arr = np.array(t1arr)
        x1arr = np.array(x1arr)
        t2arr = np.array(t2arr)
        t1nsamples = len(t1arr)
        x1nsamples = len(x1arr)
        t2nsamples = len(t2arr)

        t1diff = np.diff(t1arr)
        t1diff_std = np.std(t1diff)
        t2diff = np.diff(t2arr)
        t2diff_std = np.std(t2diff)

        if x1nsamples != t1nsamples:
            print('[resample] t1arr: x1nsamples = %s != t1nsamples = %s'
                  % (x1nsamples, t1nsamples))
            return x1arr
        if t1diff_std > dtmax or t2diff_std > dtmax:
            print('[resample] t1arr: t1nsamples %s, t1diff_std %s'
                  % (t1nsamples, t1diff_std))
            print('[resample] t2arr: t2nsamples %s, t2diff_std %s'
                  % (t2nsamples, t2diff_std))
            print('[resample] Sampling time error is too large, dtmax = %s'
                  % dtmax)
            return x1arr

        x2arr = signal.resample(x1arr, t2nsamples, t=None)
        # (x2arr, t2arr) = scipy.signal.resample(x1arr, t2nsamples, t=t1arr)

        if verbose:
            print('[resample] t1arr: t1nsamples %s, t1diff_std %s'
                  % (t1nsamples, t1diff_std))
            print('[resample] t2arr: t2nsamples %s, t2diff_std %s'
                  % (t2nsamples, t2diff_std))
            x2nsamples = len(x2arr)
            print('[resample] x1arr: x1nsamples %s' % x1nsamples)
            print('[resample] x2arr: x2nsamples %s' % x2nsamples)

        return [t2arr, x2arr]


if __name__ == '__main__':
    TimeseriesTools.test_iterate_window()
