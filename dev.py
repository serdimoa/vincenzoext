from app import app
import os

__author__ = 'serdimoa'
app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)))
