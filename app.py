import re
from settings import *
from flask import Flask, render_template, request
from db import insert_device, select_device

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello World!</p>"


@app.route(f"/device_create/", methods=['GET'])
def device_create():
    print('create')
    return render_template('device_create.html')


@app.route(f"/device_lookup/", methods=['GET'])
def device_lookup():
    return render_template('device_lookup.html')


@app.route("/device/", methods=['GET', 'POST', 'PUT'])
def device():
    if request.method == 'POST':
        label = request.form.get('label', None)
        location = request.form.get('location', None)
        serial = request.form.get('serial', None)
        host = request.form.get('host', None)
        mac = request.form.get('mac', None)
        insert_device(label=label, 
                      location=location,
                      serial=serial,
                      host=host,
                      mac=mac)
        return "<p>Device added</p>"

    if request.method == 'GET':
        value = request.form.get('key', None)
        key = request.form.get('value', None)
        device_list = select_device(value, key)
        return render_template('device_query.html', device_list=device_list)


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