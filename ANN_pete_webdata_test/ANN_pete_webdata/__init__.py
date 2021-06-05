from flask import Flask

app = Flask(__name__)

from ANN_pete_webdata import routes
