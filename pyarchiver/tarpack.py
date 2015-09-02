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

class TarPack():
	""" Read and Write .tar.gz files """
	
	def isTarFileName(self, filename):
		return filename.endswith('.tar.gz')

	def isTarFile(self, file_path):
		return file_path.endswith('.tar.gz') and os.path.isfile(file_path)