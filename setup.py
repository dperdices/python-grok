import pathlib
from setuptools import setup

cwd = pathlib.Path(__file__).parent

with open(f"{cwd}/README.md", "r") as f:
    long_desc = f.read()

setup(
    name="python-grok",
    version="0.3.0",
    description="A Python package to use Grok expressions",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/dperdices/python-grok",
    author="Daniel Perdices",
    author_email="daniel.perdices@uam.es",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["grok"],
    include_package_data=True,
    package_data={
        "": ["patterns/*"]
    },
    install_requires=["regex", "importlib-resources"],
)