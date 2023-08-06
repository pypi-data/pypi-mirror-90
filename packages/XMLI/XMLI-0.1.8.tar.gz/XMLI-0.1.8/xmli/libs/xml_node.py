# eXtensible Markup Language Interface
# Copyright (c) by Kazafka/Kafajku/kzfka - All rights reserved since 2020.

"""
This file is, originally, a part of xmli module for Python, and contains 'xml_node' class, which is used to manage single XML nodes.
"""

from xmli.libs.shared import create_node

class PropertyError(Exception):
	pass

class xml_node(object):
	"""
	xml_node(node: dict) -> xml_node

	Used to manage single XML nodes.
	Should be used only by 'xml' class and self objects.
	When used in 'str()', returns XML node based on itself.
	"""
	def __init__(self: object, node: dict) -> object:
		self.__node = node

	def __str__(self: object) -> object:
		return create_node(self.__node)

	def get_name(self: object) -> str:
		"""
		Retrieves the name of XML node.
		"""
		return self.__node["name"]

	def set_name(self: object, name: str) -> None:
		"""
		Redefines the name of XML node.
		"""
		self.__node["name"] = name

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

	def get_comments(self: object) -> list:
		"""
		Returns a list with XML node comments.
		"""
		return self.__node["comms"]

	def add_comment(self: object, comment: str) -> None:
		"""
		Adds a new comment.
		"""
		self.__node["comms"].append(comment)

	def del_comment(self: object, comment: str) -> None:
		"""
		Removes a comment.
		"""
		self.__node["comms"].remove(comment)

	def add_child(self: object, name: str, attrs: dict = {}, value: str = ""):
		"""
		Adds new child to the XML node.
		"""
		self.__node["child"].append({
			"name": name,
			"attrs": attrs,
			"child": [],
			"value": value
		})

	def get_child(self: object, **properties) -> list:
		"""
		Returns a list of XML node children.
		"""
		matching = []

		for item in self.__node["child"]:
			if len(properties) != 0:
				for property_ in properties:
					try:
						if item[property_] == properties[property_]:
							if property_ != "child":
								matching.append(xml_node(item))
							else:
								raise Exception()
					except:
						raise PropertyError(f"invalid XML node property: '{property_}'")
			else:
				matching.append(xml_node(item))

		return matching