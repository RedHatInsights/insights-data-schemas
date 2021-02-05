# OCP results written into RDS

## Schema version

1 (unofficial)

## Description

OCP results are consumed from the Kafka topic named `ccx.ocp.results`, all data
are validated and then stored in RDS, i.e. PostgreSQL instance hosted in AWS.
The database schema is minimalistic at this moment as just three tables are
used to store reports, table rules, and error keys.

## Table `report`

This table is used as a cache for reports consumed from broker. Size of this
table (i.e. number of records) scales linearly with the number of clusters,
because only latest report for given cluster is stored (it is guarantied by DB
constraints). That table has defined compound key `org_id+cluster`,
additionally `cluster` name needs to be unique across all organizations.
Additionally `kafka_offset` is used to speedup consuming messages from Kafka
topic in case the offset is lost due to issues in Kafka, Kafka library, or
the service itself (messages with lower offset are skipped):

```sql
CREATE TABLE report (
    org_id          INTEGER NOT NULL,
    cluster         VARCHAR NOT NULL UNIQUE,
    report          VARCHAR NOT NULL,
    reported_at     TIMESTAMP,
    last_checked_at TIMESTAMP,
    kafka_offset    BIGINT NOT NULL DEFAULT 0,
    PRIMARY KEY(org_id, cluster)
)
```

## Table `rule` and rule_error_key

This table represents the content for Insights rules to be displayed by OCM.
The table `rule` represents more general information about the rule, whereas
the `rule_error_key` contains information about the specific type of error
which occurred. The combination of these two create an unique rule.

Very trivialized example could be:

* rule "REQUIREMENTS_CHECK"
  * error_key "REQUIREMENTS_CHECK_LOW_MEMORY"
  * error_key "REQUIREMENTS_CHECK_MISSING_SYSTEM_PACKAGE"

```sql
CREATE TABLE rule (
    module      VARCHAR PRIMARY KEY,
    name        VARCHAR NOT NULL,
    summary     VARCHAR NOT NULL,
    reason      VARCHAR NOT NULL,
    resolution  VARCHAR NOT NULL,
    more_info   VARCHAR NOT NULL
)
```

## Table `rule_error_key`

```sql
CREATE TABLE rule_error_key (
    error_key       VARCHAR NOT NULL,
    rule_module     VARCHAR NOT NULL REFERENCES rule(module),
    condition       VARCHAR NOT NULL,
    description     VARCHAR NOT NULL,
    impact          INTEGER NOT NULL,
```
