from setuptools import setup, find_packages
import os

long_description  = "python-database-package"

classification = [
	'Development status :: 1 - Production/stable',
	'Intended Audience :: Education',
	'Operating System :: Linux :: ubuntu',
	'License :: OSI Approved :: MIT License',
	'Programming Language :: PYthon :: 3'
]

setup(
	name='django_kuldeep',
	version='1.3',
	description='database package',
	long_description=long_description,
	long_description_content_type="text/markdown",
	url='https://github.com/softprodigyofficial/sample-python-package.git',
	author='django_kuldeep khatana',
	author_email='django_kuldeep.si.softprodigy@gmail.com',
	License='MIT',
	classifiers=[
		"Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
	],
	keywords='database-package',
	package=find_packages(),
	zip_safe=False,
	python_requires='>=3.5',
	install_requires=[
		'Django>=2.2',
	],
)
