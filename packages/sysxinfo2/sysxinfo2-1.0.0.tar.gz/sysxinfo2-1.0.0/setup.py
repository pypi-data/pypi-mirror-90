import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="sysxinfo2",
    version="1.0.0",
    description="Simple CLI tool for watching system Infos",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/srshazin/sysxinfo",
    author="Shazin",
    author_email="shazin.bd@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["sysxinfo"],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "sysxinfo=sysxinfo.__main__:main",
        ]
    },
)
