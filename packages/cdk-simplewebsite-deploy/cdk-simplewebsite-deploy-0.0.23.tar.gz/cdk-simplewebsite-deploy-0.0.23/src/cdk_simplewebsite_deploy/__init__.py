"""
[![License](https://img.shields.io/badge/License-Apache%202.0-yellowgreen.svg)](https://opensource.org/licenses/Apache-2.0)
![Build](https://github.com/SnapPetal/cdk-cloudfront-deploy/workflows/Build/badge.svg)
![Release](https://github.com/SnapPetal/cdk-cloudfront-deploy/workflows/Release/badge.svg)

# cdk-simplewebsite-deploy

This is an AWS CDK Construct to simplify deploying a single-page website use CloudFront distributions.

## Installation and Usage

```console
npm i cdk-simplewebsite-deploy
```

### [CreateBasicSite](https://github.com/snappetal/cdk-simplewebsite-deploy/blob/main/API.md#cdk-cloudfront-deploy-createbasicsite)

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.core as cdk
from cdk_simplewebsite_deploy import CreateBasicSite

class PipelineStack(cdk.Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        CreateBasicSite(stack, "test-website",
            website_folder="./src/build",
            index_doc="index.html",
            encrypt_bucket=True
        )
```

### [CreateCloudfrontSite](https://github.com/snappetal/cdk-simplewebsite-deploy/blob/main/API.md#cdk-cloudfront-deploy-createcloudfrontsite)

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.core as cdk
from cdk_simplewebsite_deploy import CreateCloudfrontSite

class PipelineStack(cdk.Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        CreateCloudfrontSite(stack, "test-website",
            website_folder="./src/dist",
            index_doc="index.html",
            hosted_zone_domain="example.com",
            website_domain="www.example.com"
        )
```

## License

Distributed under the [Apache-2.0](./LICENSE) license.
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

import aws_cdk.aws_cloudfront
import aws_cdk.core


@jsii.data_type(
    jsii_type="cdk-simplewebsite-deploy.BasicSiteConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "index_doc": "indexDoc",
        "website_folder": "websiteFolder",
        "encrypt_bucket": "encryptBucket",
        "error_doc": "errorDoc",
        "website_domain": "websiteDomain",
        "website_sub_domain": "websiteSubDomain",
    },
)
class BasicSiteConfiguration:
    def __init__(
        self,
        *,
        index_doc: builtins.str,
        website_folder: builtins.str,
        encrypt_bucket: typing.Optional[builtins.bool] = None,
        error_doc: typing.Optional[builtins.str] = None,
        website_domain: typing.Optional[builtins.str] = None,
        website_sub_domain: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param index_doc: the index docuement of your S3 Bucket.
        :param website_folder: local path to the website folder you want to deploy on S3.
        :param encrypt_bucket: enable encryption for files in your S3 Bucket.
        :param error_doc: the error document of your S3 Bucket.
        :param website_domain: the domain you want to deploy to.
        :param website_sub_domain: the subdomain you want to deploy to.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "index_doc": index_doc,
            "website_folder": website_folder,
        }
        if encrypt_bucket is not None:
            self._values["encrypt_bucket"] = encrypt_bucket
        if error_doc is not None:
            self._values["error_doc"] = error_doc
        if website_domain is not None:
            self._values["website_domain"] = website_domain
        if website_sub_domain is not None:
            self._values["website_sub_domain"] = website_sub_domain

    @builtins.property
    def index_doc(self) -> builtins.str:
        """the index docuement of your S3 Bucket."""
        result = self._values.get("index_doc")
        assert result is not None, "Required property 'index_doc' is missing"
        return result

    @builtins.property
    def website_folder(self) -> builtins.str:
        """local path to the website folder you want to deploy on S3."""
        result = self._values.get("website_folder")
        assert result is not None, "Required property 'website_folder' is missing"
        return result

    @builtins.property
    def encrypt_bucket(self) -> typing.Optional[builtins.bool]:
        """enable encryption for files in your S3 Bucket."""
        result = self._values.get("encrypt_bucket")
        return result

    @builtins.property
    def error_doc(self) -> typing.Optional[builtins.str]:
        """the error document of your S3 Bucket."""
        result = self._values.get("error_doc")
        return result

    @builtins.property
    def website_domain(self) -> typing.Optional[builtins.str]:
        """the domain you want to deploy to."""
        result = self._values.get("website_domain")
        return result

    @builtins.property
    def website_sub_domain(self) -> typing.Optional[builtins.str]:
        """the subdomain you want to deploy to."""
        result = self._values.get("website_sub_domain")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BasicSiteConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-simplewebsite-deploy.CloudfrontSiteConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "hosted_zone_domain": "hostedZoneDomain",
        "index_doc": "indexDoc",
        "website_domain": "websiteDomain",
        "website_folder": "websiteFolder",
        "encrypt_bucket": "encryptBucket",
        "error_doc": "errorDoc",
        "price_class": "priceClass",
    },
)
class CloudfrontSiteConfiguration:
    def __init__(
        self,
        *,
        hosted_zone_domain: builtins.str,
        index_doc: builtins.str,
        website_domain: builtins.str,
        website_folder: builtins.str,
        encrypt_bucket: typing.Optional[builtins.bool] = None,
        error_doc: typing.Optional[builtins.str] = None,
        price_class: typing.Optional[aws_cdk.aws_cloudfront.PriceClass] = None,
    ) -> None:
        """
        :param hosted_zone_domain: hosted zone used to create the DNS record of your CloudFront distribution.
        :param index_doc: the index docuement of your CloudFront distribution.
        :param website_domain: the domain you want to deploy to.
        :param website_folder: local path to the website folder you want to deploy on S3.
        :param encrypt_bucket: enable encryption for files in your S3 Bucket.
        :param error_doc: the error document of your CloudFront distribution.
        :param price_class: the price class determines how many edge locations CloudFront will use for your distribution. default value is PriceClass_100. See https://aws.amazon.com/cloudfront/pricing/ for full list of supported regions.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "hosted_zone_domain": hosted_zone_domain,
            "index_doc": index_doc,
            "website_domain": website_domain,
            "website_folder": website_folder,
        }
        if encrypt_bucket is not None:
            self._values["encrypt_bucket"] = encrypt_bucket
        if error_doc is not None:
            self._values["error_doc"] = error_doc
        if price_class is not None:
            self._values["price_class"] = price_class

    @builtins.property
    def hosted_zone_domain(self) -> builtins.str:
        """hosted zone used to create the DNS record of your CloudFront distribution."""
        result = self._values.get("hosted_zone_domain")
        assert result is not None, "Required property 'hosted_zone_domain' is missing"
        return result

    @builtins.property
    def index_doc(self) -> builtins.str:
        """the index docuement of your CloudFront distribution."""
        result = self._values.get("index_doc")
        assert result is not None, "Required property 'index_doc' is missing"
        return result

    @builtins.property
    def website_domain(self) -> builtins.str:
        """the domain you want to deploy to."""
        result = self._values.get("website_domain")
        assert result is not None, "Required property 'website_domain' is missing"
        return result

    @builtins.property
    def website_folder(self) -> builtins.str:
        """local path to the website folder you want to deploy on S3."""
        result = self._values.get("website_folder")
        assert result is not None, "Required property 'website_folder' is missing"
        return result

    @builtins.property
    def encrypt_bucket(self) -> typing.Optional[builtins.bool]:
        """enable encryption for files in your S3 Bucket."""
        result = self._values.get("encrypt_bucket")
        return result

    @builtins.property
    def error_doc(self) -> typing.Optional[builtins.str]:
        """the error document of your CloudFront distribution."""
        result = self._values.get("error_doc")
        return result

    @builtins.property
    def price_class(self) -> typing.Optional[aws_cdk.aws_cloudfront.PriceClass]:
        """the price class determines how many edge locations CloudFront will use for your distribution.

        default value is PriceClass_100.
        See https://aws.amazon.com/cloudfront/pricing/ for full list of supported regions.
        """
        result = self._values.get("price_class")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontSiteConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CreateBasicSite(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-simplewebsite-deploy.CreateBasicSite",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        index_doc: builtins.str,
        website_folder: builtins.str,
        encrypt_bucket: typing.Optional[builtins.bool] = None,
        error_doc: typing.Optional[builtins.str] = None,
        website_domain: typing.Optional[builtins.str] = None,
        website_sub_domain: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param index_doc: the index docuement of your S3 Bucket.
        :param website_folder: local path to the website folder you want to deploy on S3.
        :param encrypt_bucket: enable encryption for files in your S3 Bucket.
        :param error_doc: the error document of your S3 Bucket.
        :param website_domain: the domain you want to deploy to.
        :param website_sub_domain: the subdomain you want to deploy to.
        """
        props = BasicSiteConfiguration(
            index_doc=index_doc,
            website_folder=website_folder,
            encrypt_bucket=encrypt_bucket,
            error_doc=error_doc,
            website_domain=website_domain,
            website_sub_domain=website_sub_domain,
        )

        jsii.create(CreateBasicSite, self, [scope, id, props])


class CreateCloudfrontSite(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-simplewebsite-deploy.CreateCloudfrontSite",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        hosted_zone_domain: builtins.str,
        index_doc: builtins.str,
        website_domain: builtins.str,
        website_folder: builtins.str,
        encrypt_bucket: typing.Optional[builtins.bool] = None,
        error_doc: typing.Optional[builtins.str] = None,
        price_class: typing.Optional[aws_cdk.aws_cloudfront.PriceClass] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param hosted_zone_domain: hosted zone used to create the DNS record of your CloudFront distribution.
        :param index_doc: the index docuement of your CloudFront distribution.
        :param website_domain: the domain you want to deploy to.
        :param website_folder: local path to the website folder you want to deploy on S3.
        :param encrypt_bucket: enable encryption for files in your S3 Bucket.
        :param error_doc: the error document of your CloudFront distribution.
        :param price_class: the price class determines how many edge locations CloudFront will use for your distribution. default value is PriceClass_100. See https://aws.amazon.com/cloudfront/pricing/ for full list of supported regions.
        """
        props = CloudfrontSiteConfiguration(
            hosted_zone_domain=hosted_zone_domain,
            index_doc=index_doc,
            website_domain=website_domain,
            website_folder=website_folder,
            encrypt_bucket=encrypt_bucket,
            error_doc=error_doc,
            price_class=price_class,
        )

        jsii.create(CreateCloudfrontSite, self, [scope, id, props])


__all__ = [
    "BasicSiteConfiguration",
    "CloudfrontSiteConfiguration",
    "CreateBasicSite",
    "CreateCloudfrontSite",
]

publication.publish()
