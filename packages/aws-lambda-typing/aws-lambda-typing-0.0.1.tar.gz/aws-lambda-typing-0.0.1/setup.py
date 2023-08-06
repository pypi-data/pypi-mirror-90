import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aws-lambda-typing",
    version="0.0.1",
    author="Mousa Zeid Baker",
    author_email="mousa.zeid.baker@gmail.com",
    description="A package that provides type hints for AWS Lambda event, context and response objects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MousaZeidBaker/aws-lambda-typing",
    keywords=[
        'typing',
        'type hints',
        'development',
        'lambda'
    ],
    packages=setuptools.find_packages(include=["aws_lambda_typing"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
