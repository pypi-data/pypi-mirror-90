#!/usr/bin/env python

import enum
import typing


class AttributeValue(typing.TypedDict, total=False):
    """
    AttributeValue https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_streams_AttributeValue.html

    Attributes:
    ----------
    B: str

    BS: typing.List[str]

    BOOL: bool

    L: typing.List

    M: typing.Dict

    N: str

    NS: typing.List[str]

    NULL: bool

    S: str

    SS: typing.List[str]
    """

    B: str
    BS: typing.List[str]
    BOOL: bool
    L: typing.List
    M: typing.Dict
    N: str
    NS: typing.List[str]
    NULL: bool
    S: str
    SS: typing.List[str]


class StreamViewTypeEnum(enum.Enum):
    """
    StreamViewTypeEnum

    Attributes:
    ----------
    KEYS_ONLY = 'KEYS_ONLY'

    NEW_IMAGE = 'NEW_IMAGE'

    OLD_IMAGE = 'OLD_IMAGE'

    NEW_AND_OLD_IMAGES = 'NEW_AND_OLD_IMAGES'
    """
    KEYS_ONLY = 'KEYS_ONLY'
    NEW_IMAGE = 'NEW_IMAGE'
    OLD_IMAGE = 'OLD_IMAGE'
    NEW_AND_OLD_IMAGES = 'NEW_AND_OLD_IMAGES'


class StreamRecord(typing.TypedDict):
    """
    StreamRecord https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_streams_StreamRecord.html

    Attributes:
    ----------
    ApproximateCreationDateTime: int

    Keys: typing.Dict[str, :class:`AttributeValue`]

    NewImage: typing.Dict[str, :class:`AttributeValue`]

    OldImage: typing.Dict[str, :class:`AttributeValue`]

    SequenceNumber: str

    SizeBytes: int

    StreamViewType: :class:`StreamViewTypeEnum`
    """

    ApproximateCreationDateTime: int
    Keys: typing.Dict[str, AttributeValue]
    NewImage: typing.Dict[str, AttributeValue]
    OldImage: typing.Dict[str, AttributeValue]
    SequenceNumber: str
    SizeBytes: int
    StreamViewType: StreamViewTypeEnum


class EventNameEnum(enum.Enum):
    """
    EventNameEnum

    Attributes:
    ----------
    INSERT = 'INSERT'

    MODIFY = 'MODIFY'

    REMOVE = 'REMOVE'
    """
    INSERT = 'INSERT'
    NEW_IMAGE = 'NEW_IMAGE'
    REMOVE = 'REMOVE'


class DynamodbRecord(typing.TypedDict):
    """
    DynamodbRecord https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_streams_Record.html

    Attributes:
    ----------
    awsRegion: str

    dynamodb: :class:`StreamRecord`

    eventID: str

    eventName: :class:`EventNameEnum`

    eventSource: str

    eventSourceARN: str

    eventVersion: str

    userIdentity: typing.Any
    """

    awsRegion: str
    dynamodb: StreamRecord
    eventID: str
    eventName: EventNameEnum
    eventSource: str
    eventSourceARN: str
    eventVersion: str
    userIdentity: typing.Any


class DynamoDBStreamEvent(typing.TypedDict):
    """
    DynamoDBStreamEvent https://docs.aws.amazon.com/lambda/latest/dg/with-ddb.html

    Attributes:
    ----------
    Records: typing.List[:class:`DynamodbRecord`]
    """

    Records: typing.List[DynamodbRecord]
