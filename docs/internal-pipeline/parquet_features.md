---
layout: default
---
\[[Front page](../index.md)\] \[[Internal data pipeline](../internal_data_pipeline.md)\]

# Format of received Kafka messages from `ccx-XXX-insights-operator-archive-features` topic

Parquet Factory is a program that can read data from several data sources,
aggregate the data received from them and generate a set of Parquet files with
the aggregated data, storing them in a selected S3 or Ceph bucket. It is used
to generate different data aggregations in the CCX Internal Data Pipeline,
reading data from Kafka topics and Thanos service.

## Schema version

1 (unofficial)

## Description

Parquet factory reads (among other data) messages from Kafka topic named
`ccx-XXX-insights-operator-archive-features` where `XXX` needs to be replaced
by environment (`prod` etc.). These messages are represented as a structured
JSON format with many attributes that are described in more details below.

## Basic format

Data consumed from `ccx-XXX-insights-operator-archive-features` topic is
represented in JSON format with the following three top-level required
attributes (all of them are mandatory):

* `path` (URL)
* `metadata` (sub-node with two attributes described below)
* `report` (nested JSON-like structure that contains results of rule execution)

An example (simplified):

```JSON
{
  "path": "archives/compressed/aa/aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee/202101/20/031044.tar.gz",
  "metadata": {
     ...
     ...
     ...
  },
  "report": [
     ...
     ...
     ...
  ]
}
```

## Format of the `path` node

This attribute contains a string that represents path to a gzipped tarball
stored in Ceph bucket. Usually the path starts by `archives/compressed`
followed by first two digits of cluster ID, then full cluster ID, and a name of
gzipped tarball.

An example:

```JSON
{
  "path": "archives/compressed/aa/aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee/202101/20/031044.tar.gz",
  ...
  ...
  ...
}
```

## Format of the `metadata` node

This attribute contains two sub-nodes:

* `cluster_id` (string) cluster ID represented as UUID
* `external_organization` (string) organization ID represented as a string (not integer)

---
**NOTE**

`ClusterName` uses its canonical textual representation: the 16 octets of a
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

## Format of the `report` node

`report` node is represented as a list (or rather an array) of zero or more
items. These items represent the result of the execution of each rule configured
in the "feature extraction service", so their format will depend on the defined
for each rule.

Each item has the following attributes:

* `metadata` (dictionary)
* `schema` (dictionary)
* `data` (list of dictionaries)

These two dictionaries are described below.

### Format of `metadata` sub-node

This sub-node contains just two attributes:

* `feature_id` (string) unique identifier of a feature
* `component` (string) component, which is basically a name of feature code

### Format of `schema` sub-node

This sub-node contains two attributes:

* `version` (string) schema version, for example "1.0"
* `fields` (list of dictionaries) specification of data fields

Each item in `fields` list (array) contains field name and field type:

* `name` (string) field name
* `type` (string) field type, for example "String", "DateTime", or "Float"

An example - schema with three fields, each having different name and type:

```JSON
"schema": {
  "version": "1.0",
  "fields": [
    {
      "name": "cluster_id",
      "type": "String"
    },
    {
      "name": "value",
      "type": "Float"
    },
    {
      "name": "last_transition_time",
      "type": "DateTime"
    }
  ]
}
```

### Format of `data` sub-node

This sub-node contains a list of data fields with extracted features. Each item
in this list is represented as a dictionary with N key-value pairs where N is
equal to number of items in `fields` list mentioned above. An example (for the
example schema with three fields mentioned before):

```JSON
"data": [
  {
    "cluster_id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
    "value": 123,
    "last_transition_time": "2021-01-20T01:03:27"
  },
  {
    "cluster_id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
    "value": 0,
    "last_transition_time": "2021-01-20T01:03:29"
  }
]
```

## Current rules schemas


### `cluster_info` result schema

```JSON
{
  "version": "1.0",
  "fields": [
    {
      "name": "cluster_id",
      "type": "String"
    },
    {
      "name": "platform",
      "type": "String"
    },
    {
      "name": "network_type",
      "type": "String"
    },
    {
      "name": "channel",
      "type": "String"
    },
    {
      "name": "initial_version",
      "type": "String"
    },
    {
      "name": "current_version",
      "type": "String"
    },
    {
      "name": "desired_version",
      "type": "String"
    },
    {
      "name": "installed_at",
      "type": "DateTime"
    },
    {
      "name": "failing_since",
      "type": "DateTime"
    },
    {
      "name": "upgrading_since",
      "type": "DateTime"
    },
    {
      "name": "last_y_upgrade_at",
      "type": "DateTime"
    },
    {
      "name": "last_z_upgrade_at",
      "type": "DateTime"
    },
    {
      "name": "analysis_time",
      "type": "DateTime"
    },
    {
      "name": "path",
      "type": "String"
    }
  ]
}
```

### `foc` result schema

```JSON
{
  "version": "1.0",
  "fields": [
    {
      "name": "cluster_id",
      "type": "String"
    },
    {
      "name": "operator",
      "type": "String"
    },
    {
      "name": "type",
      "type": "String"
    },
    {
      "name": "status",
      "type": "Boolean"
    },
    {
      "name": "last_transition_time",
      "type": "DateTime"
    },
    {
      "name": "reason",
      "type": "String"
    },
    {
      "name": "message",
      "type": "String"
    },
    {
      "name": "analysis_time",
      "type": "DateTime"
    },
    {
      "name": "path",
      "type": "String"
    }
  ]
}
```

### `alerts` result schema

```JSON
{
  "version": "1.0",
  "fields": [
    {
      "name": "cluster_id",
      "type": "String"
    },
    {
      "name": "name",
      "type": "String"
    },
    {
      "name": "state",
      "type": "String"
    },
    {
      "name": "severity",
      "type": "String"
    },
    {
      "name": "labels",
      "type": "Object"
    },
    {
      "name": "value",
      "type": "Float"
    },
    {
      "name": "last_transition_time",
      "type": "DateTime"
    },
    {
      "name": "analysis_time",
      "type": "DateTime"
    },
    {
      "name": "path",
      "type": "String"
    }
  ]
}
```

### `gatherers` result schema

```JSON
{
  "version": "1.0",
  "fields": [
    {
      "name": "cluster_id",
      "type": "String"
    },
    {
      "name": "name",
      "type": "String"
    },
    {
      "name": "duration_in_ms",
      "type": "Integer"
    },
    {
      "name": "analysis_time",
      "type": "DateTime"
    },
    {
      "name": "path",
      "type": "String"
    }
  ]
}
```

## Possible enhancements

Version (positive integer) should be included in messages as a new JSON
attribute.

## Examples

A message with just one field in `schema` sub-node and one item in `data` node:

```JSON
{
  "path": "archives/compressed/aa/aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee/202101/20/031044.tar.gz",
  "metadata": {
    "cluster_id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
    "external_organization": "1234567890"
  },
  "report": [
    {
      "metadata": {
        "feature_id": "feature_name",
        "component": "feature.component.identifier"
      },
      "schema": {
        "version": "1.0",
        "fields": [
          {
            "name": "cluster_id",
            "type": "String"
          }
        ]
      },
      "data": [
        {
          "cluster_id": "1d86b5c1-dec5-4ebe-a817-fab2b5500c8d",
        }
      ]
    }
  ]
}
```

A message with three fields in `schema` sub-node and two items in `data` node:

```JSON
{
  "path": "archives/compressed/aa/aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee/202101/20/031044.tar.gz",
  "metadata": {
    "cluster_id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
    "external_organization": "1234567890"
  },
  "report": [
    {
      "metadata": {
        "feature_id": "feature_name",
        "component": "feature.component.identifier"
      },
      "schema": {
        "version": "1.0",
        "fields": [
          {
            "name": "cluster_id",
            "type": "String"
          },
          {
            "name": "value",
            "type": "Float"
          },
          {
            "name": "last_transition_time",
            "type": "DateTime"
          }
        ]
      },
      "data": [
        {
          "cluster_id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
          "value": 123,
          "last_transition_time": "2021-01-20T01:03:27"
        },
        {
          "cluster_id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
          "value": 0,
          "last_transition_time": "2021-01-20T01:03:29"
        }
      ]
    }
  ]
}
```

`null` values are possible:

```JSON
{
  "path": "archives/compressed/aa/aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee/202101/20/031044.tar.gz",
  "metadata": {
    "cluster_id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
    "external_organization": "1234567890"
  },
  "report": [
    {
      "metadata": {
        "feature_id": "feature_name",
        "component": "feature.component.identifier"
      },
      "schema": {
        "version": "1.0",
        "fields": [
          {
            "name": "cluster_id",
            "type": "String"
          },
          {
            "name": "upgrading_since",
            "type": "DateTime"
          },
          {
            "name": "last_y_upgrade_at",
            "type": "DateTime"
          },
          {
            "name": "last_z_upgrade_at",
            "type": "DateTime"
          }
        ]
      },
      "data": [
        {
          "cluster_id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
          "upgrading_since": null,
          "last_y_upgrade_at": null,
          "last_z_upgrade_at": null,
        }
      ]
    }
  ]
}
```
