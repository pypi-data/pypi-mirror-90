import os
import codecs
from setuptools import setup, find_packages


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-report-me',
    author='Yuz Wang',
    version="0.0.1",
    author_email='looker53@sina.com',
    maintainer='Yuz Wang',
    maintainer_email='looker53@sina.com',
    license='MIT',
    url='https://github.com/looker53/pytest-report-me',
    description='Generate Pytest reports with templates',
    long_description=read('README.md'),
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'pytest',
        'jinja2'
    ],
    classifiers=[
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'report = pytest_report_me.plugin',
        ],
    },
)