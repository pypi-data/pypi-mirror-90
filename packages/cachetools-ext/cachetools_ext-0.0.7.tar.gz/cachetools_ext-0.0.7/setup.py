from setuptools import find_packages, setup

TEST_REQUIRES = ["pytest", "pytest-cov", "moto"]
DEV_REQUIRES = TEST_REQUIRES + ["pre-commit", "pylint", "black"]

setup(
    name="cachetools_ext",
    version="0.0.7",
    author="Oliver Rice",
    url="https://github.com/olirice/cachetools_ext",
    packages=find_packages(exclude=("test")),
    install_requires=[],
    extras_require={"dev": DEV_REQUIRES, "test": TEST_REQUIRES, "s3": "boto3"},
)
