"""
PyArchiver Compression and Archiving Library

@author: Clivern U{hello@clivern.com}
"""
from __future__ import print_function
import os
import zipfile
import bz2
import zlib


class ZipPack(object):
	""" Read and Write ZIP Archives """

	def __init__(self, file, mode = 'r', type = 'zipfile', compression = zipfile.ZIP_STORED, allowZip64 = True):
		""" 
		Init class instance

		:param file : Path to a new or an existing zip archive
		:param mode : The mode parameter. defaults 'r' also it may be 'w' or 'a'
		:param type : The type may be zipfile or pyzipfile
		:param compression : The numeric constant. default zipfile.ZIP_STORED it may be zipfile.ZIP_DEFLATED, zipfile.ZIP_BZIP2, zipfile.ZIP_LZMA
		:param allowZip64 : is True (the default) zipfile will create ZIP files that use the ZIP64 extensions when the zipfile is larger than 2 GiB.
		                    If it is false zipfile will raise an exception when the ZIP file would require ZIP64 extensions.

		:return Null

		.. versionadded:: 1.0.0
		"""
		if type == 'pyzipfile':
			self._ZIP = zipfile.PyZipFile(file, mode, compression, allowZip64)
		else:
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
		Write the file named filename to the archive, giving it the archive name arcname.
		.. by default, this will be the same as filename, but without a drive letter and with leading path separators removed).
		.. If given, compress_type overrides the value given for the compression parameter to the constructor for the new entry. 
		.. The archive must be open with mode 'w', 'x' or 'a'
		.. Calling write() on a ZipFile created with mode 'r' will raise a RuntimeError. 
		.. Calling write() on a closed ZipFile will raise a RuntimeError

		:return Instance of the object

        .. versionadded:: 1.0.0
        """
		for filename, arcname, compress_type in self._Files:
			self._ZIP.write(filename, arcname, compress_type)
		return self

	def writePy(self, pathname):
		""" 
		Search for files *.py and add the corresponding file to the archive.
		The corresponding file is a *.pyo file if available, else a *.pyc file, compiling if necessary. 

		:param pathname is a file, the filename must end with .py or a package directory 

		:return Instance of the object

        .. versionadded:: 1.0.0
        """
		self._ZIP.writepy(pathname)
		return self

	def extract(self, member, path = None, pwd = None):
		""" 
		Extract a member from the archive to the current working directory or specific path.

		    .. Never extract archives from untrusted sources without prior inspection.
		 	.. It is possible that files are created outside of path, 
		    .. e.g. members that have absolute filenames starting with "/" or filenames with two dots ".."

		:param member a member must be its full name or a ZipInfo object
		:param path a different directory to extract to
		:param pwd is the password used for encrypted files.

		:return the normalized path created (a directory or new file).
		
        .. versionadded:: 1.0.0
        """
		return self._ZIP.extract(member, path, pwd)

	def extractAll(self, path = None, members = None, pwd = None):
		"""
		Extract all members from the archive to the current working directory or specific path.

		:param path a different directory to extract to
		:param member is optional and must be a subset of the list returned by namelist()
		:param pwd is the password used for encrypted files.

		:return Instance of the object
		
        .. versionadded:: 1.0.0
        """
		return self._ZIP.extractall(path, members, pwd)

	def open(self, name, mode='r', pwd=None):
		""" 
		Extract a member from the archive as a file-like object (ZipExtFile).
		
		:param name name is the name of the file in the archive, or a ZipInfo object.
		:param mode The mode parameter, if included, must be one of the following: 
					'r' (the default), 
					'U', or 'rU'. Choosing 'U' or 'rU' will enable universal newlines support in the read-only object.
		:param pwd is the password used for encrypted files.

		:return A file-like object (ZipExtFile)
		
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
		Store info data about archive

		:param name
		:param mode
		:param pwd

		:return Instance of the object
		
        .. versionadded:: 1.0.0
        """
        #: A list containing a ZipInfo object for each member of the archive.
        #: The objects are in the same order as their entries in the actual ZIP file on disk 
        #: if an existing archive was opened.
		self._ZIP_INFO_LIST = self._ZIP.infolist()
		#: A list of archive members by name.
		self._ZIP_NAME_LIST = self._ZIP.namelist()
		#: The name of the first bad file, or else return None. 
		#: Calling testzip() on a closed ZipFile will raise a RuntimeError.
		self._ZIP_TEST = self._ZIP.testzip()
		return self

	def getInfoList(self):
		""" 
        Returns a list containing a ZipInfo object for each member of the archive.
        The objects are in the same order as their entries in the actual ZIP file on disk 
        if an existing archive was opened.

		:return list
		
        .. versionadded:: 1.0.0
        """
		return self._ZIP_INFO_LIST

	def getNamesList(self):
		""" 
		Return a list of archive members by name.

		:return list
		
        .. versionadded:: 1.0.0
        """
		return self._ZIP_NAME_LIST

	def getZipTest(self):
		""" 
		Returns the name of the first bad file, or else return None. 

		:return string || None
		
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