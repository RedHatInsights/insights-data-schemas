---
layout: default
---
\[[Front page](index.md)\]

# Insights Data Schemas

## Internal data pipeline

Internal data pipeline is responsible for processing Insights Operator
archives, extracting features, transforming data, and aggregating results into
reports that later will be served by API and UI.

### Whole data flow

SQS listener service listens to notifications sent to AWS SQS (Simple Queue
Service) about new files in the S3 bucket. It sends a message with S3 path of
the file to `ccx-XXX-insights-operator-archive-new` (where `XXX` needs to be
changed to `prod` etc.) Kafka topic for every new file in S3.

Archive Sync Service synchronizes every new archive by reading the related
information from `ccx-XXX-insights-operator-archive-new` (where `XXX` needs to
be replaced by environment, for example `prod`) Kafka topic, downloading the
archive from AWS S3 and uploading it to DataHub (Ceph) bucket. Information
about synchronized archive and its metadata are sent to
`ccx-XXX-insights-operator-archive-synced` Kafka topic.

Rules Service runs rules for all archives synced in DataHub (Ceph) bucket. It
reads messages from `ccx-XXX-insights-operator-archive-synced` Kafka topic to
know about incoming archives in Ceph and it will download the archive from
DataHub (Ceph) bucket. The result of the applied rules is sent to
`ccx-XXX-insights-operator-archive-rules-results` Kafka topic.

Features service runs feature extraction for all archives synced in DataHub
(Ceph) bucket. It reads messages from
`ccx-XXX-insights-operator-archive-synced` Kafka topic where `XXX` needs to be
replaced by environment (`prod` etc.) to know about incoming archives in Ceph
and it will download the archive from DataHub (Ceph) bucket. The result of the
feature extraction is sent to `ccx-XXX-insights-operator-archive-features`
Kafka topic.

Parquet Factory is a program that can read data from several data sources,
aggregate the data received from them and generate a set of Parquet files with
the aggregated data, storing them in a selected S3 or Ceph bucket. It is used
to generate different data aggregations in the CCX Internal Data Pipeline,
reading data from Kafka topics.

### Architecture diagram

<img src="images/internal-data-pipeline-architecture.png" alt="Internal data pipeline" usemap="#internal-pipeline">
<map name="internal-pipeline">
    <area shape="rect" coords="110, 298,  155, 333"   title="Incoming messages in `platform.upload.announce`" alt="internal-pipeline/platform.upload.announce_messages.html" href="internal-pipeline/platform.upload.announce_messages.html">
    <area shape="rect" coords="110, 430,  155, 465"   title="Incoming messages from SQS" alt="internal-pipeline/incoming_sqs_messages.html" href="internal-pipeline/incoming_sqs_messages.html">
    <area shape="rect" coords="110, 540,  155, 575"   title="Messages produced by SQS listener" alt="internal-pipeline/sqs_listener_messages.html" href="internal-pipeline/sqs_listener_messages.html">
    <area shape="rect" coords="139, 579,  184, 614"   title="Messages consumed from `ccx-XXX-insights-operator-archive-new` topic" alt="internal-pipeline/insights_operator_archive_new.html" href="internal-pipeline/insights_operator_archive_new.html">
    <area shape="rect" coords="223, 399,  268, 434"   title="Raw data stored in S3 bucket" alt="internal-pipeline/raw_data_S3_bucket.html" href="internal-pipeline/raw_data_S3_bucket.html">
    <area shape="rect" coords="283, 579,  328, 614"   title="Raw data stored into Ceph bucket" alt="internal-pipeline/raw_data_Ceph_bucket.html" href="internal-pipeline/raw_data_Ceph_bucket.html">
    <area shape="rect" coords="226, 649,  271, 684"   title="Messages produced by archive-sync-service" alt="internal-pipeline/archive_sync_service_messages.html" href="internal-pipeline/archive_sync_service_messages.html">
    <area shape="rect" coords="136, 698,  181, 733"   title="Messages consumed by Rules service from `ccx-XXX-insights-operator-archive-synced` topic" alt="internal-pipeline/insights_operator_archive_synced_rules_service.html" href="internal-pipeline/insights_operator_archive_synced_rules_service.html">
    <area shape="rect" coords="280, 698,  325, 733"   title="Messages consumed by Features service from `ccx-XXX-insights-operator-archive-synced` topic" alt="internal-pipeline/insights_operator_archive_synced_features_service.html" href="internal-pipeline/insights_operator_archive_synced_features_service.html">
    <area shape="rect" coords="110, 877,  155, 912"   title="Messages produced by Rules service" alt="internal-pipeline/rules_service_messages.html" href="internal-pipeline/rules_service_messages.html">
    <area shape="rect" coords="355, 877,  400, 912"   title="Messages produced by Features service" alt="internal-pipeline/features_service_messages.html" href="internal-pipeline/features_service_messages.html">
    <area shape="rect" coords="110, 1020, 155, 1055"  title="Messages consumed from `ccx-XXX-insights-operator-archive-rules-results` topic" alt="internal-pipeline/parquet_rules_results.html" href="internal-pipeline/parquet_rules_results.html">
    <area shape="rect" coords="355, 1020, 400, 1055"  title="Messages consumed from `ccx-XXX-insights-operator-archive-features` topic" alt="internal-pipeline/parquet_features.html" href="internal-pipeline/parquet_features.html">
    <area shape="rect" coords="229, 1115, 274, 1150"  title="Generated parquet files" alt="internal-pipeline/parquet_output.html" href="internal-pipeline/parquet_output.html">
</map>



### Data format descriptions

1. [Incoming messages in `platform.upload.announce`](internal-pipeline/platform.upload.announce_messages.md)
1. [Incoming messages from SQS](internal-pipeline/incoming_sqs_messages.md)
1. [Messages produced by SQS listener](internal-pipeline/sqs_listener_messages.md)
1. [Messages consumed from `ccx-XXX-insights-operator-archive-new` topic](internal-pipeline/insights_operator_archive_new.md)
1. [Raw data stored in S3 bucket](internal-pipeline/raw_data_S3_bucket.md)
1. [Raw data stored into Ceph bucket](internal-pipeline/raw_data_Ceph_bucket.md)
1. [Messages produced by archive-sync-service](internal-pipeline/archive_sync_service_messages.md)
1. [Messages consumed by Rules service from `ccx-XXX-insights-operator-archive-synced` topic](internal-pipeline/insights_operator_archive_synced_rules_service.md)
1. [Messages consumed by Features service from `ccx-XXX-insights-operator-archive-synced` topic](internal-pipeline/insights_operator_archive_synced_features_service.md)
1. [Messages produced by Rules service](internal-pipeline/rules_service_messages.md)
1. [Messages produced by Features service](internal-pipeline/features_service_messages.md)
1. [Messages consumed from `ccx-XXX-insights-operator-archive-rules-results` topic](internal-pipeline/parquet_rules_results.md)
1. [Messages consumed from `ccx-XXX-insights-operator-archive-features` topic](internal-pipeline/parquet_features.md)
1. [Generated parquet files](internal-pipeline/parquet_output.md)

### Parquet factory

Parquet Factory is a program that can read data from several data sources,
aggregate the data received from them and generate a set of Parquet files with
the aggregated data, storing them in a S3 bucket. It is used to generate
different data aggregations in the CCX Internal Data Pipeline, reading data
from Kafka topics.

<img src="images/parquet-factory.png" alt="Parquet factory" usemap="#parquet-factory">
<map name="parquet-factory">
    <area shape="rect" coords="130, 34, 170, 64"   title="Messages consumed from ccx-XXX-insights-operator-archive-rules-results topic" alt="Messages consumed from ccx-XXX-insights-operator-archive-rules-results topic" href="internal-pipeline/parquet_rules_results.html">
    <area shape="rect" coords="130, 212, 170, 242" title="Messages consumed from ccx-XXX-insights-operator-archive-features topic" alt="Messages consumed from ccx-XXX-insights-operator-archive-features topic" href="internal-pipeline/parquet_features.html">
    <area shape="rect" coords="389, 165, 429, 195" title="Generated parquet files" alt="Generated parquet files" href="internal-pipeline/parquet_output.html">
</map>

1. [Messages consumed from `ccx-XXX-insights-operator-archive-rules-results` topic](internal-pipeline/parquet_rules_results.md)
2. [Messages consumed from `ccx-XXX-insights-operator-archive-features` topic](internal-pipeline/parquet_features.md)
3. [Generated parquet files](internal-pipeline/parquet_output.md)
