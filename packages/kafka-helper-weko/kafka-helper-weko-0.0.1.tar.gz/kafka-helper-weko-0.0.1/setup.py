import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kafka-helper-weko",
    version="0.0.1",
    author="Yahor Krautsevich",
    author_email="y.krautsevich@gmail.com",
    description="Kafka handler",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=[
        'kafka_handler',
    ],
    install_requires=[
        'msgpack',
        'kafka-python',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
