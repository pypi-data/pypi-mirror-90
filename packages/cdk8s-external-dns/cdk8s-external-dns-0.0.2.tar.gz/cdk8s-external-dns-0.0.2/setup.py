import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk8s-external-dns",
    "version": "0.0.2",
    "description": "cdk8s-external-dns is an CDK8S construct library that provides External Dns Configure.",
    "license": "Apache-2.0",
    "url": "https://github.com/guan840912/cdk8s-external-dns.git",
    "long_description_content_type": "text/markdown",
    "author": "Neil Kuan<guan840912@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/guan840912/cdk8s-external-dns.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk8s_external_dns",
        "cdk8s_external_dns._jsii"
    ],
    "package_data": {
        "cdk8s_external_dns._jsii": [
            "cdk8s-external-dns@0.0.2.jsii.tgz"
        ],
        "cdk8s_external_dns": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-iam>=1.82.0, <2.0.0",
        "cdk8s-plus>=0.33.0, <0.34.0",
        "cdk8s>=0.33.0, <0.34.0",
        "constructs>=3.2.90, <4.0.0",
        "jsii>=1.16.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ]
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
