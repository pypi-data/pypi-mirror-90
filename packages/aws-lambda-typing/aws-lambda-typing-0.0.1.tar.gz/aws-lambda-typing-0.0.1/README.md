# AWS Lambda Typing

A package that provides type hints for AWS Lambda event, context and response
objects. It's a convenient way to get autocomplete and type hints built into
IDEs. Type annotations are not checked at runtime but are only enforced by
third party tools such as type checkers, IDEs, linters, etc.

## Usage
AWS SQS message event example

```python
import aws_lambda_typing as lambda_typing


def handler(event: lambda_typing.SQSEvent, context: lambda_typing.Context) -> None:

    for record in event['Records']:
        print(context.get_remaining_time_in_millis())

        print(record['body'])
```

## Demo
### IDE autocomplete
![ide_autocomplete](media/ide_autocomplete.gif)

### IDE code reference information
![code_reference_information](media/code_reference_information.gif)

## Hit counter
[![hit_count](http://hits.dwyl.com/MousaZeidBaker/aws-lambda-typing.svg)](http://hits.dwyl.com/MousaZeidBaker/aws-lambda-typing)

## License
### The MIT License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
