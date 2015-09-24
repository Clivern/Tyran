"""
PyArchiver Compression and Archiving Library

@author: Clivern U{hello@clivern.com}
"""

from __future__ import print_function
import os
import bz2
import gzip
import tarfile


class TarPack(object):
	""" Read and Write TAR files """

	def __init__(self, file, mode = 'r'):
		""" 
		Init class instance

		:param file : Path to a new or an existing tar archive
		:param mode : The mode parameter. defaults 'r' also it may be 'w' or 'a' and x (for more info. visit https://docs.python.org/3.5/library/tarfile.html#tarfile.open)

		:return Null

		.. versionadded:: 1.0.0
		"""
		self._TAR = tarfile.TarFile(file, mode)

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
		
	def add(self):
		""" 
		Add the file name to the archive. 

		 	.. name may be any type of file (directory, fifo, symbolic link, etc.). 
		 	.. If given, arcname specifies an alternative name for the file in the archive.

		:return Instance of the object

        .. versionadded:: 1.0.0
        """
		for name, arcname in self._Files:
			self._TAR.add(name, arcname)
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

	def extractAll(self, path = None, member = None, pwd = None):
		"""
		Extract all members from the archive to the current working directory or specific path.

		:param path a different directory to extract to
		:param member is optional and must be a subset of the list returned by namelist()
		:param pwd is the password used for encrypted files.

		:return Instance of the object
		
        .. versionadded:: 1.0.0
        """
		return self._ZIP.extract(member, path, pwd)

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


	def isTarFileName(self, filename):
		""" 
		Check if path is to a TAR archive

		:param file_path : Absolute path to a TAR archive

		:return boolean <whether path is to TAR archive but it may not exist>
		
        .. versionadded:: 1.0.0
        """
		return filename.endswith('.tar.gz')

	def isTarFile(self, file_path):
		""" 
		Check if path is to existing TAR archive

		:param file_path : Absolute path to TAR archive

		:return boolean <whether TAR archive exist or not>
		
        .. versionadded:: 1.0.0
        """
		return file_path.endswith('.tar.gz') and os.path.isfile(file_path)