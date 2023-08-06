from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='froxpy',
    version='1.0.1',
    author='Lizard Studios',
    author_email='support@lizard-studios.at',
    url='https://github.com/lizardstudios-at/froxpy',
    description='A library to manage and test proxy lists in python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=["froxpy"],
    package_dir={'': 'src'},
    classifier=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'License :: Apache License :: 2.0',
        'Operating System :: OS Independent'
    ],
    install_requires=[
        'requests',
        'colorama'
    ]
)
