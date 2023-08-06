from setuptools import setup, find_packages
from os.path import join, dirname
import yandexdirectpy

setup(
    name='yandexdirectpy',
    version=yandexdirectpy.__version__,
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
    author='Kriptos',
    author_email='kriptos1834@gmail.com',
    url='https://github.com/Kriptos1834/py-yandexdirect/',
    install_requires=[
        'pandas',
        'colorama',
        'requests',
        'xmltodict',
    ]
)
