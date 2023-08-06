#!/usr/bin/env python

import typing


class S3UserIdentity(typing.TypedDict):
    """
    S3UserIdentity

    Attributes:
    ----------
    principalId: str
    """

    principalId: str


class S3RequestParameters(typing.TypedDict):
    """
    S3RequestParameters

    Attributes:
    ----------
    sourceIPAddress: str
    """

    sourceIPAddress: str


class S3ResponseElements(typing.TypedDict):
    """
    S3ResponseElements

    Attributes:
    ----------
    SignatureVersion: str
    """

    SignatureVersion: str


class S3OwnerIdentity(typing.TypedDict):
    """
    S3OwnerIdentity

    Attributes:
    ----------
    principalId: str
    """

    principalId: str


class S3Bucket(typing.TypedDict):
    """
    S3Bucket

    Attributes:
    ----------
    name: str

    ownerIdentity: :class:`S3OwnerIdentity`

    arn: str
    """

    name: str
    ownerIdentity: S3OwnerIdentity
    arn: str


class S3Object(typing.TypedDict):
    """
    S3OwnerIdentity

    Attributes:
    ----------
    key: str

    size: int

    eTag: str

    versionId: typing.Optional[str]

    sequencer: str
    """

    key: str
    size: int
    eTag: str
    versionId: typing.Optional[str]
    sequencer: str


class S3(typing.TypedDict):
    """
    S3

    Attributes:
    ----------
    s3SchemaVersion: str

    configurationId: str

    bucket: :class:`S3Bucket`

    object: :class:`S3Object`
    """

    s3SchemaVersion: str
    configurationId: str
    bucket: S3Bucket
    object: S3Object


class S3GlacierEventDataRestoreEventData(typing.TypedDict):
    """
    S3GlacierEventData

    Attributes:
    ----------
    lifecycleRestorationExpiryTime: str

    lifecycleRestoreStorageClass: str
    """

    lifecycleRestorationExpiryTime: str
    lifecycleRestoreStorageClass: str


class S3GlacierEventData(typing.TypedDict):
    """
    S3GlacierEventData

    Attributes:
    ----------
    restoreEventData: :class:`S3GlacierEventDataRestoreEventData`
    """

    restoreEventData: S3GlacierEventDataRestoreEventData


class S3EventRecord(typing.TypedDict):
    """
    S3EventRecord https://docs.aws.amazon.com/AmazonS3/latest/dev/notification-content-structure.html

    Attributes:
    ----------
    eventVersion: str

    eventSource: str

    awsRegion: str

    eventTime: str

    eventName: str

    userIdentity: :class:`S3UserIdentity`

    requestParameters: :class:`S3RequestParameters`

    responseElements: :class:`S3ResponseElements`

    s3: :class:`S3`

    glacierEventData: typing.Optional[:class:`S3GlacierEventData`]
    """

    eventVersion: str
    eventSource: str
    awsRegion: str
    eventTime: str
    eventName: str
    userIdentity: S3UserIdentity
    requestParameters: S3RequestParameters
    responseElements: S3ResponseElements
    s3: S3
    glacierEventData: typing.Optional[S3GlacierEventData]


class S3Event(typing.TypedDict):
    """
    S3Event https://docs.aws.amazon.com/lambda/latest/dg/with-s3.html

    Attributes:
    ----------
    Records: typing.List[:class:`S3EventRecord`]
    """

    Records: typing.List[S3EventRecord]
