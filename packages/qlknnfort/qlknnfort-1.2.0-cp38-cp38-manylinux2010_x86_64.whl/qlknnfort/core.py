# This file is part of QLKNN-fortran
# You should have received the QLKNN-fortran LICENSE in the root of the project
import numpy as np
import pandas as pd

import qlknnfort.qlknn_f90wrap as QLKNNFORT


class QuaLiKizFortranNN:
    @property
    def _target_names(self):
        if self.opts.merge_modes:
            target_names = self._merged_target_names
        else:
            target_names = self._non_merged_target_names
        return target_names

    @property
    def _feature_min(self):
        return pd.Series(self.opts.min_input, index=self._feature_names)

    @property
    def _feature_max(self):
        return pd.Series(self.opts.max_input, index=self._feature_names)

    @property
    def _target_min(self):
        if self.opts.merge_modes:
            min_target = []
            for var in self._merged_target_names:
                if var in self._non_merged_target_names:
                    idx = self._non_merged_target_names.index(var)
                    min_target.append(self.opts.min_output[idx])
                else:
                    prefix = var[:3]
                    idx = [
                        self._non_merged_target_names.index(name)
                        for name in self._non_merged_target_names
                        if name.startswith(prefix)
                    ]
                    min_target.append(np.sum(self.opts.min_output[idx]))
            return pd.Series(min_target, index=self._target_names)
        else:
            return pd.Series(self.opts.min_output, index=self._target_names)

    @property
    def _target_max(self):
        if self.opts.merge_modes:
            max_target = []
            for var in self._merged_target_names:
                if var in self._non_merged_target_names:
                    idx = self._non_merged_target_names.index(var)
                    max_target.append(self.opts.max_output[idx])
                else:
                    prefix = var[:3]
                    idx = [
                        self._non_merged_target_names.index(name)
                        for name in qlknn_9D_non_merged_target_names
                        if name.startswith(prefix)
                    ]
                    max_target.append(np.sum(self.opts.max_output[idx]))
            return pd.Series(max_target, index=self._target_names)
        else:
            return pd.Series(self.opts.max_output, index=self._target_names)


def clip_to_bounds(output, clip_low, clip_high, low_bound, high_bound):
    if clip_low:
        for ii, bound in enumerate(low_bound):
            output[:, ii][output[:, ii] < bound] = bound

    if clip_high:
        for ii, bound in enumerate(high_bound):
            output[:, ii][output[:, ii] > bound] = bound

    return output


def determine_settings(
    network, input, safe, clip_low, clip_high, low_bound, high_bound
):
    if safe:
        if isinstance(input, pd.DataFrame):
            nn_input = input[network._feature_names]
        else:
            raise Exception("Please pass a pandas.DataFrame for safe mode")
        if low_bound is not None:
            low_bound = low_bound.loc[network._target_names].values
        if high_bound is not None:
            high_bound = high_bound.loc[network._target_names].values
    else:
        if input.__class__ == pd.DataFrame:
            nn_input = input.values
        elif input.__class__ == np.ndarray:
            nn_input = input

    if clip_low is True and (low_bound is None):
        low_bound = network._target_min.values
    if clip_high is True and (high_bound is None):
        high_bound = network._target_max.values
    return nn_input, safe, clip_low, clip_high, low_bound, high_bound
