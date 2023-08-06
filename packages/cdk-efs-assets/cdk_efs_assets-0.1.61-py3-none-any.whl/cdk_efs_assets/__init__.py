"""
[![NPM version](https://badge.fury.io/js/cdk-efs-assets.svg)](https://badge.fury.io/js/cdk-efs-assets)
[![PyPI version](https://badge.fury.io/py/cdk-efs-assets.svg)](https://badge.fury.io/py/cdk-efs-assets)
![Release](https://github.com/pahud/cdk-efs-assets/workflows/Release/badge.svg)

# cdk-efs-assets

CDK construct library to populate Amazon EFS assets from Github or S3.

# `GithubSourceSync`

The `GithubSourceSync` deploys your Amazon EFS assets from specified Github repository.

## Sample

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_efs_assets import GithubSourceSync

app = App()

env = {
    "region": process.env.CDK_DEFAULT_REGION ?? AWS_DEFAULT_REGION,
    "account": process.env.CDK_DEFAULT_ACCOUNT
}

stack = Stack(app, "testing-stack", env=env)

vpc = ec2.Vpc.from_lookup(stack, "Vpc", is_default=True)

fs = efs.FileSystem(stack, "Filesystem",
    vpc=vpc,
    removal_policy=RemovalPolicy.DESTROY
)

efs_access_point = fs.add_access_point("EfsAccessPoint",
    path="/demo",
    create_acl={
        "owner_gid": "1001",
        "owner_uid": "1001",
        "permissions": "0755"
    },
    posix_user={
        "uid": "1001",
        "gid": "1001"
    }
)

# create the one-time sync from Github repository to Amaozn EFS
GithubSourceSync(stack, "GithubSourceSync",
    repository="https://github.com/pahud/cdk-efs-assets.git",
    efs_access_point=efs_access_point,
    runs_after=[fs.mount_targets_available],
    vpc=vpc
)
```

# `S3ArchiveSync`

The `S3ArchiveSync` deploys your Amazon EFS assets from a specified zip archive file stored in S3. The extracted contents will be placed into the root directory of the access point.

If the `syncOnUpdate` property is set to `true` (defaults to `true`), then the specified zip file path will be monitored, and if a new object is uploaded to the path, then it will resync the data to EFS. Note that to use this functionality, you must have a CloudTrail Trail in your account that captures the desired S3 write data event.

*WARNING*: The contents of the access point will be removed before extracting the zip file.

## Sample

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_efs_assets import S3ArchiveSync

app = App()

env = {
    "region": process.env.CDK_DEFAULT_REGION ?? AWS_DEFAULT_REGION,
    "account": process.env.CDK_DEFAULT_ACCOUNT
}

stack = Stack(app, "testing-stack", env=env)

vpc = ec2.Vpc.from_lookup(stack, "Vpc", is_default=True)

fs = efs.FileSystem(stack, "Filesystem",
    vpc=vpc,
    removal_policy=RemovalPolicy.DESTROY
)

efs_access_point = fs.add_access_point("EfsAccessPoint",
    path="/demo",
    create_acl={
        "owner_gid": "1001",
        "owner_uid": "1001",
        "permissions": "0755"
    },
    posix_user={
        "uid": "1001",
        "gid": "1001"
    }
)

bucket = Bucket.from_bucket_name(self, "Bucket", "demo-bucket")

# Will sync initial data from compressed S3 archive to EFS, and resync if the zip file in S3 changes
S3ArchiveSync(self, "S3ArchiveSync",
    bucket=bucket,
    zip_file_path="folder/foo.zip",
    vpc=vpc,
    efs_access_point=efs_access_point,
    runs_after=[fs.mount_targets_available]
)
```

# `S3SourceSync`

TBD
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

import aws_cdk.aws_ec2
import aws_cdk.aws_efs
import aws_cdk.aws_s3
import aws_cdk.core


@jsii.data_type(
    jsii_type="cdk-efs-assets.CommonEfsAssetsProps",
    jsii_struct_bases=[],
    name_mapping={
        "efs_access_point": "efsAccessPoint",
        "vpc": "vpc",
        "runs_after": "runsAfter",
        "vpc_subnets": "vpcSubnets",
    },
)
class CommonEfsAssetsProps:
    def __init__(
        self,
        *,
        efs_access_point: aws_cdk.aws_efs.IAccessPoint,
        vpc: aws_cdk.aws_ec2.IVpc,
        runs_after: typing.Optional[typing.List[aws_cdk.core.IDependable]] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> None:
        """
        :param efs_access_point: The target Amazon EFS filesystem to clone the github repository to.
        :param vpc: The VPC of the Amazon EFS Filesystem.
        :param runs_after: The dependent resources before triggering the sync.
        :param vpc_subnets: Where to place the network interfaces within the VPC.
        """
        if isinstance(vpc_subnets, dict):
            vpc_subnets = aws_cdk.aws_ec2.SubnetSelection(**vpc_subnets)
        self._values: typing.Dict[str, typing.Any] = {
            "efs_access_point": efs_access_point,
            "vpc": vpc,
        }
        if runs_after is not None:
            self._values["runs_after"] = runs_after
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def efs_access_point(self) -> aws_cdk.aws_efs.IAccessPoint:
        """The target Amazon EFS filesystem to clone the github repository to."""
        result = self._values.get("efs_access_point")
        assert result is not None, "Required property 'efs_access_point' is missing"
        return result

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """The VPC of the Amazon EFS Filesystem."""
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return result

    @builtins.property
    def runs_after(self) -> typing.Optional[typing.List[aws_cdk.core.IDependable]]:
        """The dependent resources before triggering the sync."""
        result = self._values.get("runs_after")
        return result

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """Where to place the network interfaces within the VPC."""
        result = self._values.get("vpc_subnets")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CommonEfsAssetsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-efs-assets.GithubSourceFeederProps",
    jsii_struct_bases=[CommonEfsAssetsProps],
    name_mapping={
        "efs_access_point": "efsAccessPoint",
        "vpc": "vpc",
        "runs_after": "runsAfter",
        "vpc_subnets": "vpcSubnets",
        "repository": "repository",
    },
)
class GithubSourceFeederProps(CommonEfsAssetsProps):
    def __init__(
        self,
        *,
        efs_access_point: aws_cdk.aws_efs.IAccessPoint,
        vpc: aws_cdk.aws_ec2.IVpc,
        runs_after: typing.Optional[typing.List[aws_cdk.core.IDependable]] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        repository: builtins.str,
    ) -> None:
        """
        :param efs_access_point: The target Amazon EFS filesystem to clone the github repository to.
        :param vpc: The VPC of the Amazon EFS Filesystem.
        :param runs_after: The dependent resources before triggering the sync.
        :param vpc_subnets: Where to place the network interfaces within the VPC.
        :param repository: The github repository HTTP URI.
        """
        if isinstance(vpc_subnets, dict):
            vpc_subnets = aws_cdk.aws_ec2.SubnetSelection(**vpc_subnets)
        self._values: typing.Dict[str, typing.Any] = {
            "efs_access_point": efs_access_point,
            "vpc": vpc,
            "repository": repository,
        }
        if runs_after is not None:
            self._values["runs_after"] = runs_after
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def efs_access_point(self) -> aws_cdk.aws_efs.IAccessPoint:
        """The target Amazon EFS filesystem to clone the github repository to."""
        result = self._values.get("efs_access_point")
        assert result is not None, "Required property 'efs_access_point' is missing"
        return result

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """The VPC of the Amazon EFS Filesystem."""
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return result

    @builtins.property
    def runs_after(self) -> typing.Optional[typing.List[aws_cdk.core.IDependable]]:
        """The dependent resources before triggering the sync."""
        result = self._values.get("runs_after")
        return result

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """Where to place the network interfaces within the VPC."""
        result = self._values.get("vpc_subnets")
        return result

    @builtins.property
    def repository(self) -> builtins.str:
        """The github repository HTTP URI."""
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GithubSourceFeederProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GithubSourceSync(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-efs-assets.GithubSourceSync",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        repository: builtins.str,
        efs_access_point: aws_cdk.aws_efs.IAccessPoint,
        vpc: aws_cdk.aws_ec2.IVpc,
        runs_after: typing.Optional[typing.List[aws_cdk.core.IDependable]] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param repository: The github repository HTTP URI.
        :param efs_access_point: The target Amazon EFS filesystem to clone the github repository to.
        :param vpc: The VPC of the Amazon EFS Filesystem.
        :param runs_after: The dependent resources before triggering the sync.
        :param vpc_subnets: Where to place the network interfaces within the VPC.
        """
        props = GithubSourceFeederProps(
            repository=repository,
            efs_access_point=efs_access_point,
            vpc=vpc,
            runs_after=runs_after,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(GithubSourceSync, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-efs-assets.S3ArchiveFeederProps",
    jsii_struct_bases=[CommonEfsAssetsProps],
    name_mapping={
        "efs_access_point": "efsAccessPoint",
        "vpc": "vpc",
        "runs_after": "runsAfter",
        "vpc_subnets": "vpcSubnets",
        "bucket": "bucket",
        "zip_file_path": "zipFilePath",
        "sync_on_update": "syncOnUpdate",
    },
)
class S3ArchiveFeederProps(CommonEfsAssetsProps):
    def __init__(
        self,
        *,
        efs_access_point: aws_cdk.aws_efs.IAccessPoint,
        vpc: aws_cdk.aws_ec2.IVpc,
        runs_after: typing.Optional[typing.List[aws_cdk.core.IDependable]] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        bucket: aws_cdk.aws_s3.IBucket,
        zip_file_path: builtins.str,
        sync_on_update: typing.Optional[builtins.bool] = None,
    ) -> None:
        """
        :param efs_access_point: The target Amazon EFS filesystem to clone the github repository to.
        :param vpc: The VPC of the Amazon EFS Filesystem.
        :param runs_after: The dependent resources before triggering the sync.
        :param vpc_subnets: Where to place the network interfaces within the VPC.
        :param bucket: The S3 bucket containing the archive file.
        :param zip_file_path: The path of the zip file to extract in the S3 bucket.
        :param sync_on_update: If this is set to true, then whenever a new object is uploaded to the specified path, an EFS sync will be triggered. Currently, this functionality depends on at least one CloudTrail Trail existing in your account that captures the S3 event. (optional, default: true)
        """
        if isinstance(vpc_subnets, dict):
            vpc_subnets = aws_cdk.aws_ec2.SubnetSelection(**vpc_subnets)
        self._values: typing.Dict[str, typing.Any] = {
            "efs_access_point": efs_access_point,
            "vpc": vpc,
            "bucket": bucket,
            "zip_file_path": zip_file_path,
        }
        if runs_after is not None:
            self._values["runs_after"] = runs_after
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets
        if sync_on_update is not None:
            self._values["sync_on_update"] = sync_on_update

    @builtins.property
    def efs_access_point(self) -> aws_cdk.aws_efs.IAccessPoint:
        """The target Amazon EFS filesystem to clone the github repository to."""
        result = self._values.get("efs_access_point")
        assert result is not None, "Required property 'efs_access_point' is missing"
        return result

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """The VPC of the Amazon EFS Filesystem."""
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return result

    @builtins.property
    def runs_after(self) -> typing.Optional[typing.List[aws_cdk.core.IDependable]]:
        """The dependent resources before triggering the sync."""
        result = self._values.get("runs_after")
        return result

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """Where to place the network interfaces within the VPC."""
        result = self._values.get("vpc_subnets")
        return result

    @builtins.property
    def bucket(self) -> aws_cdk.aws_s3.IBucket:
        """The S3 bucket containing the archive file."""
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return result

    @builtins.property
    def zip_file_path(self) -> builtins.str:
        """The path of the zip file to extract in the S3 bucket."""
        result = self._values.get("zip_file_path")
        assert result is not None, "Required property 'zip_file_path' is missing"
        return result

    @builtins.property
    def sync_on_update(self) -> typing.Optional[builtins.bool]:
        """If this is set to true, then whenever a new object is uploaded to the specified path, an EFS sync will be triggered.

        Currently, this functionality depends on at least one CloudTrail Trail existing in your account that captures the S3
        event.

        (optional, default: true)
        """
        result = self._values.get("sync_on_update")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3ArchiveFeederProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3ArchiveSync(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-efs-assets.S3ArchiveSync",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        bucket: aws_cdk.aws_s3.IBucket,
        zip_file_path: builtins.str,
        sync_on_update: typing.Optional[builtins.bool] = None,
        efs_access_point: aws_cdk.aws_efs.IAccessPoint,
        vpc: aws_cdk.aws_ec2.IVpc,
        runs_after: typing.Optional[typing.List[aws_cdk.core.IDependable]] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param bucket: The S3 bucket containing the archive file.
        :param zip_file_path: The path of the zip file to extract in the S3 bucket.
        :param sync_on_update: If this is set to true, then whenever a new object is uploaded to the specified path, an EFS sync will be triggered. Currently, this functionality depends on at least one CloudTrail Trail existing in your account that captures the S3 event. (optional, default: true)
        :param efs_access_point: The target Amazon EFS filesystem to clone the github repository to.
        :param vpc: The VPC of the Amazon EFS Filesystem.
        :param runs_after: The dependent resources before triggering the sync.
        :param vpc_subnets: Where to place the network interfaces within the VPC.
        """
        props = S3ArchiveFeederProps(
            bucket=bucket,
            zip_file_path=zip_file_path,
            sync_on_update=sync_on_update,
            efs_access_point=efs_access_point,
            vpc=vpc,
            runs_after=runs_after,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(S3ArchiveSync, self, [scope, id, props])


__all__ = [
    "CommonEfsAssetsProps",
    "GithubSourceFeederProps",
    "GithubSourceSync",
    "S3ArchiveFeederProps",
    "S3ArchiveSync",
]

publication.publish()
