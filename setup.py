from setuptools import find_packages
from setuptools import setup


def _get_required_packages():
    with open('requirements.txt') as reqs_file:
        required = reqs_file.read().splitlines()
    return required


setup(
    name="stepik_p3",
    version="0.0.1",
    description="Stepik flask project 3",
    packages=find_packages(),
    install_requires=_get_required_packages(),
    include_package_data=True
)
