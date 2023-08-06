#!/usr/bin/env python

import enum
import typing


class SESMailHeader(typing.TypedDict):
    """
    SESReceiptStatus

    Attributes:
    ----------
    name: str

    value: str
    """

    name: str
    value: str


class SESMailCommonHeaders:
    """
    SESReceiptStatus

    Attributes:
    ----------
    returnPath: str

    from: typing.Optional[typing.List[str]]

    date: str

    to: typing.Optional[typing.List[str]]

    cc: typing.Optional[typing.List[str]]

    bcc: typing.Optional[typing.List[str]]

    sender: typing.Optional[typing.List[str]]

    replyTo: typing.Optional[typing.List[str]]

    messageId: str

    subject: typing.List[str]
    """

    typing.TypedDict('SESMailCommonHeaders', {
        'returnPath': str,
        'from': typing.Optional[typing.List[str]],
        'date': str,
        'to': typing.Optional[typing.List[str]],
        'cc': typing.Optional[typing.List[str]],
        'bcc': typing.Optional[typing.List[str]],
        'sender': typing.Optional[typing.List[str]],
        'replyTo': typing.Optional[typing.List[str]],
        'messageId': str,
        'subject': typing.List[str]
    })


class SESMail(typing.TypedDict):
    """
    SESReceiptStatus

    Attributes:
    ----------
    timestamp: str

    source: str

    messageId: str

    destination: typing.List[str]

    headersTruncated: bool

    headers: typing.List[:class:`SESMailHeader`]

    commonHeaders: :class:`SESMailCommonHeaders`
    """
    timestamp: str
    source: str
    messageId: str
    destination: typing.List[str]
    headersTruncated: bool
    headers: typing.List[SESMailHeader]
    commonHeaders: SESMailCommonHeaders


class SESReceiptStatusEnum(enum.Enum):
    """
    SESReceiptStatusEnum

    Attributes:
    ----------
    PASS: 'PASS'

    FAIL: 'FAIL'

    GRAY: 'GRAY'

    PROCESSING_FAILED: 'PROCESSING_FAILED'
    """
    PASS = 'PASS'
    FAIL = 'FAIL'
    GRAY = 'GRAY'
    PROCESSING_FAILED = 'PROCESSING_FAILED'


class SESReceiptStatus(typing.TypedDict):
    """
    SESReceiptStatus

    Attributes:
    ----------
    status: :class:`SESReceiptStatusEnum`
    """

    status: SESReceiptStatusEnum


class SESReceiptS3Action(typing.TypedDict):
    """
    SESReceiptS3Action

    Attributes:
    ----------
    type: str
        S3 action will use the "S3" type.

    topicArn: typing.Optional[str]

    bucketName: str

    objectKey: str
    """

    type: str
    topicArn: typing.Optional[str]
    bucketName: str
    objectKey: str


class SESReceiptSnsAction(typing.TypedDict):
    """
    SESReceiptSnsAction

    Attributes:
    ----------
    type: str
        SNS action will use the "SNS" type.

    topicArn: str
    """

    type: str
    topicArn: str


class SESReceiptBounceAction(typing.TypedDict):
    """
    SESReceiptBounceAction

    Attributes:
    ----------
    type: str
        Bounce action will use the "Bounce" type.

    topicArn: typing.Optional[str]

    smtpReplyCode: str

    statusCode: str

    message: str

    sender: str
    """

    type: str
    topicArn: typing.Optional[str]
    smtpReplyCode: str
    statusCode: str
    message: str
    sender: str


class SESReceiptLambdaAction(typing.TypedDict):
    """
    SESReceiptLambdaAction

    Attributes:
    ----------
    type: str
        Lambda action will use the "Lambda" type.

    topicArn: typing.Optional[str]

    functionArn: str

    invocationType: str
    """

    type: str
    topicArn: typing.Optional[str]
    functionArn: str
    invocationType: str


class SESReceiptStopAction(typing.TypedDict):
    """
    SESReceiptStopAction

    Attributes:
    ----------
    type: str
        Stop action will use the "Stop" type.


    topicArn: typing.Optional[str]
    """

    type: str
    topicArn: typing.Optional[str]


class SESReceiptWorkMailAction(typing.TypedDict):
    """
    SESReceiptWorkMailAction

    Attributes:
    ----------
    type: str
        Work mail action will use the "WorkMail" type.

    topicArn: typing.Optional[str]

    organizationArn: str
    """

    type: str
    topicArn: typing.Optional[str]
    organizationArn: str


class SESDmarcPolicyEnum(enum.Enum):
    """
    SESDmarcPolicyEnum

    Attributes:
    ----------
    NONE: 'none'

    QUARANTINE: 'quarantine'

    REJECT: 'reject'
    """
    NONE = 'none'
    QUARANTINE = 'quarantine'
    REJECT = 'reject'


class SESMessage(typing.TypedDict):
    """
    SESMessage https://docs.aws.amazon.com/ses/latest/DeveloperGuide/receiving-email-notifications-contents.html

    Attributes:
    ----------
    recipients: typing.List[str]

    timestamp: str

    spamVerdict: :class:`SESReceiptStatus`

    dkimVerdict: :class:`SESReceiptStatus`

    processingTimeMillis: int

    action: typing.Union[:class:`SESReceiptS3Action`, :class:`SESReceiptSnsAction`, :class:`SESReceiptBounceAction`,
                         :class:`SESReceiptLambdaAction`, :class:`SESReceiptStopAction`,
                         :class:`SESReceiptWorkMailAction`]

    spfVerdict: :class:`SESReceiptStatus`

    virusVerdict: :class:`SESReceiptStatus`

    dmarcVerdict: :class:`SESReceiptStatus`

    dmarcPolicy: :class:`SESDmarcPolicyEnum`
    """

    recipients: typing.List[str]
    timestamp: str
    spamVerdict: SESReceiptStatus
    dkimVerdict: SESReceiptStatus
    processingTimeMillis: int
    action: typing.Union[SESReceiptS3Action, SESReceiptSnsAction, SESReceiptBounceAction, SESReceiptLambdaAction,
                         SESReceiptStopAction, SESReceiptWorkMailAction]
    spfVerdict: SESReceiptStatus
    virusVerdict: SESReceiptStatus
    dmarcVerdict: SESReceiptStatus
    dmarcPolicy: SESDmarcPolicyEnum


class SESEventRecord(typing.TypedDict):
    """
    SESEventRecord

    Attributes:
    ----------
    EventVersion: str

    ses: :class:`SESMessage`

    EventSource: str
    """

    EventVersion: str
    ses: SESMessage
    EventSource: str


class SESEvent(typing.TypedDict):
    """
    SESEvent https://docs.aws.amazon.com/lambda/latest/dg/services-ses.html

    Attributes:
    ----------
    Records: typing.List[:class:`SESEventRecord`]
    """

    Records: typing.List[SESEventRecord]
