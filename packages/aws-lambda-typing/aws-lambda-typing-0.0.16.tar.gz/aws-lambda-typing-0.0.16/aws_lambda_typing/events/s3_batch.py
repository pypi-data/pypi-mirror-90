#!/usr/bin/env python

import enum
import typing


class S3BatchRequestJob(typing.TypedDict):
    """
    S3BatchRequestJob

    Attributes:
    ----------
    id: str
    """

    id: str


class S3BatchRequestTask(typing.TypedDict):
    """
    S3BatchRequestTask

    Attributes:
    ----------
    taskId: str

    s3Key: str

    s3VersionId: typing.Optional[str]

    s3BucketArn: str
    """

    taskId: str
    s3Key: str
    s3VersionId: typing.Optional[str]
    s3BucketArn: str


class S3BatchRequestEvent(typing.TypedDict):
    """
    S3BatchRequestEvent https://docs.aws.amazon.com/lambda/latest/dg/services-s3-batch.html

    Attributes:
    ----------
    invocationSchemaVersion: str

    invocationId: str

    job: :class:`S3BatchRequestJob`

    tasks: typing.List[:class:`S3BatchRequestTask`]
    """

    invocationSchemaVersion: str
    invocationId: str
    job: S3BatchRequestJob
    tasks: typing.List[S3BatchRequestTask]


class S3BatchResponseResultCodeEnum(enum.Enum):
    """
    S3BatchResponseResultCodeEnum https://docs.aws.amazon.com/AmazonS3/latest/dev/batch-ops-invoke-lambda.html

    Attributes:
    ----------
    SUCCEEDED: 'Succeeded'

    TEMPORARY_FAILURE: 'TemporaryFailure'

    PERMANENT_FAILURE: 'PermanentFailure'
    """
    SUCCEEDED = 'Succeeded'
    TEMPORARY_FAILURE = 'TemporaryFailure'
    PERMANENT_FAILURE = 'PermanentFailure'


class S3BatchResponseResult(typing.TypedDict):
    """
    S3BatchRequestTask

    Attributes:
    ----------
    taskId: str

    resultCode: str

    resultString: str
    """

    taskId: str
    resultCode: str
    resultString: str


class S3BatchResponse(typing.TypedDict):
    """
    S3BatchResponse https://docs.aws.amazon.com/lambda/latest/dg/services-s3-batch.html

    Attributes:
    ----------
    invocationSchemaVersion: str

    treatMissingKeysAs: :class:`S3BatchResponseResultCodeEnum`

    invocationId: str

    results: typing.List[:class:`S3BatchResponseResult`]
    """

    invocationSchemaVersion: str
    treatMissingKeysAs: S3BatchResponseResultCodeEnum
    invocationId: str
    results: typing.List[S3BatchResponseResult]
