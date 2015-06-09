from sklearn.base import TransformerMixin, BaseEstimator
from sklearn.decomposition import FactorAnalysis
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline, make_pipeline, FeatureUnion, make_union
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.cross_validation import StratifiedKFold
from scipy import stats

import numpy as np


class FitlessMixin(TransformerMixin, BaseEstimator):
    def fit_transform(self, X, y=None, **fit_params):
        self.fit(X, y, **fit_params)
        return self.transform(X)

    def fit(self, X, y=None, **fit_params):
        return self


class IdentityTformer(FitlessMixin):
    def transform(self, X, y=None, **fit_params):
        return X


class DenseTformer(FitlessMixin):
    def transform(self, X, y=None, **fit_params):
        return X.todense()

    
class InverseTformer(FitlessMixin):
    def transform(self, X, y=None, **fit_params):
        return 1. - 1./(X+1.)

class RootTformer(FitlessMixin):
    def __init__(self, root=2, offset=0):
        self.root = root
        self.offset = offset
        
    def transform(self, X, y=None, **fit_params):
        return (X + self.offset)**(1./self.root)
    
class AnscombeTformer(FitlessMixin):
    def transform(self, X, y=None, **fit_params):
        return np.sqrt(X+0.375)
    
class FreemanTukeyTformer(FitlessMixin):
    def transform(self, X, y=None, **fit_params):
        return np.sqrt(X+1) + np.sqrt(X)
    
class ArcsinhTformer(FitlessMixin):
    def transform(self, X, y=None, **fit_params):
        return np.log(X + np.sqrt(X**2 + 1))
    
class AbsTformer(FitlessMixin):
    def transform(self, X, y=None, **fit_params):
        return np.abs(X)
    
class BoxCoxTformer(TransformerMixin, BaseEstimator):
    def __init__(self):
        self.lambdas = None
    
    def fit(self, X, y=None):
        # Not sure how to use np.apply_over_axes here
        self.lambdas = [stats.boxcox(X[:, col])[1] for col in range(X.shape[1])]
        return self
    
    def transform(self, X, y=None):
        return np.array([stats.boxcox(X[:, col])[0] for col in range(X.shape[1])]).T
    
    def fit_transform(self, X, y=None):
        t = [stats.boxcox(X[:, col]) for col in range(X.shape[1])]
        xt, self.lambdas = zip(*t)
        return np.array(xt).T
    
class AddTformer(FitlessMixin):
    def __init__(self, offset=0):
        self.offset = offset
        
    def transform(self, X, y=None, **fit_params):
        return X + self.offset
    
class LogTformer(FitlessMixin):
    def transform(self, X, y=None, **fit_params):
        return np.log(X + 1)
    
class GLogTformer(FitlessMixin):
    def __init__(self, a=0):
        self.a = a
        
    def transform(self, X, y=None, **fit_params):
        return np.log(X + np.sqrt(X**2 + self.a**2)/2.)    


class NzTformer(FitlessMixin):
    def transform(self, X, y=None, **fit_params):
        return np.apply_along_axis(func1d=np.count_nonzero,
                                   axis=1, arr=X)[:, None]


class NzvarTformer(FitlessMixin):
    def transform(self, X, y=None, **fit_params):
        ret = np.apply_along_axis(func1d=lambda r: np.var(r[np.nonzero(r)]),
                                  axis=1, arr=X)[:, None]
        ret[np.isnan(ret)] = 0
        return ret


class NzmeanTformer(FitlessMixin):
    def transform(self, X, y=None, **fit_params):
        ret = np.apply_along_axis(func1d=lambda r: np.mean(r[np.nonzero(r)]),
                                  axis=1, arr=X)[:, None]
        ret[np.isnan(ret)] = 0
        return ret


pipe = make_pipeline(
    TfidfTransformer(norm=u'l2',
                     use_idf=True,
                     smooth_idf=True,
                     sublinear_tf=True),
    DenseTformer(),
    make_union(
        IdentityTformer(),
        # FactorAnalysis(n_components=74),
        # PCA(n_components=20, whiten=True),
        NzTformer(),
        NzvarTformer(),
        NzmeanTformer(),
    ),
    StandardScaler(),
    # MinMaxScaler(),
)