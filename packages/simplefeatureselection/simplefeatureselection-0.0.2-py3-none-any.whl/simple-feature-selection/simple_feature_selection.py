import numpy as np
import pandas as pd
import category_encoders as ce
from boruta import BorutaPy
from sklearn.ensemble import RandomForestClassifier as RFC


class SimpleFeatureSelection(object):
    def __init__(self):
        pass
    
    def _onehot_encoding(self, df, cols):
        
        df_cat_oh = pd.get_dummies(df[cols])
        print("One Hot data size: {}".format(df_cat_oh.shape))
        return df_cat_oh
        
    def _ordinary_encoding(self, df, cols):
        obj_df = df.copy()
        encoder  = ce.OrdinalEncoder(cols=cols.to_list(), handle_unknown='impute')
        df_cat_oe = encoder.fit_transform(obj_df)
        df_cat_oe = df_cat_oe.add_suffix("_od")
        print("Ordinary data size: {}".format(df_cat_oe.shape))

        return df_cat_oe
        
    def _binary_encoding(self, df, cols):
        
        obj_df = df.copy()
        encoder   = ce.BinaryEncoder(cols=cols.to_list(), handle_unknown='impute')
        df_cat_bn = encoder.fit_transform(obj_df)
        df_cat_bn = df_cat_bn.add_suffix("_bn")
        print("Binary data size: {}".format(df_cat_bn.shape))
    
        return df_cat_bn
        
    def _polynomial_encoding(self, df, cols):
        obj_df = df.copy() 
        encoder = ce.PolynomialEncoder(cols=cols.to_list(), handle_unknown='impute')
        df_cat_pn = encoder.fit_transform(obj_df)
        df_cat_pn = df_cat_pn.add_suffix("_pn")
        print("Polynomial data size: {}".format(df_cat_pn.shape))
        return df_cat_pn
    
    def _boruta_selection(self, df_X, df_y):
        model = RFC(n_estimators=100,
                    criterion="entropy",
                    max_depth=4,
                    max_features = 'sqrt',
                    n_jobs=-1,
                    verbose=True) 

        feature_selector = BorutaPy(model,
                        n_estimators="auto",
                        verbose=2,
                        alpha=0.05,
                        max_iter=10,
                        random_state=1)
    
        feature_selector.fit(df_X.values, df_y.values)
        df_X_boruta = df_X.iloc[:, feature_selector.support_]
    
        return df_X_boruta, df_y
        
    
    def fit_transform(self, df_X, df_y):
        
        cat_cols = df_X.select_dtypes(include=["category"]).columns
        cat_obj_cols = df_X.select_dtypes(exclude=["int64", "float64"]).columns
        num_cols = df_X.select_dtypes(include=["int64", "float64"]).columns
        
        df_num = df_X[num_cols]
        df_oh = self._onehot_encoding(df_X, cat_cols)
        df_od = self._ordinary_encoding(df_X, cat_obj_cols)
        df_bn = self._binary_encoding(df_X, cat_obj_cols)
        df_pn = self._polynomial_encoding(df_X, cat_cols)
        
        df_tot = pd.concat([df_num, df_od, df_bn, df_pn], axis=1)
        print("Concat data size: {}".format(df_tot.shape))
        
        df_bt, df_y = self._boruta_selection(df_tot, df_y)
        print("Redused data size: {}".format(df_bt.shape))
        
        #return df_num, df_oh, df_od, df_bn
        return df_bt, df_y