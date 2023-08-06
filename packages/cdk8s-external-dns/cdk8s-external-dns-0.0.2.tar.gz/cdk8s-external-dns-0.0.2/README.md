[![NPM version](https://badge.fury.io/js/cdk8s-external-dns.svg)](https://badge.fury.io/js/cdk8s-external-dns)
[![PyPI version](https://badge.fury.io/py/cdk8s-external-dns.svg)](https://badge.fury.io/py/cdk8s-external-dns)
![Release](https://github.com/guan840912/cdk8s-external-dns/workflows/Release/badge.svg)

![Downloads](https://img.shields.io/badge/-DOWNLOADS:-brightgreen?color=gray)
![npm](https://img.shields.io/npm/dt/cdk8s-external-dns?label=npm&color=orange)
![PyPI](https://img.shields.io/pypi/dm/cdk8s-external-dns?label=pypi&color=blue)

# cdk8s-external-dns

> [cdk8s external dns](https://github.com/kubernetes-sigs/external-dns) constructs for cdk8s

Basic implementation of a [external dns](https://github.com/kubernetes-sigs/external-dns) construct for cdk8s. Contributions are welcome!

## Usage

### CDK External Dns

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk8s import App, Chart
from constructs import Construct
from cdk8s_external_dns import AwsExternalDns, AwsZoneTypeOptions

# default will deploy to default namespace.
class MyChart(Chart):
    def __init__(self, scope, name):
        super().__init__(scope, name)
        AwsExternalDns(self, "cdk8sAwsExternalDns",
            domain_filter="exmaple.com",
            aws_zone_type=AwsZoneTypeOptions.PUBLIC
        )
app = App()
MyChart(app, "testcdk8s")
app.synth()
```

# Featrue For Add IAM Policy.

* For IRSA add IAM Policy.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# CDK APP like eks_cluster.ts
from cdk8s_external_dns import AwsExternalDnsPolicyHelper
import aws_cdk.aws_eks as eks
cluster = eks.Cluster(self, "MyK8SCluster",
    default_capacity=0,
    masters_role=cluster_admin,
    version=eks.KubernetesVersion.V1_18
)

external_dns_service_account = cluster.add_service_account("external-dns",
    name="external-dns"
)

# will help you add policy to IAM Role .
AwsExternalDnsPolicyHelper.add_policy(external_dns_service_account)
```

Also can see [example repo](https://github.com/guan840912/cdk8s-cdk-example)

## License

Distributed under the [Apache 2.0](./LICENSE) license.
