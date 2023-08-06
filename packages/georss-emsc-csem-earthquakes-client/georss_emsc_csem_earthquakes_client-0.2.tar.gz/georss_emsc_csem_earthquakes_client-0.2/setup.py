from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

REQUIRES = [
    'georss_client>=0.12',
]

setup(
    name="georss_emsc_csem_earthquakes_client",
    version="0.2",
    author="Matej Sekoranja",
    author_email="matej.sekoranja@gmail.com",
    description="A GeoRSS client library for the EMSC CSEM Earthquakes feed.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/msekoranja/python-georss-emsc-csem-earthquakes-client",
    packages=find_packages(exclude=("tests*",)),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=REQUIRES
)
