---
layout: default
---
\[[Front page](../index.md)\] \[[Internal data pipeline](../internal_data_pipeline.md)\]

# Raw data stored into Ceph bucket (OLS)

Archive Sync OLS Service synchronizes every new archive by reading the related
information from `[qa|prod]-ols-archive-new` Kafka topic, downloading the
archive from AWS S3 and uploading it to Internal Ceph bucket.

## Schema version

1 (unofficial)

## Description

Archive containing data gathered by Openshift Lightspeed from cluster.

## Basic format

The only relevant file in the Openshift Lightspeed archives is the 
`openshift_lightspeed.json` in the root of the archive.
