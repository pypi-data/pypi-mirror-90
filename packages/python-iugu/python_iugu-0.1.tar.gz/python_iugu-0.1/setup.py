from setuptools import setup, find_packages

import os
import sys

from python_iugu.version import __version__

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'python_iugu'))

requirements = [
    "aiodns==2.0.0",
    "aiohttp==3.7.3",
    "async-timeout==3.0.1",
    "attrs==20.3.0",
    "brotlipy==0.7.0",
    "cchardet==2.1.7",
    "certifi==2020.12.5",
    "cffi==1.14.4",
    "chardet==3.0.4",
    "deserialize==1.8.0",
    "idna==2.10",
    "multidict==5.1.0",
    "pycares==3.1.1",
    "pycparser==2.20",
    "typing-extensions==3.7.4.3",
    "urllib3==1.26.2",
    "yarl==1.6.3",
]

setup(
    name='python_iugu',
    packages=find_packages(),
    version=__version__,
    license='MIT',
    description='This provides Python REST APIs to create, process and manage payments on IUGU.',
    author='Guilherme Silva',
    author_email='guilherme.1995lemes@gmail.com',
    keywords=['iugu', 'rest', 'payment'],
    install_requires=requirements,
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],

)
