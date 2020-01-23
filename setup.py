from setuptools import setup, find_packages

with open('./README.md') as readme:
    long_desc = readme.read()

setup(
    name='regulagity',
    author='Michael Milton',
    author_email='michael.r.milton@gmail.com',
    description='A tool for measuring the activity of a git repo using a variety of single summary statistics',
    long_description_content_type='text/markdown',
    long_description=long_desc,
    keywords='git activity summary',
    url='https://github.com/TMiguelT/Regulagity',
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Version Control',
        'Topic :: Software Development :: Version Control :: Git'
    ],
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'gitpython',
        'click',
        'pandas'
    ],
    entry_points={
        "console_scripts": [
            "regulagity = regulagity:main",
        ],
    })
