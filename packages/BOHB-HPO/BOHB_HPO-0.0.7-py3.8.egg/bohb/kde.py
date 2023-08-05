import numpy as np
import statsmodels.api as sm

class KDEMultivariate(sm.nonparametric.KDEMultivariate):
    def __init__(self, configurations, vartypes):
        self.configurations = configurations
        self.vartypes = vartypes
        data = []
        for config in configurations:
            data.append(np.array(config.to_list()))
        data = np.array(data)
        super().__init__(data, vartypes, 'normal_reference')
