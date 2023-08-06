from setuptools import setup

with open("VERSION") as version_file:
    version = version_file.read().strip()

# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setup(name="gevent-queue", version=version, install_requires=["redis>=3.0.0"])
