"""
# antenny-cdk

antenny-cdk is a cloud development kit construct library for Antenny. It provides a way to integrate Antenny into your cdk infrastructure.

## Installation

#### npm

```shell
npm install antenny-cdk --save
```

#### pip

```shell
pip install antenny-cdk
```

#### nuget

```shell
dotnet add package Antenny.Cdk
```
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

import aws_cdk.core


@jsii.interface(jsii_type="antenny-cdk.IResourceProps")
class IResourceProps(typing_extensions.Protocol):
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IResourcePropsProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        ...


class _IResourcePropsProxy:
    __jsii_type__: typing.ClassVar[str] = "antenny-cdk.IResourceProps"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return jsii.get(self, "protocol")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return jsii.get(self, "url")


@jsii.interface(jsii_type="antenny-cdk.ISubscription")
class ISubscription(typing_extensions.Protocol):
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ISubscriptionProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="customerId")
    def customer_id(self) -> builtins.str:
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> IResourceProps:
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="resource")
    def resource(self) -> IResourceProps:
        ...


class _ISubscriptionProxy:
    __jsii_type__: typing.ClassVar[str] = "antenny-cdk.ISubscription"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="customerId")
    def customer_id(self) -> builtins.str:
        return jsii.get(self, "customerId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> IResourceProps:
        return jsii.get(self, "endpoint")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return jsii.get(self, "name")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return jsii.get(self, "region")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="resource")
    def resource(self) -> IResourceProps:
        return jsii.get(self, "resource")


@jsii.interface(jsii_type="antenny-cdk.ISubscriptionProps")
class ISubscriptionProps(typing_extensions.Protocol):
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ISubscriptionPropsProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="apiKey")
    def api_key(self) -> builtins.str:
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="subscription")
    def subscription(self) -> ISubscription:
        ...


class _ISubscriptionPropsProxy:
    __jsii_type__: typing.ClassVar[str] = "antenny-cdk.ISubscriptionProps"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="apiKey")
    def api_key(self) -> builtins.str:
        return jsii.get(self, "apiKey")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="subscription")
    def subscription(self) -> ISubscription:
        return jsii.get(self, "subscription")


class Subscription(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="antenny-cdk.Subscription",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        props: ISubscriptionProps,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        """
        jsii.create(Subscription, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> aws_cdk.core.Reference:
        return jsii.get(self, "attrId")

    @attr_id.setter # type: ignore
    def attr_id(self, value: aws_cdk.core.Reference) -> None:
        jsii.set(self, "attrId", value)


__all__ = [
    "IResourceProps",
    "ISubscription",
    "ISubscriptionProps",
    "Subscription",
]

publication.publish()
