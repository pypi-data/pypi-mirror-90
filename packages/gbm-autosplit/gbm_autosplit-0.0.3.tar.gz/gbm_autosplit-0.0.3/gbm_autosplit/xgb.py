import math

import xgboost

from . import auto_split_logic


class XGBClassifier(xgboost.XGBClassifier):
    def __init__(self, objective="binary:logistic", max_n_estimators=5000, ratio_training=0.8, metric="auc",
                 ratio_min_child_weight=None, early_stopping_rounds=100, max_depth=None,
                 learning_rate=None, scale_pos_weight=None, subsample=None, colsample_bynode=None,
                 n_jobs=1, importance_type=None, base_score=None, booster=None, colsample_bylevel=None,
                 colsample_bytree=None, gamma=None, gpu_id=None, interaction_constraints=None,
                 max_delta_step=None, min_child_weight=None, missing=None, monotone_constraints=None,
                 num_parallel_tree=None, random_state=None, reg_alpha=None, reg_lambda=None, tree_method=None,
                 validate_parameters=None, verbosity=None, n_estimators=None, use_label_encoder=False):
        self.max_n_estimators = max_n_estimators
        self.early_stopping_rounds = early_stopping_rounds
        self.ratio_training = ratio_training
        self.ratio_min_child_weight = ratio_min_child_weight
        self.metric = metric
        super(XGBClassifier, self).__init__(
            objective=objective, n_estimators=max_n_estimators, max_depth=max_depth, learning_rate=learning_rate,
            scale_pos_weight=scale_pos_weight, subsample=subsample, colsample_bynode=colsample_bynode, n_jobs=n_jobs,
            importance_type=importance_type, base_score=base_score, booster=booster,
            colsample_bylevel=colsample_bylevel, colsample_bytree=colsample_bytree, gamma=gamma, gpu_id=gpu_id,
            interaction_constraints=interaction_constraints, max_delta_step=max_delta_step,
            min_child_weight=min_child_weight, missing=missing, monotone_constraints=monotone_constraints,
            num_parallel_tree=num_parallel_tree, random_state=random_state, reg_alpha=reg_alpha, reg_lambda=reg_lambda,
            tree_method=tree_method, validate_parameters=validate_parameters, verbosity=verbosity,
            use_label_encoder=use_label_encoder
        )

    def call_parent_fit(self, x, y, **kwargs):
        super(XGBClassifier, self).fit(x, y, **kwargs)

    def fit(self, x, y, **kwargs):
        if self.early_stopping_rounds > 0:
            self._set_min_child_weight(self.ratio_training * x.shape[0])
            auto_split_logic.auto_split_fit(self, x, y, early_stopping_rounds=self.early_stopping_rounds, **kwargs)
        self._set_min_child_weight(x.shape[0])
        self.call_parent_fit(x, y, verbose=False)

    def _set_min_child_weight(self, sample_size):
        if self.ratio_min_child_weight is not None:
            self.set_params(min_child_weight=int(math.ceil(sample_size*self.ratio_min_child_weight)))


class XGBRegressor(xgboost.XGBRegressor):
    def __init__(self, max_n_estimators=5000, ratio_training=0.8, metric="rmse", ratio_min_child_weight=None,
                 early_stopping_rounds=100, max_depth=None, learning_rate=None, scale_pos_weight=None,
                 subsample=None, colsample_bynode=None, n_jobs=1, importance_type=None, objective=None, base_score=None,
                 booster=None, colsample_bylevel=None, colsample_bytree=None, gamma=None, gpu_id=None,
                 interaction_constraints=None, max_delta_step=None, min_child_weight=None, missing=None,
                 monotone_constraints=None, num_parallel_tree=None, random_state=None, reg_alpha=None, reg_lambda=None,
                 tree_method=None, validate_parameters=None, verbosity=None, n_estimators=None):
        self.max_n_estimators = max_n_estimators
        self.early_stopping_rounds = early_stopping_rounds
        self.ratio_training = ratio_training
        self.ratio_min_child_weight = ratio_min_child_weight
        self.metric = metric
        super(XGBRegressor, self).__init__(
            n_estimators=max_n_estimators, max_depth=max_depth, learning_rate=learning_rate,
            scale_pos_weight=scale_pos_weight, subsample=subsample, colsample_bynode=colsample_bynode, n_jobs=n_jobs,
            importance_type=importance_type, objective=objective, base_score=base_score, booster=booster,
            colsample_bylevel=colsample_bylevel, colsample_bytree=colsample_bytree, gamma=gamma, gpu_id=gpu_id,
            interaction_constraints=interaction_constraints, max_delta_step=max_delta_step,
            min_child_weight=min_child_weight, missing=missing, monotone_constraints=monotone_constraints,
            num_parallel_tree=num_parallel_tree, random_state=random_state, reg_alpha=reg_alpha, reg_lambda=reg_lambda,
            tree_method=tree_method, validate_parameters=validate_parameters, verbosity=verbosity
        )

    def call_parent_fit(self, x, y, **kwargs):
        super(XGBRegressor, self).fit(x, y, **kwargs)

    def fit(self, x, y, **kwargs):
        if self.early_stopping_rounds > 0:
            self._set_min_child_weight(self.ratio_training * x.shape[0])
            auto_split_logic.auto_split_fit(self, x, y, early_stopping_rounds=self.early_stopping_rounds, **kwargs)
        self._set_min_child_weight(x.shape[0])
        self.call_parent_fit(x, y, verbose=False)

    def _set_min_child_weight(self, sample_size):
        if self.ratio_min_child_weight is not None:
            self.set_params(min_child_weight=int(math.ceil(sample_size*self.ratio_min_child_weight)))
