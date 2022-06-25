from settings import *
from flask import Flask, redirect, url_for, request

app = Flask(__name__)


@app.route("/")
def hello_world():
  return "<p>Hello World!</p>"


@app.route(f"/device/", methods=['GET'])
def get_device_all(dev_id):
  pass


@app.route(f"/device/<dev_id>", methods=['GET'])
def get_device(dev_id):
  content = request.get_json
  print(content)
  return dev_id


@app.route(f"/device/<dev_id>/status/", methods=['GET'])
def get_device_health(dev_id):
  pass

if __name__ == '__main__':
  app.run(debug = DEBUG)