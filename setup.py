from setuptools import setup, find_packages

setup(
    name='PyCloudia Chat example',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pyzmq >= 14.0.1',
        'tornado >= 3.1.1',
        'zope.interface >= 4.0.5',
    ],
    author='CordiS',
    author_email='cordis@game-mafia.ru',
    description='PyCloudia Chat example demonstrates how to built distributed software',
    keywords='pycloudia chat example',
    url='https://github.com/cordis/pycloudia-chat',
)
