"""Setup ethermine library."""

from setuptools import find_packages, setup
setup(
    name='ethermine',
    packages=find_packages(include=['ethermine']),
    version='0.1.2',
    description='Ethermine API python wrapper',
    author='Chris Landa',
    author_email='stylesuxx@gmail.com',
    url='https://github.com/stylesuxx/python-ethermine',
    license='MIT',
    keywords=['ethermine', 'etherium', 'eth'],
    install_requires=['requests'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)
