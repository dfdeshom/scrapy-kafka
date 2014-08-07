import os
from pkg_resources import parse_requirements
from setuptools import setup

MY_DIR = os.path.dirname(__file__)
LONG_DESC = open(os.path.join(MY_DIR, 'README.md')).read()
req_fh = open(os.path.join(MY_DIR, 'requirements.txt'))
install_requirements = [str(r) for r in parse_requirements(req_fh)]
req_fh.close()

setup(name='scrapy-kafka',
      version='0.1.1',
      description='Kafka-based components for Scrapy',
      long_description=LONG_DESC,
      author='Didier Deshommes',
      author_email='dfdeshom@gmail.com',
      url='https://github.com/dfdeshom/scrapy-kafka',
      packages=['scrapy_kafka'],
      license='BSD',
      install_requires=install_requirements,
      classifiers=[
          'Programming Language :: Python',
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
      ])
