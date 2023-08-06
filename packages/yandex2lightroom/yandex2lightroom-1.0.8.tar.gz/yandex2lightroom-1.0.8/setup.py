from setuptools import setup, find_packages
from codecs import open
from os import path

__version__ = 'v1.0.8'

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

# get the dependencies and installs
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs]

setup(
    name='yandex2lightroom',
    packages=['yandex2lightroom'],
    version=__version__,
    license='MIT',
    description="Python Script to download images from Yandex.Images for the use in Adobe Lightroom.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Dieter Stockhausen',
    author_email='dieter@schwingenhausen.at',
    url='https://github.com/sto3014/yandex2lightroom-git',
    download_url=f'https://github.com/sto3014/yandex2lightroom-git/archive/main.zip',
    keywords='yandex images download save terminal command-line scrapper lightroom',
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ],
    entry_points={
        "console_scripts": [
            'yandex2lightroom = yandex2lightroom:run_main'
        ]
    }
)
