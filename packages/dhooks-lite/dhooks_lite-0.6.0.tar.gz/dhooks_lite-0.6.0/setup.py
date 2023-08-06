import os
from setuptools import find_packages, setup
from dhooks_lite.constants import APP_NAME, APP_VERSION, HOMEPAGE_URL


# read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name=APP_NAME,
    version=APP_VERSION,
    packages=find_packages(),
    include_package_data=True,
    license="MIT",
    description=(
        "Another simple class wrapper for interacting with "
        "Discord webhooks in Python 3"
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["discord", "webhooks", "discordwebhooks", "discordhooks"],
    url=HOMEPAGE_URL,
    author="Erik Kalkoken",
    author_email="kalkoken87@gmail.com",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",  # example license
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Natural Language :: English",
        "Topic :: Communications :: Chat",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires="~=3.6",
    install_requires=["requests"],
)
