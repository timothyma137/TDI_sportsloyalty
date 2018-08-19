from flask import Flask,render_template,request,redirect,session

import requests as rq
import simplejson as json
import pandas as pd
import quandl as qd
import numpy as np
 
app = Flask(__name__)

app.vars={}

@app.route('/')
def index():
    return render_template('index.html', attendancenumber = 0)

@app.route('/basicadd', methods=['GET', 'POST'])
def basicadd():
    app.vars['cityinput'] = request.args.get('cityinput')
    app.vars['sportinput'] = request.args.get('sportinput')
    app.vars['wininput'] = request.args.get('wininput')
    
    attendancenumber= app.vars['cityinput']+app.vars['sportinput']+app.vars['wininput']
    
    return rendertemplate('index.html', attendancenumber = attendancenumber)

if __name__ == "__main__":
    app.run(host='0.0.0.0')