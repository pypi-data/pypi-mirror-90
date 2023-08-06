# eXtensible Markup Language Interface
# Copyright (c) by Kazafka/Kafajku/kzfka - All rights reserved since 2020.

"""
This file is, originally, a part of xmli module for Python, and contains 'xml_node' class, which is used to manage single XML nodes.
"""

from xmli.libs.shared import create_node

class xml_node(object):
	"""
	xml_node(node: dict) -> xml_node

	Used to manage single XML nodes.
	Should be used only by 'xml' class and self objects.
	When used in e.g. 'print' function, returns it's dict.
	When called, returns it's representation of real XML node.
	"""
	def __init__(self: object, node: dict) -> object:
		self.__node = node

	def __str__(self: object) -> object:
		return str(self.__node)

	def __call__(self: object) -> str:
		return create_node(self.__node)

	def get_value(self: object) -> str:
		"""
		Returns value of the XML node.
		"""
		return self.__node["value"]

	def set_value(self: object, value: str) -> None:
		"""
		Changes value of the XML node.
		"""
		self.__node["value"] = value

	def get_attr(self: object, name: str) -> str or None:
		"""
		Retrieves XML node attribute from the list of available.
		"""
		return self.__node["attrs"][name]

	def set_attr(self: object, name: str, value: str) -> None:
		"""
		Redefines XML node attribute.
		"""
		self.__node["attrs"][name] = value

	def get_child(self: object) -> list:
		"""
		Returns a list of XML node children.
		"""
		return [xml_node(node) for node in self.__node["child"]]