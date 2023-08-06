import codecs
import os.path

from setuptools import setup, find_packages

this_file_path = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    return codecs.open(os.path.join(this_file_path, *parts), 'r').read()


install_requires = [
    'click',
    'pyfiglet',
    'colorama',
    'configparser',
    'tqdm',
    'tabulate',
    'requests',
    'beautifultable'
]

setup_options = dict(
    name='chargebee-cli',
    description='cli for chargebee apis',
    long_description=read('README.md'),
    version='0.0.14',
    entry_points={
        'console_scripts': [
            'cb = chargebeecli.__main__:main'
        ]
    },
    install_requires=install_requires,
    packages=find_packages(),
    nclude_package_data=True,
    zip_safe=False
)
setup(**setup_options)
