from setuptools import setup

with open('VERSION') as f:
    version = f.read().strip()

setup(
    name='scrabble',
    version=version,
    python_requires='>=3.10',
    description='Scrabble game logic library',
    url='',
    classifiers=['Programming Language :: Python :: 3'],
    author='Simon Staal',
    author_email='simonstaal10@gmail.com',
    packages=['scrabble/src'],
    zip_safe=True,
    test_suite='tests',
)
