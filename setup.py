    '''
Created on 15 Mar 2017

@author: User
'''

from setuptools import setup
from setuptools.dist import check_entry_points

setup(name="combinedDataPull",
      version="0.1",
      description="Weather & Bike Data API interface",
      url="",
      author="David Fottrell",
      author_email="david.fottrell@ucdconnect.ie",
      licence="GPL3",
      packages=["weatherDataPull"],
      entry_points={
          'console_scripts':['workspaceComp30670_dataPull=combinedDataPull.main:main']
          }
    
    )
