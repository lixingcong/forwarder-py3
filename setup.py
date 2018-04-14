#!/usr/bin/env python

from setuptools import setup

packages = ['bottle',]

setup(name='forwarder', version='1.0',
		description='OpenShift Python3 application',
		author='lixingcong', author_email='lixngcong@live.com',
		url='https://www.python.org',
		install_requires=packages,
	)