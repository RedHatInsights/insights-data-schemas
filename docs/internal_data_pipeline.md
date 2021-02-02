---
layout: default
---
# Insights Data Schemas

## Internal data pipeline

<img src="images/internal-data-pipeline-architecture.png" alt="Internal data pipeline" usemap="#internal-pipeline">

[Incoming messages from SQS](incoming_sqs_messages.md)

### Parquet factory

<img src="images/parquet-factory.png" alt="Parquet factory" usemap="#parquet-factory">
<map name="parquet-factory">
    <area shape="rect" coords="130, 34, 170, 64"   title="Messages consumed from ccx-XXX-insights-operator-archive-rules-results topic" alt="Messages consumed from ccx-XXX-insights-operator-archive-rules-results topic" href="parquet_rules_results.html">
    <area shape="rect" coords="130, 212, 170, 242" title="Messages consumed from ccx-XXX-insights-operator-archive-features topic" alt="Messages consumed from ccx-XXX-insights-operator-archive-features topic" href="parquet_features.html">
    <area shape="rect" coords="295, 83, 335, 114"  title="Data consumed from Thanos" alt="Data consumed from Thanos" href="parquet_thanos.html">
    <area shape="rect" coords="389, 165, 429, 195" title="Generated parquet files" alt="Generated parquet files" href="parquet_output.md">
</map>

[Messages consumed from `ccx-XXX-insights-operator-archive-rules-results` topic](parquet_rules_results.md)
[Messages consumed from `ccx-XXX-insights-operator-archive-features` topic](parquet_features.md)
[Data consumed from Thanos](parquet_thanos.md)
[Generated parquet files](parquet_output.md)
