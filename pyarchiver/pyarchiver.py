from __future__ import print_function

import os
import bz2
import gzip
import tarfile
import zipfile
import zlib


class PyArchiver(dict):
	""" A class which compress and decompress files """
	
	def __init__(self, name=''):
		pass
		
	def __getattr__(self, name, default = False):
		""" Get attributes """
		if name in self.__dict__:
			return self.__dict__[name]
		elif name in self:
			return self.get(name)
		else:
			# Check for denormalized name
			name = self._denormalize(name)
			if name in self:
				return self.get(name)
			else:
				return default

	def __setattr__(self, name, value):
		""" Set attributes """
		if name in self.__dict__:
			self.__dict__[name] = value
		elif name in self:
			self[name] = value
		else:
			# Check for denormalized name
			name2 = self._denormalize(name)
			if name2 in self:
				self[name2] = value
			else:
				# New attribute
				self[name] = value

	def _normalize(self, value):
		""" Normalize a string """

		if value.find('-') != -1:
			value = value.replace('-', '_')

		return value

	def _denormalize(self, value):
		""" De-normalize a string """

		if value.find('_') != -1:
			value = value.replace('_', '-')

		return value

	def setConfig(self, name, value):
		""" Set a config whether during compression or decompression process """
		pass

	def getConfig(self, name, default = False):
		""" Get a config whether during compression or decompression process """
		pass

	def addFile(self, path):
		""" Add file to be compressed """
		pass

	def addFiles(self, paths):
		""" Add files to be compressed """
		pass

	def addFolder(self, path):
		""" Add folder to be compressed """
		pass

	def addFolders(self, paths):
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

	def getConfigs(self, default = {}):
		""" Get compression or decompression configs """
		pass

	def getResults(self, default = {}):
		""" Get compression or decompression process results """
		pass