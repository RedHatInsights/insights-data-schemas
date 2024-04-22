---
layout: default
---
\[[Front page](../index.md)\] \[[Internal data pipeline](../internal_data_pipeline.md)\]

# Messages produced by Rules service

Rules Service runs rules for all archives synced in DataHub (Ceph) bucket. It
reads messages from `[qa|prod]-archive-synced` Kafka topic to know about incoming
archives in Ceph and it will download the archive from DataHub (Ceph) bucket.

The result of the applied rules is sent to `[qa|prod]-insights-rules-results` Kafka
topic.

## Schema version

1 (unofficial)

## Description

Rules service constructs messages and produces them into topic named
`[qa|prod]-insights-rules-results`. These messages are represented as a
structured JSON format with many attributes that are described in more details
below.

## Basic format

Data produced into `[qa|prod]-insights-rules-results` topic is in JSON format
with the following three top-level required attributes (all of them are mandatory):

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
  "report": {
     ...
     ...
     ...
  }
}
```
## Format of the `path` node

This attribute contains a string that represents path to a gzipped tarball
stored in Ceph bucket. Usually the path starts by `archives/compressed`
followed by first two digits of cluster ID, then full cluster ID, and a name
of gzipped tarball.

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

An example:

```JSON
  "metadata": {
    "cluster_id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
    "external_organization": "1234567890"
  }
```

---
**NOTE**

`ClusterName` uses its canonical textual representation: the 16 octets of a
UUID are represented as 32 hexadecimal (base-16) digits, displayed in five
groups separated by hyphens, in the form 8-4-4-4-12 for a total of 36
characters (32 hexadecimal characters and 4 hyphens).

An example of UUID:

```
3ba9b042-b8b8-4714-98e9-17915c2eeb95
```

---

## Format of the `report` node

The generated cluster reports from Insights results contain three lists of
rules that were either __skipped__ (because of missing requirements, etc.),
__passed__ (the rule got executed but no issue was found), or __hit__ (the
rule got executed and found the issue it was looking for) by the cluster,
where each rule is represented as a dictionary containing identifying
information about the rule itself (actually __hit__ rules are stored in
`reports` attribute).

`Report` node is represented as a standard JSON dictionary with following four required attributes:

* `system`: additional information about the cluster
* `reports`: list of rules that detect any problem on given cluster
* `skips`: list of rules that have been skipped because not all required information was available on checked cluster
* `pass`: list of rules that passes all conditions (i.e. rules without any problem/issue detected)
* `info`: list of rules that return info messages only 
* `fingerprints`: ?
* `analysis_metadata`: information about Insights Rules settings, context, and analysis duration 

### Format of `system` attribute in `Report` node

TBD (not used in internal data pipeline)

### Format of `reports` attribute in `Report` node

This attribute contains list of rules that detect any problem on given cluster.
Each element in the list is represented as a node with seven attributes:

* `rule_id`: rule name and a key
* `component`: fully-qualified name of the rule (unique)
* `type`: information that issue or issues have been detected by this rule
* `key`: a key that selects the variant of issue (one rule can detect more different issues)
* `tags`: tags assigned to the rule
* `links`: links to documentation, Knowledge Base article etc.

An example:

```json
        "reports": [
            {
                "rule_id": "tutorial_rule|TUTORIAL_ERROR",
                "component": "ccx_rules_ocp.external.tutorial_rule.report",
                "type": "rule",
                "key": "TUTORIAL_ERROR",
                "details": {
                    "type": "rule",
                    "error_key": "TUTORIAL_ERROR"
                },
                "tags": [],
                "links": {}
            }
        ]
```

### Format of `skips` attribute in `Report` node

This attribute contains list of rules that have been skipped because not all
required information was available on checked cluster. Each element in the list
is represented as a node with four attributes:

* `rule_fqdn`: fully-qualified name of the rule (unique)
* `reason`: reason why the rule was skipped
* `details`: detailed information about the rule and the condition to skip it
* `type`: information that this rule was skipped

An example:

```json
        "skips": [
            {
                "rule_fqdn": "ccx_rules_ocp.ocs.check_ocs_version.report",
                "reason": "MISSING_REQUIREMENTS",
                "details": "All: ['ccx_ocp_core.specs.must_gather_ocs.OperatorsOcsMGOCS'] Any: ",
                "type": "skip"
            },
            {
                "rule_fqdn": "ccx_rules_ocp.ocs.check_pods_scc.report",
                "reason": "MISSING_REQUIREMENTS",
                "details": "All: ['ccx_ocp_core.specs.must_gather_ocs.PodsMGOCS'] Any: ",
                "type": "skip"
            }
        ]
```

### Format of `pass` attribute in `Report` node

This attribute contains list of rules that passes all conditions (i.e. rules without any problem/issue detected)

### Format of `info` attribute in `Report` node

TBD

### Format of `fingerprints` attribute in `Report` node

TBD (not used in internal data pipeline)

### Minimal structure of `Report` node

`Report` node can contains attributes with empty values. Its minimal structure ca look like:

```json
{
    "Report": {
        "system": {
            "metadata": {},
            "hostname": null
        },
        "reports": [],
        "fingerprints": [],
        "skips": [],
        "info": [],
        "pass": []
    }
}
```

## Possible enhancements

Version (positive integer) should be included in messages as a new JSON
attribute.

## Examples

A typical message for a node "hit" just by so-called tutorial rule.
Additionally two other rules was skipped:

```json
{
    "path": "archives/compressed/aa/aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee/202101/20/031044.tar.gz",
    "metadata": {
      "cluster_id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
      "external_organization": "1234567890"
    },
    "Report": {
        "system": {
            "metadata": {},
            "hostname": null
        },
        "reports": [
            {
                "rule_id": "tutorial_rule|TUTORIAL_ERROR",
                "component": "ccx_rules_ocp.external.tutorial_rule.report",
                "type": "rule",
                "key": "TUTORIAL_ERROR",
                "details": {
                    "type": "rule",
                    "error_key": "TUTORIAL_ERROR"
                },
                "tags": [],
                "links": {}
            }
        ],
        "fingerprints": [],
        "skips": [
            {
                "rule_fqdn": "ccx_rules_ocp.ocs.check_ocs_version.report",
                "reason": "MISSING_REQUIREMENTS",
                "details": "All: ['ccx_ocp_core.specs.must_gather_ocs.OperatorsOcsMGOCS'] Any: ",
                "type": "skip"
            },
            {
                "rule_fqdn": "ccx_rules_ocp.ocs.check_pods_scc.report",
                "reason": "MISSING_REQUIREMENTS",
                "details": "All: ['ccx_ocp_core.specs.must_gather_ocs.PodsMGOCS'] Any: ",
                "type": "skip"
            },
        ],
        "info": [],
        "pass": []
    }
}
```
