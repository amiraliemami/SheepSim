# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 11:31:30 2019

@author: gyae
"""

from flask import Flask
app = Flask(__name__)




@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()
    
    
    
# always at the end
from app import routes