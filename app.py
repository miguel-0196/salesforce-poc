#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard libraries
import os
import time

# External libraries
from flask import Flask, request, render_template

# Internal libraries
from SalesforceClient import SalesforceClient

salesforceClient = SalesforceClient()

# Flask app setup
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# App routes
@app.route("/")
def index():
    return render_template("main.html")

@app.post("/view_salesforce_data")
def view_salesforce_data():
    return salesforceClient.get_data(request.form['type'], request.form['date1'], request.form['date2'])

@app.post("/load_extra")
def load_extra():
    return salesforceClient.load_extra(request.form['nextRecordsUrl'])
    
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
    app.run(threaded=True, host='0.0.0.0', port=4444, ssl_context="adhoc")