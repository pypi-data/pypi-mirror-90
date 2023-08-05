from setuptools import setup, find_packages
import os


setup(
	name='django-kuldeep',
	version='1.5',
	description='database package',
	# long_description=long_description,
	long_description_content_type="text/markdown",
	url='https://github.com/softprodigyofficial/sample-python-package.git',
	author='kuldeep khatana',
	author_email='kuldeep.si.softprodigy@gmail.com',
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
		'Django',
	],
)