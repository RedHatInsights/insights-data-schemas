---
layout: default
---
\[[Front page](index.md)\]

# Insights Data Schemas

## External data pipeline

### Whole data flow

1. Event about new data from insights operator is consumed from Kafka. That event contains (among
other things) URL to S3 Bucket
2. Insights operator data is read from S3 Bucket and Insights rules are applied to that data
3. Results (basically organization ID + account number + cluster name + insights results JSON) are stored back into
Kafka, but into different topic
4. That results are consumed by Insights rules aggregator service that caches them
5. The service provides such data via REST API to other tools, like OpenShift Cluster Manager web
UI, OpenShift console, etc.

### Architecture diagram

<img src="images/external-data-pipeline.png" alt="External data pipeline" usemap="#external-data-pipeline">
<map name="external-data-pipeline">
    <area shape="rect" coords="249, 155, 334, 212" title="Incoming messages in platform.upload.buckit" alt="Incoming messages in platform.upload.buckit" href="external-pipeline/platform_upload_buckit_messages.html">
    <area shape="rect" coords="361,  46, 446, 103" title="Raw data stored in S3 bucket" alt="Raw data stored in S3 bucket" href="external-pipeline/raw_data_S3_bucket.html">
    <area shape="rect" coords="496, 162, 581, 219" title="Data produced by OCP rules engine" alt="Data produced by OCP rules engine" href="external-pipeline/ccx_data_pipeline.html">
    <area shape="rect" coords="496, 346, 581, 403" title="Messages consumed from ccx.ocp.results topic" alt="Data consumed from ccx.ocp.results topic" href="external-pipeline/ccx_ocp_results_topic.html">
    <area shape="rect" coords="496, 511, 581, 568" title="OCP results written into RDS" alt="OCP results written into RDS" href="external-pipeline/results_in_rds.html">
    <area shape="rect" coords="127, 418, 212, 475" title="Rule content produced by Content Service" alt="Rule content produced by Content Servic" href="external-pipeline/content_service.html">
</map>

### Data format descriptions

1. [Incoming messages in `platform.upload.buckit`](external-pipeline/platform_upload_buckit_messages.md)
1. [Raw data stored in S3 bucket](external-pipeline/raw_data_S3_bucket.md)
1. [Data produced by OCP rules engine](external-pipeline/ccx_data_pipeline.md)
1. [Messages consumed from `ccx.ocp.results` topic](external-pipeline/ccx_ocp_results_topic.md)
1. [OCP results written into RDS](external-pipeline/results_in_rds.md)
1. [Rule content produced by Content Service](external-pipeline/content_service.md)
1. [Rule content consumed by Content Service](external-pipeline/content_service_source.md)

