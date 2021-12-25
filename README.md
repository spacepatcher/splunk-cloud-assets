[![Python 3.9.9](https://img.shields.io/badge/python-3.9.9-blue.svg)](https://www.python.org/downloads/release/python-399/)

## splunk-cloud-assets

### About

This repository contains Splunk input scripts to collect assets from cloud providers:

- Aliyun
- AWS (only Amazon Route 53)
- Cloudflare

I focus on gathering information about assets that are accessable from Internet. Аny information about vulnerabilities interests me as well.

### Cloud API

List of API functions used to collect data from cloud providers.

Aliyun:
- `DescribeCloudCenterInstances`
- `DescribeGroupedContainerInstances`
- `DescribeDomainList`
- `DescribeDomainDetail`
- `DescribeExposedInstanceList`
- `DescribeAllEntity`
- `DescribeVulList`

AWS (only Amazon Route 53):
- `ListHostedZones`
- `ListResourceRecordSets`

Cloudflare:
- `ListZones`


### Usage

As already mentioned, the scripts are designed primarily as Splunk data inputs.

Bash wrappers are used to activate Python environment and pass parameters to the startup. Wrappers with parameters are set in Splunk when creating a new local script input.

But nothing prevents you from using scripts separately from Splunk.

**Init**

Replace these lines in Python scripts with secrets for accessing cloud accounts:

- `<ALI_KEY>`
- `<ALI_SECRET>`
- `<AWS_ID>`
- `<AWS_KEY>`
- `<CF_EMAIL>`
- `<CF_TOKEN>`
