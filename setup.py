from setuptools import setup, find_packages

setup(
    name='regulagity',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'gitpython',
        'click',
        'python-dateutil',
        'pandas'
    ],
  entry_points={
        "console_scripts": [
            "regulagity = regulagity:main",
        ],
    })