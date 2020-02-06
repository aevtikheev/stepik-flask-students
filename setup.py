from setuptools import find_packages
from setuptools import setup

try:
    # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:
    # for pip <= 9.0.3
    from pip.req import parse_requirements


def load_requirements(fname):
    reqs = parse_requirements(fname, session="test")
    return [str(ir.req) for ir in reqs]


setup(
    name="stepik_p3",
    version="0.0.1",
    description="Stepik flask project 3",
    packages=find_packages(),
    install_requires=load_requirements('requirements.txt'),
    include_package_data=True
)
