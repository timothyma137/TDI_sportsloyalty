from flask import Flask,render_template,request,redirect,session

import requests as rq
import simplejson as json
import pandas as pd
import quandl as qd
import numpy as np

from bokeh.plotting import figure, show, output_file
from bokeh.embed import components,file_html
 
app = Flask(__name__)

app.vars={}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/onepage', methods=['GET'])
def retrievesymbol():
    return render_template('interactivemap.html')

@app.route('/showgraph', methods=['POST'])
def stockgraph():
    app.vars['stocksymbol'] = request.form['stocksymbol']
    madegraph = makegraph(app.vars['stocksymbol'])
    thescript, thediv = components(madegraph)
    return render_template('stockgraph.html', script=thescript, div=thediv)

if __name__ == "__main__":
    app.run(host='159.89.38.228')