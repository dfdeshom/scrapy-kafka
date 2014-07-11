import os
from setuptools import setup

LONG_DESC = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

setup(name='scrapy-kafka',
        version='0.1.1',
        description='Kafka-based components for Scrapy',
        long_description=LONG_DESC,
        author='Didier Deshommes',
        author_email='dfdeshom@gmail.com',
        url='https://github.com/dfdeshom/scrapy-kafka',
        packages=['scrapy_kafka'],
        license='BSD',
        install_requires=['Scrapy>=0.24.2', 'samsa>=0.3.11', 'kazoo==2.0'],
        classifiers=[
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        ],)
        
