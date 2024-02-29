#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard libraries
import os
import time

# External libraries
from flask import Flask, request, render_template, redirect

# Internal libraries
from SalesforceClient import SalesforceClient

# Flask app setup
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
service_ip = os.environ.get('SERVICE_IP') or '0.0.0.0'
service_port = os.environ.get('SERVICE_PORT') or 4444
salesforceClient = SalesforceClient()

# App routes
@app.route("/")
def index():
    oauth_url = salesforceClient.oauth_url(request.base_url + 'login/callback')
    print(oauth_url)
    return redirect(oauth_url)

@app.route("/login/callback")
def callback():
    code = request.args.get("code")
    result = salesforceClient.init(code, request.base_url)
    if result == 'OK':
        return redirect("/main")
    else:
        return "<b>Login failed: </b>" + result

@app.route("/main")
def main():
    return render_template("main.html")

@app.post("/view_salesforce_data")
def view_salesforce_data():
    return salesforceClient.get_data(request.form['type'], request.form['date1'], request.form['date2'])

@app.post("/load_extra")
def load_extra():
    return salesforceClient.load_extra(request.form['nextRecordsUrl'])

@app.post("/create_custom_obj")
def create_custom_obj():
    try:
        fields = []
        for one in request.form['fields'].split(','):
            fields.append({
                'fullName': f"{one}__c",
                'label': one,
                'type': 'Text',
                'length': 255
            })
        salesforceClient.create_custom_obj(f"{request.form['name']}__c", request.form['name'], 'Custom Objects', fields)
        return 'OK'
    except Exception as err:
        return str(err), 404

@app.post("/upload_salesforce_data")
def upload_salesforce_data():
    # type: Account
    # data:
    # Name,ShippingCity,NumberOfEmployees,AnnualRevenue,Website,Description
    # Lorem Ipsum,Milano,2676,912260031,https://ft.com/lacus/at.jsp,"Lorem ipsum dolor sit amet"
    try:
        job_data = {
            "object" : "",
            "contentType" : "CSV",
            "operation" : "insert",
            "lineEnding" : "LF"
        }
        job_data['object'] = request.form['type']

        pjr = salesforceClient.post_job(job_data)
        if 'contentUrl' not in pjr:
            return pjr, 405

        salesforceClient.insert_data(pjr['contentUrl'], request.form['data'])
        salesforceClient.upload_complete(pjr['id'])

        while (True):
            time.sleep(1)
            status = salesforceClient.check_status(pjr['id'])
            print(status['state'])

            if (status['state'] != 'InProgress'):
                return status
    except Exception as err:
        return str(err), 404


if __name__ == '__main__':
    app.run(threaded=True, host=service_ip, port=service_port, ssl_context="adhoc")