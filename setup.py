#!/usr/bin/env python

from setuptools import setup

setup(name='ranked-vote',
      version='0.0.1',
      description='Tools for working with ranked-vote data',
      author='Paul Butler',
      author_email='rcv@paulbutler.org',
      url='https://github.com/ranked-vote/ranked-vote-tools',
      packages=['ranked_vote', 'ranked_vote.format'],
      python_requires='>3.6'
      )
