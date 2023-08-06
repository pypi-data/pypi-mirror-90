#!/usr/bin/env python

import enum
import typing


class SQSAttributes(typing.TypedDict):
    """
    SQSAttributes

    Attributes:
    ----------
    ApproximateReceiveCount: str

    SentTimestamp: str

    SenderId: str

    ApproximateFirstReceiveTimestamp: str

    SequenceNumber: typing.Optional[str]
        Only in FIFO queues

    MessageGroupId: typing.Optional[str]
        Only in FIFO queues

    MessageDeduplicationId: typing.Optional[str]
        Only in FIFO queues
    """
    ApproximateReceiveCount: str
    SentTimestamp: str
    SenderId: str
    ApproximateFirstReceiveTimestamp: str
    SequenceNumber: typing.Optional[str]
    MessageGroupId: typing.Optional[str]
    MessageDeduplicationId: typing.Optional[str]


class SQSDataTypeEnum(enum.Enum):
    """
    SQSDataTypeEnum

    Attributes:
    ----------
    STRING: 'String'

    NUMBER: 'Number'

    BINARY: 'Binary'
    """
    STRING = 'String'
    NUMBER = 'Number'
    BINARY = 'Binary'


class SQSMessageAttribute(typing.TypedDict):
    """
    SQSMessageAttribute https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_MessageAttributeValue.html

    Attributes:
    ----------
    BinaryValue: str

    DataType: :class:`SQSDataTypeEnum`

    StringValue: str
    """
    BinaryValue: str
    DataType: SQSDataTypeEnum
    StringValue: str


class SQSMessage(typing.TypedDict):
    """
    SQSMessage https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_Message.html

    Attributes:
    ----------
    messageId: str

    receiptHandle: str

    body: str

    attributes: :class:`SQSAttributes`

    messageAttributes: typing.Dict[str, :class:`SQSMessageAttribute`]

    md5OfBody: str

    eventSource: str

    eventSourceARN: str

    awsRegion: str
    """

    messageId: str
    receiptHandle: str
    body: str
    attributes: SQSAttributes
    messageAttributes: typing.Dict[str, SQSMessageAttribute]
    md5OfBody: str
    eventSource: str
    eventSourceARN: str
    awsRegion: str


class SQSEvent(typing.TypedDict):
    """
    SQSEvent https://docs.aws.amazon.com/lambda/latest/dg/with-sqs.html

    Attributes:
    ----------
    Records: typing.List[:class:`SQSMessage`]
    """

    Records: typing.List[SQSMessage]
