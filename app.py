from settings import *
from flask import Flask, redirect, render_template, url_for, request

app = Flask(__name__)


@app.route("/")
def hello_world():
  return "<p>Hello World!</p>"


@app.route(f"/device_lookup/", methods=['GET'])
def device_lookup():
  return render_template('device_lookup.html')


@app.route("/device/", methods=['GET'])
def device():
  if request.method == 'POST':
    if request.form['submit'] == 'lookup':
      print('lookup')
    if request.form['submit'] == 'save':
      print('save')
    print('post')
  if request.method == 'GET':
    print('get')


@app.route(f"/device/<dev_id>", methods=['GET'])
def get_device(dev_id):
  content = request.get_json
  print(content)
  return dev_id


@app.route(f"/device/<dev_id>/status/", methods=['GET'])
def get_device_health(dev_id):
  pass

if __name__ == '__main__':
  app.run(debug = True)