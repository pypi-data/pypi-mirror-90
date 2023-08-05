from setuptools import setup, find_packages
import os

long_description  = "python-database-package"
# BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# with open(BASE_DIR+"/README.md", "r") as fh:
#     long_description = fh.read()
classification = [
	'Development status :: 1 - Production/stable',
	'Intended Audience :: Education',
	'Operating System :: Linux :: ubuntu',
	'License :: OSI Approved :: MIT License',
	'Programming Language :: PYthon :: 3'
]

setup(
	name='kuldeep',
	version='0.0.10',
	description='database package',
	long_description=long_description,
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
	install_requires=['django'],
	py_modules=['kuldeep'],
)
