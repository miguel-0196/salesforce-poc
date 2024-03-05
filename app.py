#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard libraries
import os
import json
import time

# External libraries
from flask import Flask, request, render_template, redirect, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
    UserMixin
)

# Internal libraries
from SalesforceClient import SalesforceClient

# Flask app setup
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
service_ip = os.environ.get('SERVICE_IP') or '0.0.0.0'
service_port = os.environ.get('SERVICE_PORT') or 4444

# User session management setup
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.unauthorized_handler
def unauthorized():
    return  '<meta http-equiv="REFRESH" content="0;URL=/">', 403

# Flask-Login helper to retrieve a user from our db
user_db = {}
@login_manager.user_loader
def load_user(user_id):
    if user_id not in user_db:
        return None
    return user_db[user_id]

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

# App routes
@app.route("/")
def index():
    oauth_url = SalesforceClient.oauth_url(request.base_url + 'login/callback')
    return redirect(oauth_url)

@app.route("/login/callback")
def callback():
    code = request.args.get("code")
    salesforceClient = SalesforceClient()
    result = salesforceClient.init(code, request.base_url)
    if result == 'OK':
        user = UserMixin()
        user.id = str(time.time())
        user.sf = salesforceClient
        user_db[user.id] = user
        login_user(user)
        return redirect("/main")
    else:
        return "<b>Login failed: </b>" + result

@app.route("/main")
@login_required
def main():
    return render_template("main.html")

@app.post("/view_salesforce_data")
@login_required
def view_salesforce_data():
    return current_user.sf.get_data(request.form['type'], request.form['date1'], request.form['date2'])

@app.post("/load_extra")
@login_required
def load_extra():
    return current_user.sf.load_extra(request.form['nextRecordsUrl'])

@app.post("/create_custom_obj")
@login_required
def create_custom_obj():
    try:
        current_user.sf.create_custom_obj(f"{request.form['name']}__c", request.form['name'], request.form['name'], json.loads(request.form['fields']))
        return 'OK'
    except Exception as err:
        return str(err), 404

@app.post("/upload_salesforce_data")
@login_required
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

        pjr = current_user.sf.post_job(job_data)
        if 'contentUrl' not in pjr:
            return pjr, 405

        current_user.sf.insert_data(pjr['contentUrl'], request.form['data'])
        current_user.sf.upload_complete(pjr['id'])

        while (True):
            time.sleep(1)
            status = current_user.sf.check_status(pjr['id'])

            if (status['state'] != 'InProgress'):
                return status
    except Exception as err:
        return str(err), 404


if __name__ == '__main__':
    app.run(threaded=True, host=service_ip, port=service_port, ssl_context="adhoc")