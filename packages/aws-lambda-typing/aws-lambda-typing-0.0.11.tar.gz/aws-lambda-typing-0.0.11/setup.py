import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aws-lambda-typing",
    version="0.0.11",
    description="A package that provides type hints for AWS Lambda event, context and response objects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MousaZeidBaker/aws-lambda-typing",
    author="Mousa Zeid Baker",
    author_email="mousa.zeid.baker@gmail.com",
    license="MIT",
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=[
        'typing',
        'type hints',
        'aws',
        'lambda',
        'serverless',
        'development'
    ],
    # packages=setuptools.find_packages(include=['aws_lambda_typing']),
    package_dir={'': 'aws_lambda_typing'},
    packages=setuptools.find_packages(where='aws_lambda_typing'),
    # packages=['aws_lambda_typing'],
    # py_modules=["index"],
    python_requires='>=3.8',
)
