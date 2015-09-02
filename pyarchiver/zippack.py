"""
PyArchiver Compression and Archiving Library

@author: Clivern U{hello@clivern.com}
"""

from __future__ import print_function
import os
import zipfile
import bz2
import zlib

class ZipPack():
	""" 
	Read and Write .zip files

	for more info:
		- https://docs.python.org/3.4/library/zipfile.html
	"""

	def __init__(self, file, mode = 'r', compression = ZIP_STORED, allowZip64 = True):
		"""
		Init class instance

		* file : Path to a new or an existing zip archive
		* mode : r || w || a
		* compression : ZIP_STORED || ZIP_DEFLATED || ZIP_BZIP2 || ZIP_LZMA
		* allowZip64 : True || False
		"""
		self._ZIP = zipfile.ZipFile(file, mode, compression, allowZip64)

	def isZipFileName(self, filename):
		return filename.endswith('.zip')

	def isZipFile(self, file_path):
		return file_path.endswith('.zip') and os.path.isfile(file_path)
		
	def close(self):
		""" Closes the archive file or essential records will not be written. """
		self._ZIP.close()

	def getInfo(self, name):
		""" Return a ZipInfo object with information about the archive member name. """
		return self._ZIP.getinfo(name)

	def infoList(self):
		""" Return a list containing a ZipInfo object for each member of the archive. The objects are in the same order as their entries in the actual ZIP file on disk if an existing archive was opened."""
		return self._ZIP.infolist()

	def nameList(self):
		""" Return a list of archive members by name. """
		return self._ZIP.namelist()