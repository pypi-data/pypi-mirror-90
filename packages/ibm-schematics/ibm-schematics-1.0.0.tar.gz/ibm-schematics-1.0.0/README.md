[![Build Status](https://travis-ci.com/IBM/schematics-python-sdk.svg?branch=master)](https://travis-ci.com/IBM/schematics-python-sdk)
[![semantic-release](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg)](https://github.com/semantic-release/semantic-release)
# IBM Cloud Schematics Python SDK

Python client library to interact with various [IBM Cloud Schematics APIs](https://cloud.ibm.com/apidocs?category=schematics).

Disclaimer: this SDK is being released initially as a **pre-release** version.
Changes might occur which impact applications that use this SDK.

## Table of Contents

<!--
  The TOC below is generated using the `markdown-toc` node package.

      https://github.com/jonschlinkert/markdown-toc

  You should regenerate the TOC after making changes to this file.

      npx markdown-toc -i README.md
  -->

<!-- toc -->

- [IBM Cloud Schematics Python SDK](#ibm-cloud-schematics-python-sdk)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Authentication](#authentication)
    - [Authenticate with environment variables](#authenticate-with-environment-variables)
    - [Authenticate with external configuration](#authenticate-with-external-configuration)
    - [Authenticate programmatically](#authenticate-programmatically)
  - [Getting Started](#getting-started)
  - [Error handling](#error-handling)
  - [Using the SDK](#using-the-sdk)
  - [Questions](#questions)
  - [Issues](#issues)
  - [Open source @ IBM](#open-source--ibm)
  - [Contributing](#contributing)
  - [License](#license)

<!-- tocstop -->

## Overview

The IBM Cloud Schematics Python SDK allows developers to programmatically interact with the following
IBM Cloud services:

Service Name | Imported Class Name
--- | ---
[Schematics](https://cloud.ibm.com/apidocs/schematics) | schematicsv1 

## Prerequisites

[ibm-cloud-onboarding]: https://cloud.ibm.com/registration

* An [IBM Cloud][ibm-cloud-onboarding] account.
* An IAM API key to allow the SDK to access your account. Create one [here](https://cloud.ibm.com/iam/apikeys).
* Python 3.5.3 or above.

## Installation

To install, use `pip` or `easy_install`:

```bash
pip install --upgrade "ibm-schematics>=1.0.0"
```

or

```bash
easy_install --upgrade "ibm-schematics>=1.0.0"
```

## Authentication

The library requires Identity and Access Management (IAM) to authenticate requests. There are several ways to set the properties for authentication

1. [As environment variables](#authenticate-with-environment-variables)
2. [The programmatic approach](#authenticate-programmatically)
3. [With an external credentials file](#authenticate-with-external-configuration)

### Authenticate with environment variables

For Schematics IAM authentication set the following environmental variables by replacing <apikey> with your proper service credentials.

```
SCHEMATICS_URL = https://schematics.cloud.ibm.com
SCHEMATICS_APIKEY = <apikey>
```

### Authenticate with external configuration

To use an external configuration file, see the related documentation in the [Python SDK Core document about authentication](https://github.com/IBM/ibm-cloud-sdk-common/blob/master/README.md).

### Authenticate programmatically

To learn more about how to use programmatic authentication, see the related documentation in the [Python SDK Core document about authentication](https://github.com/IBM/ibm-cloud-sdk-common/blob/master/README.md).

## Getting Started

A quick example to get you up and running with Schematics Python SDK service

```

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_schematics.schematics_v1 import SchematicsV1

authenticator = IAMAuthenticator('<apiKey>')
schematics_service = SchematicsV1(authenticator = authenticator)
schematics_service.set_service_url('https://schematics.cloud.ibm.com')

get_schematics_version_response = schematics_service.get_schematics_version()
version_response = get_schematics_version_response.get_result()
print(version_response)


```

## Error handling

For sample code on handling errors, please see [Schematics API docs](https://cloud.ibm.com/apidocs/schematics#error-handling).

## Using the SDK
For general SDK usage information, please see [this link](https://github.com/IBM/ibm-cloud-sdk-common/blob/master/README.md)

## Questions

If you are having difficulties using this SDK or have a question about the IBM Cloud services,
please ask a question
[Stack Overflow](http://stackoverflow.com/questions/ask?tags=ibm-cloud).

## Issues
If you encounter an issue with the project, you are welcome to submit a
[bug report](https://github.com/IBM/schematics-python-sdk.git/issues).
Before that, please search for similar issues. It's possible that someone has already reported the problem.

## Open source @ IBM
Find more open source projects on the [IBM Github Page](http://ibm.github.io/)

## Contributing
See [CONTRIBUTING.md](https://github.com/IBM/schematics-python-sdk.git/blob/master/CONTRIBUTING.md).

## License

This SDK is released under the Apache 2.0 license.
The license's full text can be found in [LICENSE](https://github.com/IBM/schematics-python-sdk.git/blob/master/LICENSE).
