import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "awscdk-81-patch",
    "version": "1.1.0",
    "description": "awscdk-81-patch",
    "license": "Apache-2.0",
    "url": "https://github.com/eladb/awscdk-81-patch.git",
    "long_description_content_type": "text/markdown",
    "author": "Elad Ben-Israel<benisrae@amazon.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/eladb/awscdk-81-patch.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "awscdk_81_patch",
        "awscdk_81_patch._jsii"
    ],
    "package_data": {
        "awscdk_81_patch._jsii": [
            "awscdk-81-patch@1.1.0.jsii.tgz"
        ],
        "awscdk_81_patch": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
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
