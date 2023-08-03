from setuptools import setup, find_packages

setup(
    name='lmppl_code',
    version='0.3',
    packages=find_packages(),
    install_requires=[
        'transformers',  # specify the transformers library as a dependency
    ],
)
