import os

from pypandoc import convert_file
from setuptools import setup, find_packages


def convert_markdown_to_rst(file):
    return convert_file(file, "rst")


# we need this to make reading the version work in some CI envs (like GitHub actions)
def get_version_file_path():
    ci_path = "/home/runner/work/requests-extra/requests-extra"
    if os.path.isfile(ci_path + "/version"):
        return ci_path + "/version"
    else:
        return "version"


setup(
    name="requests_extra",
    version=open(get_version_file_path()).read(),
    description="Drop-in wrapper around the Python Requests library"
    " that provides extra features.",
    long_description=convert_markdown_to_rst("README.md"),
    url="https://github.com/requests-extra/requests-extra",
    author="requests-extra contributors and the upstream projects authors",
    keywords=["requests", "timeout", "retry", "exception", "brotli"],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
    ],
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1,<3",
        "urllib3>=1.26,<2",
        "brotli",
    ],
    # TODO: consider migrating to PEP 517. for now install the below dependency by yourself / in the CI.
    # setup_requires=[
    #     "pypandoc",
    # ],
)
