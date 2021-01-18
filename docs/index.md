---
layout: default
---
# Insights Data Schemas

## External data pipeline

![External data pipeline](images/external-data-pipeline.png)

<img src="images/external-data-pipeline.png" alt="External data pipeline" usemap="#external-data-pipeline">
<map name="external-data-pipeline">
    <area shape="rect" coords="249, 155, 334, 212" title="Incoming messages in platform.upload.buckit" alt="Incoming messages in platform.upload.buckit" href="platform_upload_buckit_messages.html">
    <area shape="rect" coords="361,  46, 446, 103" title="Raw data stored in S3 bucket" alt="Raw data stored in S3 bucket" href="raw_data_S3_bucket.html">
    <area shape="rect" coords="496, 162, 581, 219" title="Data produced by OCP rules engine" alt="Data produced by OCP rules engine" href="ccx_data_pipeline.html">
    <area shape="rect" coords="496, 346, 581, 403" title="Data consumed from ccx.ocp.results topic" alt="Data consumed from ccx.ocp.results topic" href="ccx_ocp_results_topic.html">
    <area shape="rect" coords="496, 511, 581, 568" title="OCP results written into RDS" alt="OCP results written into RDS" href="into_rds.html">
    <area shape="rect" coords="127, 418, 212, 475" title="Rule content produced by Content Service" alt="Rule content produced by Content Servic" href="content_service.html">
</map>

[Incoming messages in `platform.upload.buckit`](platform_upload_buckit_messages.md)

## Internal data pipeline

[Incoming messages from SQS](incoming_sqs_messages.md)

## Implemented validators

[validators.md](validators.md)

## Documentation for Python packages

[validators.py](packages/validators.html)
