"""
PyArchiver Compression and Archiving Library

@author: Clivern U{hello@clivern.com}
"""

from __future__ import print_function
import os
import bz2
import gzip
import tarfile
import zipfile
import zlib


class PyArchiver(dict):
	""" A Class Which Compress and Decompress Files """
	
	

    def __init__(self, **kargs):
        """ Init PyArchiver Class """
        self._config(**kargs)

    def _config(self, **kargs):
        """ ReConfigure Package """
        for key, value in kargs.items():
            setattr(self, key, value)

    def getConfig(self, key):
        """ Get a Config Value """
        if hasattr(self, key):
            return getattr(self, key)
        else:
            return None

    def setConfig(self, key, value):
        """ Set a Config Value """
        setattr(self, key, value)

    def getConfigs(self, *kargs):
        """ Get Configs """
        for key in kargs:
			if hasattr(self, key):
            	yield getattr(self, key)
        	else:
            	return None

    def setConfigs(self, **kargs):
        """ ReConfigure Package """
        for key, value in kargs.items():
            setattr(self, key, value)

	def addFile(self, path):
		""" Add file to be compressed """
		pass

	def addFiles(self, *paths):
		""" Add files to be compressed """
		pass

	def addFolder(self, path):
		""" Add folder to be compressed """
		pass

	def addFolders(self, *paths):
		""" Add folders to be compressed """
		pass

	def addArchive(self, path):
		""" Add archive to be uncompressed """
		pass

	def addArchives(self, paths):
		""" Add archives to be uncompressed """
		pass

	def compress(self):
		""" Compress files """
		pass

	def decompress(self):
		""" Decompress archive """
		pass

	def getResults(self):
		""" Get compression or decompression process results """
		pass