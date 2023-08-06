import os
import sys

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [("pytest-args=", "a", "Arguments to pass into py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)

    def run_tests(self):
        import pytest

        errno = pytest.main([])
        sys.exit(errno)


path, script = os.path.split(sys.argv[0])
os.chdir(os.path.abspath(path))

version = {}
with open(os.path.join("dibuk", "version.py")) as f:
    exec(f.read(), version)

setup(
    name="dibuk",
    version=version["VERSION"],
    description="Dibuk Python Bindings",
    long_description=open("./README.md", "r").read(),
    long_description_content_type="text/markdown",
    author="Palo Sopko",
    author_email="pavol@sopko.sk",
    license="MIT",
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=["requests >= 2.21.0", "user-agents >= 2.0.0"],
    tests_require=["pytest >= 6.2.1"],
    cmdclass={"test": PyTest},
    project_urls={
        "Bug Tracker": "https://github.com/palosopko/dibuk-python/issues",
        "Source Code": "https://github.com/palosopko/dibuk-python",
    },
    python_requires=">=3.6.*",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
