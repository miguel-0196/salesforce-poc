# Salesforce

## OAuth

### Setting

- Apps/App Manager/Connected App Setting:

    ✔️Enable OAuth Settings

    ✔️Enable for Device Flow

    ✔️Require Secret for Web Server Flow

    ✔️Require Secret for Refresh Token Flow

    Callback URL: https://127.0.0.1:4444/login/callback

    Selected Oauth Scopes: Full access(full)

- Identity/OAuth and OpenID Connect Settings:

    ✔️ Allow OAuth Username-Password Flows

### Reference
- Without web login

    https://python.plainenglish.io/connect-salesforce-oauth2-0-app-python-without-any-special-library-f2629a4d4e5a

- With web login

    https://developer.salesforce.com/blogs/developer-relations/2014/01/python-and-the-force-com-rest-api-simple-simple-salesforce-example
    https://gist.github.com/zaki-yama/c3407b550628e63af432#file-force_oauth-py-L58

- Fix

    https://trailhead.salesforce.com/trailblazer-community/feed/0D54V00007T42fmSAB




## How to create a custom object
- https://pypi.org/project/simple-salesforce/
- https://stackoverflow.com/questions/75437264/how-to-create-a-new-custom-object-in-salesforce-and-write-a-record-to-it
- https://stackoverflow.com/questions/65332251/how-to-create-custom-field-via-api
- https://stackoverflow.com/questions/72132475/simple-salesforce-create-custom-field
- https://medium.com/@saivarma844/creating-a-custom-field-on-salesforce-objects-2d515e6b0041



## How to create a lookup relationship field on an object

- https://pypi.org/project/simple-salesforce/

- https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/customobject.htm

- https://salesforce.stackexchange.com/questions/178364/create-a-lookup-field-in-salesforce-using-metadata-api-c
