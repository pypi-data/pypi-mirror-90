#!/usr/bin/env python

import typing


class KinesisFirehoseKinesisRecordMetadata(typing.TypedDict):
    """
    KinesisFirehoseKinesisRecordMetadata

    Attributes:
    ----------
    shardId: str

    partitionKey: str

    approximateArrivalTimestamp: str

    sequenceNumber: str

    subsequenceNumber: int
    """

    shardId: str
    partitionKey: str
    approximateArrivalTimestamp: str
    sequenceNumber: str
    subsequenceNumber: int


class KinesisFirehoseRecord(typing.TypedDict):
    """
    KinesisFirehoseRecord

    Attributes:
    ----------
    data: str

    recordId: str

    approximateArrivalTimestamp: int

    kinesisRecordMetadata: :class:`KinesisFirehoseKinesisRecordMetadata`
    """

    data: str
    recordId: str
    approximateArrivalTimestamp: int
    kinesisRecordMetadata: KinesisFirehoseKinesisRecordMetadata


class KinesisFirehoseEvent(typing.TypedDict):
    """
    KinesisFirehoseEvent https://docs.aws.amazon.com/lambda/latest/dg/with-kinesis.html

    Attributes:
    ----------
    invocationId: str

    deliveryStreamArn: str

    region: str

    records: typing.List[:class:`KinesisFirehoseRecord`]
    """

    invocationId: str
    deliveryStreamArn: str
    region: str
    records: typing.List[KinesisFirehoseRecord]
