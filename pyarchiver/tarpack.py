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

	def extract(self, member, path = None):
		""" 
		Extract a member from the archive to the current working directory or specific path.

		    .. Never extract archives from untrusted sources without prior inspection.
		 	.. It is possible that files are created outside of path, 
		    .. e.g. members that have absolute filenames starting with "/" or filenames with two dots ".."

		:param member a member must be its full name or a TarInfo object
		:param path a different directory to extract to
		
        .. versionadded:: 1.0.0
        """
		return self._TAR.extract(member, path)

	def extractAll(self, path = None):
		"""
		Extract all members from the archive to the current working directory or specific path.

		:param path a different directory to extract to

		:return Instance of the object
		
        .. versionadded:: 1.0.0
        """
		return self._TAR.extractall(path)

	def close(self):
		""" 
		Closes the archive file or essential records will not be written.

		:return Instance of the object

		.. versionadded:: 1.0.0
		"""
		self._TAR.close()
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
        #: A list containing a TarInfo object for each member of the archive.
        #: The objects are in the same order as their entries in the actual TAR file on disk 
        #: if an existing archive was opened.
		self._TAR_INFO_LIST = self._TAR.getmembers()
		#: A list of archive members by name.
		self._TAR_NAME_LIST = self._TAR.getnames()

		return self

	def getInfo(self, name):
		"""
		Get a TarInfo object for member name

		:param name member name

		:return TarInfo object

		.. versionadded:: 1.0.0
		"""
		return self._TAR.getmember(name)

	def getInfoList(self):
		""" 
        Returns a list containing a TarInfo object for each member of the archive.
        The objects are in the same order as their entries in the actual TAR file on disk 
        if an existing archive was opened.

		:return list
		
        .. versionadded:: 1.0.0
        """
		return self._TAR_INFO_LIST

	def getNamesList(self):
		""" 
		Return a list of archive members by name.

		:return list
		
        .. versionadded:: 1.0.0
        """
		return self._TAR_NAME_LIST


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