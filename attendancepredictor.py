import numpy as np
import pandas as pd
import requests
import re
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from numpy import NaN
from sklearn.tree import DecisionTreeRegressor
from sklearn.base import TransformerMixin
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction import DictVectorizer

class RowIterator(TransformerMixin):
        """ Prepare dataframe for DictVectorizer """
        def fit(self, X, y=None):
            return self

        def transform(self, X):
            return (row for _, row in X.iterrows())

def newfunc():

    


    rawsportsdata = pd.read_excel('exceldata.xlsx')
    rsd = rawsportsdata

    for i in range(2001, 2018):
        rsd['per'+str(i)] = rsd['W'+str(i)]/(rsd['W'+str(i)]+rsd['L'+str(i)]) 

    inflate_01_17= [1, 1.0158, 1.0390, 1.0666, 1.1028, 1.1383, 1.1708, 1.2157, 1.2114, 1.2313, 1.2701, 1.2964, 1.3154,1.3367, 1.3383, 1.3552, 1.3841]

    for i, value in enumerate(range(2001, 2018)):
        rsd['t_inf'+str(value)] = rsd['T'+str(value)]/inflate_01_17[i] 

    newdataframe=[]
    for col in range(2001, 2018):
        for index, row in rsd.iterrows():
            if np.isnan(row['per'+str(col)]) or np.isnan(row['t_inf'+str(col)]) or np.isnan(row['A'+str(col)]) or row['A'+str(col)]>1400:
                pass
            else:
                newrow= [row['team_name'],
                         col,
                        row['City'],
                        row['Size'],
                        row['Mascot'],
                        row['sport'],
                        row['lat'],
                        row['lon'],
                        row['per'+str(col)],
                        row['t_inf'+str(col)],
                        row['A'+str(col)]]
                newdataframe.append(newrow)

    data_as_vector= pd.DataFrame(newdataframe)
    sorteddata= data_as_vector.sort_values(by=[2])

    copper_pipeline = Pipeline([
                        ('row_it', RowIterator()), 
                        ('dict_vect', DictVectorizer(sparse=False)),
                        ('dec_tree', DecisionTreeRegressor(random_state=7))

    ])
    themodel = copper_pipeline.fit(sorteddata[[2, 5, 8]], sorteddata[[10]] )


    exampledata2=pd.DataFrame([['Anaheim Ducks', 2010, 'Minneapolis', 100, 'Supersonics', 'NBA', 33,33, .3, 80]])
    
    return(themodel.predict(exampledata2))
