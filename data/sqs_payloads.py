# noqa: E501

"""Typical messages send via SQS."""

SQS_NO_MESSAGES_RESPONSE = {
    "ResponseMetadata": {
        "RequestId": "84f68448-82ed-521d-98a2-d3110aff12a1",
        "HTTPStatusCode": 200,
        "HTTPHeaders": {
            "x-amzn-requestid": "84f68448-82ed-521d-98a2-d3110aff12a1",
            "date": "Tue, 09 Jun 2020 12:51:50 GMT",
            "content-type": "text/xml",
            "content-length": "240",
        },
        "RetryAttempts": 0,
    },
}

SQS_MESSAGES_RESPONSE = {
    "Messages": [
        {
            "MessageId": "abe528f6-18a9-45a9-9871-8391ccb5c7d7",
            "ReceiptHandle": "123",
            "MD5OfBody": "905bbf7ea802c6043fbc0e81cafe7e5f",
            "Body": '{"Records": [{"s3": {"object": {"key": "7307752/4e696069-edf5-44dd-9f05-fcca2d14cdf1/20200609125740-113ebefe3cdd4a62b9d0e094213bf9e9","size": 11805,"eTag": "ef140efa70e9efe79fdd71e5909713bb","sequencer": "005EDF87444DDF7525"}}}]}',  # noqa: E501
            "Attributes": {
                "SenderId": "321123",
                "ApproximateFirstReceiveTimestamp": "1591707477622",
                "ApproximateReceiveCount": "1",
                "SentTimestamp": "1591707468964",
            },
        },
    ],
    "ResponseMetadata": {
        "RequestId": "aeb60670-75fd-5378-a1d3-5129fc68d330",
        "HTTPStatusCode": 200,
        "HTTPHeaders": {
            "x-amzn-requestid": "aeb60670-75fd-5378-a1d3-5129fc68d330",
            "date": "Tue, 09 Jun 2020 12:57:57 GMT",
            "content-type": "text/xml",
            "content-length": "22437",
        },
        "RetryAttempts": 0,
    },
}
