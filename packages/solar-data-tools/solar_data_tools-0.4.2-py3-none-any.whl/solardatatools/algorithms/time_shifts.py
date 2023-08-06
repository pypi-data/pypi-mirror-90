''' Time Shift Algorithm Module

This module contains the algorithm for detecting time shifts in an unlabeled PV
power production data sets. These occur because of the local clock on the data
logging system being changed or by incorrect handling of daylight savings.
The algorithm works as follows:

    - Estimate solar noon on each day from the data
    - Fit a signal demixing model, assuming a seasonal component and a piecewise
      constant component
    - Polish the L1 heuristic used to estimate piecewise constant component
      using iterative reweighting
    - Use piecewise constance component to detect shift points in time and
      correction amounts

'''

import numpy as np
from scipy.stats import mode
from solardatatools.solar_noon import energy_com, avg_sunrise_sunset
from solardatatools.utilities import total_variation_plus_seasonal_filter

class TimeShift():
    def __init__(self):
        self.metric = None
        self.s1 = None
        self.s2 = None
        self.index_set = None
        self.corrected_data = None
        self.roll_by_index = None
        self.normalized_holdout_error = None
        self.normalized_train_error = None
        self.best_c1 = None
        self.best_ix = None

    def run(self, data, use_ixs=None, c1=None, c2=200.,
            solar_noon_estimator='com', threshold=0.1, periodic_detector=False):
        if solar_noon_estimator == 'com':
            metric = energy_com(data)
        elif solar_noon_estimator == 'srss':
            metric = avg_sunrise_sunset(data, threshold=threshold)
        self.metric = metric
        if use_ixs is None:
            use_ixs = ~np.isnan(metric)
        else:
            use_ixs = np.logical_and(use_ixs, ~np.isnan(metric))
        self.use_ixs = use_ixs
        # Optimize c1
        if c1 is None:
            n = np.sum(use_ixs)
            select = np.random.uniform(size=n) <= 0.8
            train = np.copy(use_ixs)
            test = np.copy(use_ixs)
            train[use_ixs] = select
            test[use_ixs] = ~select
            c1s = np.logspace(-1, 2, 15)
            train_r = np.zeros_like(c1s)
            test_r = np.zeros_like(c1s)
            for i, v in enumerate(c1s):
                s1, s2 = self.estimate_components(metric, v, c2, train, periodic_detector)
                y = metric
                train_r[i] = np.average(np.power((y - s1 - s2)[train], 2))
                test_r[i] = np.average(np.power((y - s1 - s2)[test], 2))
            zero_one_scale = lambda x: (x - np.min(x)) / (np.max(x) - np.min(x))
            hn = zero_one_scale(test_r)
            rn = zero_one_scale(train_r)
            best_ix = np.argmin(hn)
            # if np.isclose(hn[best_ix], hn[-1]):
            #     best_ix = np.argmax(hn * rn)
            best_c1 = c1s[best_ix]
        else:
            best_c1 = c1
            hn = None
            rn = None
            c1s = None
            best_ix = None
        s1, s2 = self.estimate_components(metric, best_c1, c2, use_ixs, periodic_detector)
        # find indices of transition points
        index_set = np.arange(len(s1) - 1)[np.round(np.diff(s1, n=1), 3) != 0]
        s1, s2 = self.estimate_components(metric, best_c1, c2, use_ixs,
                                          periodic_detector,
                                          transition_locs=index_set)
        # Apply corrections
        roll_by_index = np.round(
            (mode(np.round(s1, 3)).mode[0] - s1) * data.shape[0] / 24, 0)
        self.roll_by_index = roll_by_index
        Dout = self.apply_corrections(data)

        # save results
        self.normalized_holdout_error = hn
        self.normalized_train_error = rn
        self.c1_vals = c1s
        self.best_c1 = best_c1
        self.best_ix = best_ix
        self.s1 = s1
        self.s2 = s2
        self.index_set = index_set
        self.corrected_data = Dout

    def estimate_components(self, metric, c1, c2, use_ixs, periodic_detector,
                            transition_locs=None):
        # Iterative reweighted L1 heuristic
        w = np.ones(len(metric) - 1)
        eps = 0.1
        for i in range(5):
            s1, s2 = total_variation_plus_seasonal_filter(
                metric, c1=c1, c2=c2,
                tv_weights=w,
                use_ixs=use_ixs,
                periodic_detector=periodic_detector,
                transition_locs=transition_locs
            )
            w = 1 / (eps + np.abs(np.diff(s1, n=1)))
        return s1, s2

    def plot_optimization(self):
        if self.best_ix is not None:
            c1s = self.c1_vals
            hn = self.normalized_holdout_error
            rn = self.normalized_train_error
            best_c1 = self.best_c1
            import matplotlib.pyplot as plt
            plt.plot(c1s, hn, marker='.')
            plt.axvline(best_c1, ls='--', color='red')
            plt.xscale('log')
            plt.title('holdout validation')
            plt.show()
            plt.plot(c1s, rn, marker='.')
            plt.axvline(best_c1, ls='--', color='red')
            plt.xscale('log')
            plt.title('training residuals')
            plt.show()
            plt.plot(c1s, hn * rn, marker='.')
            plt.axvline(best_c1, ls='--', color='red')
            plt.xscale('log')
            plt.title('holdout error times training error')
            plt.show()
            print(hn)

    def apply_corrections(self, data):
        roll_by_index = self.roll_by_index
        Dout = np.copy(data)
        for roll in np.unique(roll_by_index):
            if roll != 0:
                ixs = roll_by_index == roll
                Dout[:, ixs] = np.roll(data, int(roll), axis=0)[:, ixs]
        return Dout

    def invert_corrections(self, data):
        roll_by_index = self.roll_by_index
        Dout = np.copy(data)
        for roll in np.unique(roll_by_index):
            if roll != 0:
                ixs = roll_by_index == roll
                Dout[:, ixs] = np.roll(data, -int(roll), axis=0)[:, ixs]
        return Dout