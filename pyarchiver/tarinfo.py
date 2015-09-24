"""
PyArchiver Compression and Archiving Library

@author: Clivern U{hello@clivern.com}
"""

class TarInfo(object):
	""" A getter class for TarInfo object """

	def __init__(self, file_info):
		self._FILE_INFO = file_info

	def getFileName(self):
		""" Name of the file in the archive. """
		return self._FILE_INFO.filename

	def getModifDate(self):
		""" The time and date of the last modification to the archive member. """
		return self._FILE_INFO.date_time

	def getCompressType(self):
		""" Type of compression for the archive member. """
		return self._FILE_INFO.compress_type

	def getComment(self):
		""" Comment for the individual archive member. """
		return self._FILE_INFO.comment

	def getExtra(self):
		""" Expansion field data. """
		return self._FILE_INFO.extra

	def getCreateSys(self):
		""" System which created ZIP archive. """
		return self._FILE_INFO.create_system

	def getCreateVer(self):
		""" PKZIP version which created ZIP archive. """
		return self._FILE_INFO.create_version

	def getExtractVer(self):
		""" PKZIP version needed to extract archive. """
		return self._FILE_INFO.extract_version

	def getReserved(self):
		""" Must be zero. """
		return self._FILE_INFO.reserved

	def getFlagBits(self):
		""" ZIP flag bits. """
		return self._FILE_INFO.flag_bits

	def getVolume(self):
		""" Volume number of file header. """
		return self._FILE_INFO.volume

	def getInternalAttr(self):
		""" Internal attributes. """
		return self._FILE_INFO.internal_attr

	def getExternalAttr(self):
		""" External file attributes. """
		return self._FILE_INFO.external_attr

	def getHeaderOffset(self):
		""" Byte offset to the file header. """
		return self._FILE_INFO.header_offset

	def getCRC(self):
		""" CRC-32 of the uncompressed file. """
		return self._FILE_INFO.CRC

	def getCompressSize(self):
		""" Size of the compressed data. """
		return self._FILE_INFO.compress_size

	def getFileSize(self):
		""" Size of the uncompressed file. """
		return self._FILE_INFO.file_size