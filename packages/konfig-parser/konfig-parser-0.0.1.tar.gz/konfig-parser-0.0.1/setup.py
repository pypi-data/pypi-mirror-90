from setuptools import setup, find_packages
import os

package_root = os.path.abspath(os.path.dirname(__file__))

version = {}
with open(os.path.join(package_root, "src/version.py")) as fp:
    exec(fp.read(), version)
version = version["__version__"]

with open('./requirements.txt') as r:
    # strip fixed version info from requirements file
    requirements = [line.split('~=', 1)[0] for line in r]

setup(
    install_requires=requirements,
    packages=find_packages(),
    version=version
)
