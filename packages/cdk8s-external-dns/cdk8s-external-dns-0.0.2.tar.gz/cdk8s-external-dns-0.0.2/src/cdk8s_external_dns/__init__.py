"""
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
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import constructs


class AwsExternalDns(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk8s-external-dns.AwsExternalDns",
):
    """Generate external-dns config yaml.

    see https://github.com/kubernetes-sigs/external-dns/blob/master/docs/tutorials/aws.md
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        domain_filter: builtins.str,
        aws_zone_type: typing.Optional["AwsZoneTypeOptions"] = None,
        image: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        service_account_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param domain_filter: will make ExternalDNS see only the hosted zones matching provided domain, omit to process all available hosted zones. Default: - none
        :param aws_zone_type: will make ExternalDNS see only the hosted zones matching provided domain, omit to process all available hosted zones. Default: - AwsZoneTypeOptions.PUBLIC = public
        :param image: image for external-dns. Default: - k8s.gcr.io/external-dns/external-dns:v0.7.3
        :param namespace: Namespace for external-dns. Default: - default
        :param service_account_name: Service Account Name for external-dns. Default: - external-dns
        """
        options = AwsExternalDnsOptions(
            domain_filter=domain_filter,
            aws_zone_type=aws_zone_type,
            image=image,
            namespace=namespace,
            service_account_name=service_account_name,
        )

        jsii.create(AwsExternalDns, self, [scope, id, options])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="awsZoneType")
    def aws_zone_type(self) -> "AwsZoneTypeOptions":
        """will make ExternalDNS see only the hosted zones matching provided domain, omit to process all available hosted zones.

        :default: - AwsZoneTypeOptions.PUBLIC = public
        """
        return jsii.get(self, "awsZoneType")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="deploymentName")
    def deployment_name(self) -> builtins.str:
        """Kubernetes Deployment Name for external-dns."""
        return jsii.get(self, "deploymentName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="image")
    def image(self) -> builtins.str:
        """image for external-dns.

        :default: - k8s.gcr.io/external-dns/external-dns:v0.7.3
        """
        return jsii.get(self, "image")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        """Namespace for external-dns.

        :default: - default
        """
        return jsii.get(self, "namespace")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="serviceAccountName")
    def service_account_name(self) -> builtins.str:
        """Service Account Name for external-dns."""
        return jsii.get(self, "serviceAccountName")


@jsii.data_type(
    jsii_type="cdk8s-external-dns.AwsExternalDnsOptions",
    jsii_struct_bases=[],
    name_mapping={
        "domain_filter": "domainFilter",
        "aws_zone_type": "awsZoneType",
        "image": "image",
        "namespace": "namespace",
        "service_account_name": "serviceAccountName",
    },
)
class AwsExternalDnsOptions:
    def __init__(
        self,
        *,
        domain_filter: builtins.str,
        aws_zone_type: typing.Optional["AwsZoneTypeOptions"] = None,
        image: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        service_account_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param domain_filter: will make ExternalDNS see only the hosted zones matching provided domain, omit to process all available hosted zones. Default: - none
        :param aws_zone_type: will make ExternalDNS see only the hosted zones matching provided domain, omit to process all available hosted zones. Default: - AwsZoneTypeOptions.PUBLIC = public
        :param image: image for external-dns. Default: - k8s.gcr.io/external-dns/external-dns:v0.7.3
        :param namespace: Namespace for external-dns. Default: - default
        :param service_account_name: Service Account Name for external-dns. Default: - external-dns
        """
        self._values: typing.Dict[str, typing.Any] = {
            "domain_filter": domain_filter,
        }
        if aws_zone_type is not None:
            self._values["aws_zone_type"] = aws_zone_type
        if image is not None:
            self._values["image"] = image
        if namespace is not None:
            self._values["namespace"] = namespace
        if service_account_name is not None:
            self._values["service_account_name"] = service_account_name

    @builtins.property
    def domain_filter(self) -> builtins.str:
        """will make ExternalDNS see only the hosted zones matching provided domain, omit to process all available hosted zones.

        :default: - none

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            -mydomain.com
        """
        result = self._values.get("domain_filter")
        assert result is not None, "Required property 'domain_filter' is missing"
        return result

    @builtins.property
    def aws_zone_type(self) -> typing.Optional["AwsZoneTypeOptions"]:
        """will make ExternalDNS see only the hosted zones matching provided domain, omit to process all available hosted zones.

        :default: - AwsZoneTypeOptions.PUBLIC = public
        """
        result = self._values.get("aws_zone_type")
        return result

    @builtins.property
    def image(self) -> typing.Optional[builtins.str]:
        """image for external-dns.

        :default: - k8s.gcr.io/external-dns/external-dns:v0.7.3
        """
        result = self._values.get("image")
        return result

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        """Namespace for external-dns.

        :default: - default
        """
        result = self._values.get("namespace")
        return result

    @builtins.property
    def service_account_name(self) -> typing.Optional[builtins.str]:
        """Service Account Name for external-dns.

        :default: - external-dns
        """
        result = self._values.get("service_account_name")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsExternalDnsOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AwsExternalDnsPolicyHelper(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk8s-external-dns.AwsExternalDnsPolicyHelper",
):
    """Aws External Dns Policy class ,help you add policy to your Iam Role for service account."""

    def __init__(self) -> None:
        jsii.create(AwsExternalDnsPolicyHelper, self, [])

    @jsii.member(jsii_name="addPolicy")
    @builtins.classmethod
    def add_policy(cls, role: typing.Any) -> typing.Any:
        """
        :param role: -
        """
        return jsii.sinvoke(cls, "addPolicy", [role])


@jsii.enum(jsii_type="cdk8s-external-dns.AwsZoneTypeOptions")
class AwsZoneTypeOptions(enum.Enum):
    PUBLIC = "PUBLIC"
    """will make ExternalDNS see only the hosted zones matching provided domain, omit to process all available hosted zones."""
    PRIVATE = "PRIVATE"
    """will make ExternalDNS see only the hosted zones matching provided domain, omit to process all available hosted zones."""


__all__ = [
    "AwsExternalDns",
    "AwsExternalDnsOptions",
    "AwsExternalDnsPolicyHelper",
    "AwsZoneTypeOptions",
]

publication.publish()
