from setuptools import setup, find_packages
from helloworldpy.__main__ import __version__

from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'Environment :: Console',
    'Intended Audience :: Education',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: POSIX',
    'Programming Language :: Python',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    author='Saketh Chandra',
    author_email='b.sakethchandra9@gmail.com',
    name="helloworldpy",
    version=__version__,
    packages=["helloworldpy"],
    entry_points={
        "console_scripts": [
            "helloworldpy = helloworldpy.__main__:main"
        ]
    },
    classifiers=classifiers,
    license='MIT',
    description='This a basic project for learning how to make PIP(PyPI) package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Saketh-Chandra/helloworldpy',
    keywords=['Hello', 'World', 'Hello-World', 'Hello python'],

)
