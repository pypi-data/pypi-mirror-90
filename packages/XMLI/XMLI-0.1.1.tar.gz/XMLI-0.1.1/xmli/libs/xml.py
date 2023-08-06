# eXtensible Markup Language Interface
# Copyright (c) by Kazafka/Kafajku/kzfka - All rights reserved since 2020.

"""
This file is, originally, a part of xmli module for Python, and contains 'xml' class, used to parse and compose XML source code.
"""

from xmli.libs.xml_node import xml_node
from xmli.libs.shared import create_node, enc_in

class xml(object):
	"""
	xml(path: str) -> xml

	With this class you can read an XML file and update it with a simple, object-like interface.
	When used in 'str()', returns (updated in real time) XML file code.
	"""
	def __init__(self: object, path: str) -> object:
		self.path = path
		self.__list = []

		file = open(path)
		lines = "".join(file.readlines()).replace("\t", "").replace("\n", "")
		file.close()

		def add_node(line: str, start: dict = None, start_value: dict = None) -> None:
			if start == None:
				start = self.__list

			if line != "" and line != None:
				if line[0] == "<" and line[1] != "/":
					end = line.find(" ")

					if end == -1 or end > line.find(">"):
						end = line.find(">")

					name = line[1:end]

					if name != "":
						attrs = line[end:line.find(">")]
						attrs_ = attrs.split(" ")
						attrs__ = {}

						for attr in attrs_:
							try:
								value = eval(attr.split("=")[1])

								for enc_in_piece in enc_in:
									value = value.replace(enc_in_piece, enc_in[enc_in_piece])

								attrs__[attr.split("=")[0]] = value
							except:
								pass

						index = len(start)

						start.append({
							"name": name,
							"attrs": attrs__,
							"child": [],
							"value": ""
						})

						child = line[line.find(f"<{name}{attrs}>") + len(f"<{name}{attrs}>"):line.find(f"</{name}>")]

						result = child

						while True:
							result = add_node(result, start[index]["child"], start[index])

							if result == "":
								break

						line = line.replace(f"<{name}{attrs}>{child}</{name}>", "")

						return line
				else:
					try:
						for enc_in_piece in enc_in:
							line = line.replace(enc_in_piece, enc_in[enc_in_piece])

						start_value["value"] = line
					except:
						pass
			else:
				return ""

		while True:
			lines = add_node(lines)

			if lines == "":
				break

	def __str__(self: object) -> object:
		nodes = ""

		for node in self.__list:
			nodes += create_node(node)

		return nodes

	def update(self: object) -> None:
		"""
		Updates the XML file.
		"""
		nodes = ""

		for node in self.__list:
			nodes += create_node(node)

		file = open(self.path, "w")
		file.write(nodes)
		file.close()

	def get_root_node(self: object, name: str) -> xml_node:
		"""
		If present, returns root node.
		"""
		present = False
		root = {}

		for item in self.__list:
			if item["name"] == name:
				present = True
				root = item
				
				break

		if present:
			return xml_node(root)
		else:
			raise NameError(f"unknown root node: '{name}'")