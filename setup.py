from setuptools import setup

with open('VERSION') as f:
    version = f.read().strip()

setup(
    name='scrabble',
    version=version,
    description='Scrabble game logic library',
    url='',
    classifiers=['Programming Language :: Python :: 3'],
    author='Simon Staal',
    author_email='simonstaal10@gmail.com',
    packages=['scrabble'],
    zip_safe=True,
)
