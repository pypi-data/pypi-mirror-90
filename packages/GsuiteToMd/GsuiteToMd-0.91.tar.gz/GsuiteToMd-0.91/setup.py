from setuptools import setup
import setuptools
import sys


# Extra dependecies to run tests
tests_requirements = [
    "pytest>=4.6.0",
    "timeout-decorator",
    "funcy>=1.14",
    "flake8",
    "flake8-docstrings",
]

if sys.version_info >= (3, 6):
    tests_requirements.append("black==19.10b0")

setup(
    name="GsuiteToMd",
    version="0.91",
    author="Laurent Maumet",
    author_email="laurent@aurora-5r.fr",
    packages=setuptools.find_packages(),
    url="https://github.com/laurentmau/GsuiteToMd",
    description="Tools to convert gsuite Documents to markdown.",
    long_description=open("README.md").read(),
    install_requires=["google-api-python-client >= 1.12.5", "PyYAML >= 3.0"],
    extras_require={"tests": tests_requirements},
)
