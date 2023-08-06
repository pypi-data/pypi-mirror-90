#!/usr/bin/env python
# This will try to import setuptools. If not here, it fails with a message
import os
try:
    import setuptools
except ImportError:
    raise ImportError("This module could not be installed, probably because"
                      " setuptools is not installed on this computer."
                      "\nInstall ez_setup ([sudo] pip install ez_setup) and try again.")

package_name = "ntnx_api"
packages = setuptools.find_packages(
    include=[package_name, "{}.*".format(package_name)]
)

# Version info -- read without importing
_locals = {}
with open(os.path.join(package_name, "_version.py")) as fp:
    exec(fp.read(), None, _locals)
version = _locals["__version__"]

readme = open('README.rst', 'r')
README_TEXT = readme.read()
readme.close()

setup_deps = []

with open('docs/requirements.txt') as f:
    install_deps = f.read().splitlines()

with open('docs/test-requirements.txt') as f:
    testing_deps = f.read().splitlines()

pytest_deps = ["pytest"]

setuptools.setup(
    name=package_name,
    version=version,
    setup_requires=setup_deps,
    description="Nutanix API Library",
    keywords=["ntnx", "nutanix", "hci", "hyper-converged", "rest", "client", "prism", "prism-element", "prism-central"],
    url="https://gitlab.com/nutanix-se/python/nutanix-api",
    author="Ross Davies",
    author_email="davies.ross@gmail.com",
    license="BSD 2-Clause",
    packages=packages,
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        ],
    python_requires='>=3.6',
    install_requires=install_deps,
    long_description=README_TEXT,
    extras_require={
        "testing": testing_deps,
        "pytest": testing_deps + pytest_deps,
    },
)
