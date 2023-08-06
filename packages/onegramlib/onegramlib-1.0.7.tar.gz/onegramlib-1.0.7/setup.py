#!/usr/bin/env python

from setuptools import setup

# Work around mbcs bug in distutils.
# http://bugs.python.org/issue10945
import codecs
try:
    codecs.lookup('mbcs')
except LookupError:
    ascii = codecs.lookup('ascii')
    codecs.register(lambda name, enc=ascii: {True: enc}.get(name == 'mbcs'))

VERSION = '1.0.7'

setup(
    name='onegramlib',
    version=VERSION,
    description='Python library for OneGram project graphene-based blockchains',
    long_description=open('README.md').read(),
	download_url='https://gitlab.com/onegram-developers/python-onegramlib/-/archive/v' + VERSION + '/python-onegramlib-v' + VERSION + '.zip',
    author='01People',
    author_email='info@01people.com',
    maintainer='01People',
    maintainer_email='info@01people.com',
    url='https://gitlab.com/onegram-developers/python-onegramlib',
    keywords=[
        'onegram',
        'api',
        'rpc',
        'ecdsa',
        'secp256k1'
    ],
    packages=["grapheneapi",
              "graphenebase",
              ],
    install_requires=["ecdsa",
                      "requests",
                      "websocket-client",
                      "pylibscrypt",
                      "pycryptodome",
                      ],
    classifiers=['License :: OSI Approved :: MIT License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 3',
                 'Development Status :: 3 - Alpha',
                 'Intended Audience :: Developers',
                 ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    include_package_data=True,
    zip_safe=True,
)
