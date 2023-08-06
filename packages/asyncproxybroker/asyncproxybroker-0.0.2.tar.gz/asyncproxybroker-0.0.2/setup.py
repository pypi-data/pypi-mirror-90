import io
import os

from setuptools import setup


def read(*parts):
    filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), *parts)

    with io.open(filename, encoding='utf-8', mode='r') as fp:
        return fp.read()


setup(
    name='asyncproxybroker',
    version='0.0.2',
    description='Library to asynchronously find and use public proxies from multiple sources.',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='Martin Zlocha',
    url='https://github.com/martinzlocha/asyncproxybroker',
    license='Apache License, Version 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'Topic :: Internet :: Proxy Servers',
        'Framework :: AsyncIO',
        'License :: OSI Approved :: Apache Software License',
    ],
    keywords=(
        'proxy finder grabber scraper parser checker broker async asynchronous http https connect asyncio aiohttp'
    ),
    platforms='any',
    python_requires='>=3.7',
    packages=['asyncproxybroker'],
    install_requires=['aiohttp>=3.7.3', 'proxybroker>=0.3.2', 'fake-useragent>=0.1.11'],
)