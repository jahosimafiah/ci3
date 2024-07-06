from setuptools import setup, find_packages

setup(
    name='ci3',
    version='0.0.0',
    packages=find_packages(),
    install_requires=[
        'click',
        'boto3',
    ],
    entry_points={
        'console_scripts': [
            'ci3 = ci3.run:cli',
        ],
    }
)