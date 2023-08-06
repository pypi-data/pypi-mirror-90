#!/usr/bin/env python

import typing


class CloudWatchEventsMessageEvent(typing.TypedDict):
    """
    CloudWatchEventsMessageEvent https://docs.aws.amazon.com/lambda/latest/dg/services-cloudwatchevents.html

    Other CloudWatch Events Event Examples: https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/EventTypes.html

    Attributes:
    ----------
    account: str

    region: str

    detail: typing.Dict

    detail-type: str

    source: str

    time: str

    id: str

    resources: typing.List[str]
    """

    typing.TypedDict('CloudWatchEventsMessageEvent', {
        'account': str,
        'region': str,
        'detail': typing.Dict,
        'detail-type': str,
        'source': str,
        'time': str,
        'id': str,
        'resources': typing.List[str]
    })
