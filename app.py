from flask import Flask,render_template,request,redirect,session, jsonify, json

import re
import requests as rq
import simplejson as json
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from numpy import NaN
from sklearn.tree import DecisionTreeRegressor
from sklearn.base import TransformerMixin
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction import DictVectorizer

import logging
logging.basicConfig(filename='example.log',level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')

app = Flask(__name__)

app.vars={}

class RowIterator(TransformerMixin):
        """ Prepare dataframe for DictVectorizer """
        def fit(self, X, y=None):
            return self

        def transform(self, X):
            return (row for _, row in X.iterrows())

@app.route('/')

def index():
    return render_template('index.html', attendancenumber = 0)


@app.route('/basicadd', methods=['GET','POST'])
def basicadd():
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
    
    app.vars['cityinput'] = request.args.get('cityinput')
    app.vars['sportinput'] = request.args.get('sportinput')
    app.vars['wininput'] = request.args.get('wininput')
    
    exampledata2=pd.DataFrame([['Anaheim Ducks', 2010, str(app.vars['cityinput']), 100, 'Supersonics', str(app.vars['sportinput']), 33,33, float(app.vars['wininput']), 80]])

    theanswer= round(themodel.predict(exampledata2)[0], 1)
    
    if app.vars['cityinput'] not in [u'Atlanta',
 u'Baltimore',
 u'Bay Area',
 u'Boston',
 u'Buffalo',
 u'Calgary',
 u'Charlotte',
 u'Chicago',
 u'Cincinnati',
 u'Cleveland',
 u'Columbus',
 u'Dallas',
 u'Denver',
 u'Detroit',
 u'Edmonton',
 u'Houston',
 u'Indianapolis',
 u'Jacksonville',
 u'Kansas City',
 u'Los Angeles',
 u'Memphis',
 u'Miami',
 u'Milwaukee',
 u'Minneapolis',
 u'Montreal',
 u'Nashville',
 u'New Orleans',
 u'New York',
 u'Oklahoma City',
 u'Orlando',
 u'Ottawa',
 u'Philadelphia',
 u'Phoenix',
 u'Pittsburg',
 u'Portland',
 u'Raleigh-Durham',
 u'Sacramento',
 u'Salt Lake City',
 u'San Antonio',
 u'San Diego',
 u'Seattle',
 u'St. Louis',
 u'Tampa Bay',
 u'Toronto',
 u'Vancouver',
 u'Washington D.C.',
 u'Winnipeg']:
        theanswer= "pick a valid city"
    if app.vars['sportinput'] not in [u'NFL',u'NBA',u'MLB',u'NHL']:
        theanswer= "pick a valid sports league"
    if float(app.vars['wininput'])<0 or float(app.vars['wininput'])>1:
        theanswer= "pick a valid win percentage"

    
    
    return render_template('index.html', attendancenumber = theanswer, ci=app.vars['cityinput'], si=app.vars['sportinput'], wi=app.vars['wininput'])

if __name__ == "__main__":
    app.run(host='0.0.0.0')