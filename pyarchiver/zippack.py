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
	""" Read and Write .zip files """

	def __init__(self, file, mode = 'r', compression = zipfile.ZIP_STORED, allowZip64 = True):
		""" 
		Init class instance with archive name, mode ...etc

		:param file : Path to a new or an existing zip archive
		:param mode : r || w || a
		:param compression : zipfile.ZIP_STORED || zipfile.ZIP_DEFLATED || zipfile.ZIP_BZIP2 || zipfile.ZIP_LZMA
		:param allowZip64 : True || False

		:return Null

		.. versionadded:: 1.0.0
		"""
		self._ZIP = zipfile.ZipFile(file, mode, compression, allowZip64)

	def setFiles(self, files):
		""" 
		Set the files that we need to compress or decompress
		Files must be a the absoulte path
		
		:param files: A list of files

		:return Instance of the object

        .. versionadded:: 1.0.0
        """
		self._Files = files
		return self
		
	def write(self):
		""" 
		Write files to ZIP file

		:return Instance of the object

        .. versionadded:: 1.0.0
        """
		for filename, arcname, compress_type in self._Files:
			self._Files.write(filename, arcname, compress_type)
		return self

	def extract(self, member, path = None, pwd = None):
		""" 
		Extract file from archive to a specific path

		:param member
		:param path
		:param pwd

		:return Instance of the object
		
        .. versionadded:: 1.0.0
        """
		self._ZIP.extract(member, path, pwd)
		return self

	def extractAll(self, path = None, member = None, pwd = None):
		"""
		Extract all files or list of files from archive to a specific path

		:param path
		:param member
		:param pwd

		:return Instance of the object
		
        .. versionadded:: 1.0.0
        """
		self._ZIP.extract(member, path, pwd)
		return self

	def open(self, name, mode='r', pwd=None):
		""" 
		Open archive for reading or writing

		:param name
		:param mode
		:param pwd

		:return Instance of the object
		
        .. versionadded:: 1.0.0
        """
		return self._ZIP.open(name, mode, pwd)

	def close(self):
		""" 
		Closes the archive file or essential records will not be written.

		:return Instance of the object

		.. versionadded:: 1.0.0
		"""
		self._ZIP.close()
		return self

	def setInfo(self):
		""" 
		Open archive for reading or writing

		:param name
		:param mode
		:param pwd

		:return Instance of the object
		
        .. versionadded:: 1.0.0
        """
		self._ZIP_INFO_LIST = self._ZIP.infolist()
		self._ZIP_NAME_LIST = self._ZIP.namelist()
		self._ZIP_TEST = self._ZIP.testzip()
		return self

	def getInfoList(self):
		""" 
		Open archive for reading or writing

		:param name
		:param mode
		:param pwd

		:return Instance of the object
		
        .. versionadded:: 1.0.0
        """
		return self._ZIP_INFO_LIST

	def getNamesList(self):
		""" 
		Open archive for reading or writing

		:param name
		:param mode
		:param pwd

		:return Instance of the object
		
        .. versionadded:: 1.0.0
        """
		return self._ZIP_NAME_LIST

	def getZipTest(self):
		""" 
		Get ZIP test result

		:return None ||
		
        .. versionadded:: 1.0.0
        """
		return self._ZIP_TEST

	def isZipFileName(self, filename):
		""" 
		Check if path is to a ZIP archive

		:param file_path : Absolute path to a ZIP archive

		:return boolean <whether path is to ZIP archive but it may not exist>
		
        .. versionadded:: 1.0.0
        """
		return filename.endswith('.zip')

	def isZipFile(self, file_path):
		""" 
		Check if path is to existing ZIP archive

		:param file_path : Absolute path to ZIP archive

		:return boolean <whether ZIP archive exist or not>
		
        .. versionadded:: 1.0.0
        """
		return file_path.endswith('.zip') and os.path.isfile(file_path)