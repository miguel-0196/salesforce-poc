import os
import json
import requests

class SalesforceClient:
    def __init__(self):
        self.USERNAME = os.environ.get('SALES_USERNAME')
        self.PASSWORD = os.environ.get('SALES_PASSWORD')
        self.CONSUMER_KEY = os.environ.get('SALES_CLIENT_KEY')
        self.CONSUMER_SECRET = os.environ.get('SALES_CLIENT_SECRET')
        self.DOMAIN_NAME = os.environ.get('SALES_DOMAIN_NAME')

        json_data = {
            'grant_type': 'password',
            'username': self.USERNAME,
            'password': self.PASSWORD,
            'client_id': self.CONSUMER_KEY,
            'client_secret': self.CONSUMER_SECRET,
            'content-type': 'application/json'
        }

        uri_token_request = self.DOMAIN_NAME + '/services/oauth2/token'
        response = requests.post(uri_token_request, data=json_data)
        self.access_token = response.json()['access_token']

    def post_job(self, job_data):
        job_url = self.DOMAIN_NAME + '/services/data/v59.0/jobs/ingest/'

        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-PrettyPrint': '1'
        }

        response = requests.post(job_url, headers=headers, data=json.dumps(job_data).replace('\n', ''))
        return response.json()

    def insert_data(self, url, data):
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'text/csv',
            'Accept': 'application/json',
            'X-PrettyPrint': '1'
        }

        return requests.put(self.DOMAIN_NAME + '/' + url, headers=headers, data=data)

    def upload_complete(self, url):
        job_url = self.DOMAIN_NAME + '/services/data/v59.0/jobs/ingest/'

        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/json; charset=UTF-8',
            'Accept': 'application/json',
            'X-PrettyPrint': '1'
        }
        json_data = {
            'state': 'UploadComplete',
        }

        response = requests.patch(job_url + url, headers=headers, json=json_data)
        return response.json()

    def check_status(self, url):
        job_url = self.DOMAIN_NAME + '/services/data/v59.0/jobs/ingest/'

        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Accept': 'application/json',
            'X-PrettyPrint': '1'
        }

        response = requests.get(job_url + url, headers=headers)
        return response.json()

    def api_query(self, query):
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Encoding': 'gzip'
        }

        response = requests.get(self.DOMAIN_NAME + '/services/data/v59.0/query/?q=' + query, headers=headers)
        return response.json()

    def get_data(self, type, date1, date2):
        query = 'SELECT+FIELDS(STANDARD)+FROM+'+ type +'+WHERE+IsDeleted=False'

        if date1 != '' or date2 != '':
            if date1 != '':
                query += '+AND+LastModifiedDate>=' + date1 + 'T00:00:00.000%2B0000'

                if date2 != '':
                    query += '+AND+LastModifiedDate<=' + date2 + 'T00:00:00.000%2B0000'
            else:
                query += '+AND+LastModifiedDate<=' + date2 + 'T00:00:00.000%2B0000'

        return self.api_query(query)
    

    def load_extra(self, nextRecordsUrl):
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Encoding': 'gzip'
        }

        response = requests.get(self.DOMAIN_NAME + nextRecordsUrl)
        return response.json()