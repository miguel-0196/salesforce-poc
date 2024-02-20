# [Salesforce Bulk API 2.0](https://developer.salesforce.com/docs/atlas.en-us.api_asynch.meta/api_asynch/asynch_api_intro.htm)

It is based on REST principles and are optimized for working with `large sets of data`.

Use them to insert, update, upsert, or delete many records `asynchronously`. You submit a request and come back for the `results later`.

## When
Any data operation that includes `more than 2,000` records is a good candidate for Bulk API 2.0 to successfully prepare, execute, and manage an asynchronous workflow that uses the Bulk framework. 

Jobs with `fewer than 2,000` records should involve “bulkified” synchronous calls in REST (for example, Composite) or SOAP.


## Job

Bulk API 2.0 `ingest` jobs allow you to upload records to your org by using a CSV file representation.

Bulk API 2.0 `query` jobs return records based on the specified query.







# [Salesforce API Sorts](https://developer.salesforce.com/docs/apis#browse)

### [Bulk API 2.0](https://developer.salesforce.com/docs/atlas.en-us.api_bulk_v2.meta/api_bulk_v2/bulk_ingest.htm)



### [REST API](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/intro_what_is_rest_api.htm)






# Query performance and optimizing.

1. Query optimizing
https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/resources_query.htm

When excute a query with REST API, up to 2k records can be returned at a time in a synchronous request. (We can set the limit to less than 2k.)
However, to optimize performance, the returned batch can include fewer records than the limit or what's set in the request.

2. Query Performance Feedback (Beta)
https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/resources_query_performance_feedback.htm

3. Use a compression header to compress a REST API request or response.
https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/intro_rest_compression.htm

4. For integration users who make only API calls, Salesforce recommends setting MRU field to false to improve performance.
https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/headers_mru.htm

5. For best performance, we should care about API Limits. You can get lists information about limits in your org.
https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/resources_limits.htm

DailyApiRequests, DailyAsyncApexExecutions, DailyBulkApiBatches, DataStorageMB, FileStorageMB, PermissionSets