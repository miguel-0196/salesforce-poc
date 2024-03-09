import os
import json
import requests
from dotenv import load_dotenv
from simple_salesforce import Salesforce

# Load environment variables
load_dotenv()

class SalesforceClient:
    def __init__(self) -> None:
        self.USERNAME = os.getenv('SALES_USERNAME')
        self.PASSWORD = os.getenv('SALES_PASSWORD')
        self.CONSUMER_KEY = os.getenv('SALES_CLIENT_KEY')
        self.CONSUMER_SECRET = os.getenv('SALES_CLIENT_SECRET')

    @staticmethod
    def oauth_url(redirect_uri):
        return "https://login.salesforce.com/services/oauth2/authorize?response_type=code&client_id="+os.getenv('SALES_CLIENT_KEY')+"&redirect_uri="+redirect_uri

    def init(self, callback_code = None, redirect_uri = None):
        if callback_code == None:
            data = {
                'grant_type': 'password',
                'username': self.USERNAME,
                'password': self.PASSWORD,
                'client_id': self.CONSUMER_KEY,
                'client_secret': self.CONSUMER_SECRET,
                'content-type': 'application/json'
            }
        else:
            data = {
                'grant_type': 'authorization_code',
                'redirect_uri': redirect_uri,
                'code': callback_code,
                'client_id' : self.CONSUMER_KEY,
                'client_secret' : self.CONSUMER_SECRET
            }

        uri_token_request = 'https://login.salesforce.com/services/oauth2/token'
        response = requests.post(uri_token_request, data=data).json()
        if 'error' in response:
            print("Oauth error:", response)
            return response['error_description']

        self.access_token = response['token_type'] + ' ' + response['access_token']
        self.domain_name = response['instance_url']
        self.sf = Salesforce(instance_url=response['instance_url'], session_id=response['access_token'])
        return 'OK'

    def post_job(self, job_data):
        job_url = self.domain_name + '/services/data/v59.0/jobs/ingest/'

        headers = {
            'Authorization': self.access_token,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-PrettyPrint': '1'
        }

        response = requests.post(job_url, headers=headers, data=json.dumps(job_data).replace('\n', ''))
        return response.json()

    def insert_data(self, url, data):
        headers = {
            'Authorization': self.access_token,
            'Content-Type': 'text/csv',
            'Accept': 'application/json',
            'X-PrettyPrint': '1'
        }

        return requests.put(self.domain_name + '/' + url, headers=headers, data=data)

    def upload_complete(self, url):
        job_url = self.domain_name + '/services/data/v59.0/jobs/ingest/'

        headers = {
            'Authorization': self.access_token,
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
        job_url = self.domain_name + '/services/data/v59.0/jobs/ingest/'

        headers = {
            'Authorization': self.access_token,
            'Accept': 'application/json',
            'X-PrettyPrint': '1'
        }

        response = requests.get(job_url + url, headers=headers)
        return response.json()

    def api_query(self, query):
        headers = {
            'Authorization': self.access_token,
            'Content-Encoding': 'gzip'
        }

        response = requests.get(self.domain_name + query, headers=headers)
        return response.json()

    def get_object_data(self, object_type, date1 = '', date2 = ''):
        # Check whether the object you want to see is a custom object or not.
        if object_type.endswith('__c'):
            query = 'SELECT+FIELDS(CUSTOM)+FROM+' + object_type + '+WHERE+IsDeleted=False'
        else:
            query = 'SELECT+FIELDS(STANDARD)+FROM+' + object_type + '+WHERE+IsDeleted=False'

        if date1 != '' or date2 != '':
            if date1 != '':
                query += '+AND+LastModifiedDate>=' + date1 + 'T00:00:00Z'

                if date2 != '':
                    query += '+AND+LastModifiedDate<=' + date2 + 'T23:59:59Z'
            else:
                query += '+AND+LastModifiedDate<=' + date2 + 'T23:59:59Z'

        if object_type.endswith('__c'):
            query += '+LIMIT+200'

        return self.api_query('/services/data/v59.0/query/?q=' + query)


    def load_extra(self, nextRecordsUrl):
        headers = {
            'Authorization': self.access_token,
            'Content-Encoding': 'gzip'
        }

        response = requests.get(self.domain_name + nextRecordsUrl, headers=headers)
        return response.json()


    def create_custom_obj(self, fullName, label, pluralLabel, fields):
        md_api = self.sf.mdapi
        custom_object = md_api.CustomObject(
            fullName = fullName,
            label = label,
            pluralLabel = pluralLabel,
            nameField = md_api.CustomField(
                label = "Name",
                type = md_api.FieldType("Text")
            ),
            fields = fields,
            deploymentStatus = md_api.DeploymentStatus("Deployed"),
            sharingModel = md_api.SharingModel("Read")
        )
        return md_api.CustomObject.create(custom_object)



# Self test
if __name__ == '__main__':
    salesforceClient = SalesforceClient()
    salesforceClient.init()
    #print(salesforceClient.get_data('Order'))

    obj_name = f'testobj22'
    field_name = 'col1'
    fields = [{
                'fullName': field_name + '__c',
                'label': field_name,
                'type': 'Text',
                'length': 255,
                'required': True
    }]
    salesforceClient.create_custom_obj(f'{obj_name}__c', obj_name, obj_name, fields)

    from pprint import pprint
    pprint(salesforceClient.api_query(f'/services/data/v59.0/sobjects/{obj_name}__c/describe'))
