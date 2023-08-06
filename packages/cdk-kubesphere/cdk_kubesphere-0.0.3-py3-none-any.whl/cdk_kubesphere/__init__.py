"""
[![NPM version](https://badge.fury.io/js/cdk-kubesphere.svg)](https://badge.fury.io/js/cdk-kubesphere)
[![PyPI version](https://badge.fury.io/py/cdk-kubesphere.svg)](https://badge.fury.io/py/cdk-kubesphere)
![Release](https://github.com/pahud/cdk-kubesphere/workflows/Release/badge.svg)

# cdk-kubesphere

**cdk-kubesphere** is a CDK construct library that allows you to create [KubeSphere](https://kubesphere.io/) on AWS with CDK in TypeScript, JavaScript or Python.

# Sample

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
imoprtKubeSpherefrom"cdk-kubesphere"

app = cdk.App()

stack = cdk.Stack(app, "cdk-kubesphere-demo")

# deploy a default KubeSphere service on a new Amazon EKS cluster
KubeSphere(stack, "KubeSphere")
```

# Console

Run the following command to create a `port-forward` from localhost:8888 to `ks-console:80`

```sh
kubectl -n kubesphere-system port-forward service/ks-console 8888:80
```

Open `http://localhost:8888` and enter the default username/password(`admin/P@88w0rd`) to enter the admin console.
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

import aws_cdk.aws_eks
import aws_cdk.core


class KubeSphere(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-kubesphere.KubeSphere",
):
    """The KubeSphere workload."""

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        cluster: typing.Optional[aws_cdk.aws_eks.ICluster] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param cluster: The existing Amazon EKS cluster(if any).
        """
        props = KubeSphereProps(cluster=cluster)

        jsii.create(KubeSphere, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-kubesphere.KubeSphereProps",
    jsii_struct_bases=[],
    name_mapping={"cluster": "cluster"},
)
class KubeSphereProps:
    def __init__(
        self,
        *,
        cluster: typing.Optional[aws_cdk.aws_eks.ICluster] = None,
    ) -> None:
        """The construct properties for KubeSphere.

        :param cluster: The existing Amazon EKS cluster(if any).
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if cluster is not None:
            self._values["cluster"] = cluster

    @builtins.property
    def cluster(self) -> typing.Optional[aws_cdk.aws_eks.ICluster]:
        """The existing Amazon EKS cluster(if any)."""
        result = self._values.get("cluster")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubeSphereProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "KubeSphere",
    "KubeSphereProps",
]

publication.publish()
