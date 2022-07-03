import re
from settings import *
from flask import Flask, render_template, request
from db import insert_device, select_device
from jinja2.exceptions import TemplateNotFound
from ssh import check_interfaces

app = Flask(__name__)


@app.route(f"/device_<action>/", methods=['GET'])
def device_form(action):
    """Takes user to specified device_<action> template html forum

    /device_create/: Takes user to a form to insert a new device into the database
    /device_lookup/: Takes user to a form to search device info from the database
    """
    try:
        return render_template(f'device_{action}.html')
    except TemplateNotFound as error:
        print(f'Template error: {error}')
        return "<p>oops this page doesn't exist</p>"


@app.route("/device/", methods=['GET', 'POST', 'PUT'])
def device():
    """Endpoint facilitates database interaction
    
    GET request allows a device query
    POST request allows a device record to be inserted
    PUT request allows a device record to be updated (not available yet)
    """
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
        key = request.args.get('key', None)
        if key == 'None':
          key = None
        value = request.args.get('value', None)
        device_list = select_device(key, value)
        return render_template('device_query.html', device_list=device_list)

    if request.method == 'PUT':
        print('put')
        return "<p>put would be here</p>"


@app.route(f"/device/<column>/<value>/", methods=['GET'])
def get_device_by_column(column, value):
    """Endpoint allows user to execute SELECT query with WHERE clause

    Where:
    <column> = Column name for WHERE clause
    <value> = value for WHERE clause
    """
    device_list = select_device(column, value)
    return render_template('device_query.html', device_list=device_list)


@app.route(f"/device/<column>/<value>/status/", methods=['GET'])
def get_device_health_by_column(column, value):
    """Pull device interface status via SSH for devices that match search query

    Where:
    <column> = Column name for WHERE clause
    <value> = value for WHERE clause
    """
    if value == 'all':
            device_list = select_device(column, value)
    else:
        device_list = select_device(column, value)

    device_interface_list = []

    for device in device_list:
        device_info = {}
        device_info['id'] = device[0]
        device_info['label'] = device[1]
        device_info['location'] = device[2]
        device_info['serial'] = device[3]
        device_info['host'] = device[4]
        device_info['mac'] = device[5]

        try:
            data = check_interfaces(host=device[4], user=SSH['USERNAME'],
                                    rsa_key_file=SSH['RSA_KEY_FILE'])
        except:
            data = [{'ifname': 'Unavailable'}]
        device_info['interfaces'] = data

        device_interface_list.append(device_info)

    return render_template('device_interface.html', device_interface_list=device_interface_list)

if __name__ == '__main__':
    app.run(debug = True)