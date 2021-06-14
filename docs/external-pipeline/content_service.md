---
layout: default
---
\[[Front page](../index.md)\] \[[External data pipeline](../external_data_pipeline.md)\]

# Rule content produced by Content Service

## Schema version

1 (unofficial)

## Description

Rule content produced by the Content Service is being consumed regularly by a
Smart Proxy. The static content is taken from the memory cache and send in
`gob` format (it is much faster than to use JSON encoding). More information
about `gob` format is available at https://golang.org/pkg/encoding/gob/

## Possible enhancements

Version (positive integer) should be included in the message available via REST
API (in `gob` format) so the schema change will be possible w/o breaking other
services and tools.

## Basic format

Because `gob` format is used, the schema description is made using the standard
Go programming language type definitions:

### `RuleContent`

```go
// RuleContent wraps all the content available for a rule into a single structure.
type RuleContent struct {
	Summary    string                         `json:"summary"`
	Reason     string                         `json:"reason"`
	Resolution string                         `json:"resolution"`
	MoreInfo   string                         `json:"more_info"`
	Plugin     RulePluginInfo                 `json:"plugin"`
	ErrorKeys  map[string]RuleErrorKeyContent `json:"error_keys"`
	HasReason  bool
}
```

### `RulePluginInfo`

```go
// RulePluginInfo is a Go representation of the `plugin.yaml`
// file inside of the rule content directory.
type RulePluginInfo struct {
	Name         string `yaml:"name" json:"name"`
	NodeID       string `yaml:"node_id" json:"node_id"`
	ProductCode  string `yaml:"product_code" json:"product_code"`
	PythonModule string `yaml:"python_module" json:"python_module"`
}
```

### `RuleErrorKeyContent`

```go
// RuleErrorKeyContent wraps content of a single error key.
type RuleErrorKeyContent struct {
	Generic   string           `json:"generic"`
	Metadata  ErrorKeyMetadata `json:"metadata"`
	TotalRisk int              `json:"total_risk"`
	Reason    string           `json:"reason"`
	HasReason bool
}
```

### `ErrorKeyMetadata`

```go
// ErrorKeyMetadata is a Go representation of the `metadata.yaml`
// file inside of an error key content directory.
type ErrorKeyMetadata struct {
	Description string   `yaml:"description" json:"description"`
	Impact      string   `yaml:"impact" json:"impact"`
	Likelihood  int      `yaml:"likelihood" json:"likelihood"`
	PublishDate string   `yaml:"publish_date" json:"publish_date"`
	Status      string   `yaml:"status" json:"status"`
	Tags        []string `yaml:"tags" json:"tags"`
}
```
