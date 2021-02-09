---
layout: default
---
\[[Front page](../index.md)\] \[[Internal data pipeline](../internal_data_pipeline.md)\]

# Messages produced by archive-sync-service

Archive Sync Service synchronizes every new archive by reading the related
information from `ccx-XXX-insights-operator-archive-new` (where `XXX` needs to
be replaced by environment, for example `prod`) Kafka topic, downloading the
archive from AWS S3 and uploading it to DataHub (Ceph) bucket.

Information about synchronized archive and its metadata are sent to
`ccx-XXX-insights-operator-archive-synced` Kafka topic.

## Schema version

1 (unofficial)

## Description

Messages produced into `ccx-XXX-insights-operator-archive-synced` topic (where
`XXX` needs to be replaced by environment, for example `prod`) are created by
Archive Sync Service for each object stored into Ceph. These messages have very
simple format consisting of just three attributes:

* target_apth
* s3_path
* metadata


## Basic format

Messages are stored in JSON format and have to contain three attributes:

* `target_path` (string with path)
* `s3_path` (string with path)
* `metadata` (dictionary)


### `target_path` attribute

This attribute contains path to object stored in Ceph. It must be real path
with chunks splitted by slash character.

An example of path structure:

```
archives/compressed/$ORG_ID/$CLUSTER_ID/$YEAR$MONTH/$DAY/$TIME.tar.gz
```


### `s3_path` attribute

This attribute contains path to object stored in AWS S3. It must be real path
with chunks splitted by slash character.

An example of path:

```
1234567/abcd1234-1234-abcd-5678-1234abcd1234/20200609125740-1234567890abcdef1234567890abcdef
```

### `metadata` attribute

This attribute contains two required sub-nodes:

* `cluster_id` (string) cluster ID represented as UUID
* `external_organization` (string) organization ID represented as a string (not integer)

---
**NOTE**

`cluster_id` uses its canonical textual representation: the 16 octets of a
UUID are represented as 32 hexadecimal (base-16) digits, displayed in five
groups separated by hyphens, in the form 8-4-4-4-12 for a total of 36
characters (32 hexadecimal characters and 4 hyphens).  For more information
please look at
[https://en.wikipedia.org/wiki/Universally_unique_identifier](https://en.wikipedia.org/wiki/Universally_unique_identifier).

An example of UUID:

```
3ba9b042-b8b8-4714-98e9-17915c2eeb95
```

---

## Possible enhancements

It would be possible to add a schema version into generated messages in JSON
format.
