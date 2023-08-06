# eXtensible Markup Language Interface
# Copyright (c) by Kazafka/Kafajku/kzfka - All rights reserved since 2020.

"""
This file is, originally, a part of xmli module for Python, and contains 'xml' class, used to parse and compose XML source code.
"""

from xmli.libs.xml_node import xml_node, PropertyError
from xmli.libs.shared import create_node, enc_in

class xml(object):
	"""
	xml(path: str, create_only: bool = False) -> xml

	With this class you can read an XML file and update it with a simple, object-like interface.
	When used in 'str()', returns (updated in real time) XML file code.
	"""
	def __init__(self: object, path: str, create_only: bool = False) -> object:
		self.path = path
		self.__list = []

		if not create_only:
			file = open(path)
			lines = "".join(file.readlines()).replace("\t", "").replace("\n", "")
			file.close()

			def add_node(line: str, start: dict = None, start_value: dict = None) -> None:
				if start == None:
					start = self.__list

				if line != "" and line != None:
					if line[0] == "<" and line[1] != "/" and line[1] != "!":
						end = line.find(" ")

						if end == -1 or end > line.find(">"):
							end = line.find(">")

						name = line[1:end]

						if name != "":
							if "/" in name:
								name = name.replace("/", "")

							if line.find(f"</{name}>") != -1:
								attrs = line[end:line.find(">")]
							else:
								attrs = line[end:line.find("/>")]

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
								"value": "",
								"comms": []
							})

							if line.find(f"<{name}/>") != -1:
								available = True

								if line.find(f"</{name}>") != -1:
									if line.find(f"<{name}/>") > line.find(f"</{name}>"):
										available = False

								if available:
									if f"<{name}{attrs}>"[-2] == "/":
										return line.replace(f"<{name}{attrs}>", "")
									else:
										return line.replace(f"<{name}{attrs}/>", "")
							else:
								child = line[line.find(f"<{name}{attrs}>") + len(f"<{name}{attrs}>"):line.find(f"</{name}>")]

								result = child

								while True:
									result = add_node(result, start[index]["child"], start[index])

									if result == "":
										break

								return line.replace(f"<{name}{attrs}>{child}</{name}>", "")
					elif line[0] == "<" and line[1] == "!":
						comment = line[line.find("<!--") + len("<!--"):line.find("-->")]

						start_value["comms"].append(comment)

						return line.replace(f"<!--{comment}-->", "")
					else:
						try:
							for enc_in_piece in enc_in:
								line = line.replace(enc_in_piece, enc_in[enc_in_piece])

							end = line.find("<br/>")

							if end == -1:
								end = len(line)
							else:
								child = line[end + len("<br/>"):len(line)]
								
								while True:
									child = add_node(child, start, start_value)

									if child == "":
										break

							start_value["value"] = line[0:end] + start_value["value"]
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

	def get_root_nodes(self: object, **properties: dict) -> list:
		"""
		Returns root nodes.
		"""
		matching = []

		for item in self.__list:
			if len(properties) != 0:
				for property_ in properties:
					try:
						if property_ != "child":
							if item[property_] == properties[property_]:
								matching.append(xml_node(item))
						else:
							raise Exception()
					except:
						raise PropertyError(f"invalid XML node property: '{property_}'")
			else:
				matching.append(xml_node(item))

		return matching

	def add_root_node(self: object, name: str, attrs: dict = {}, value: str = ""):
		"""
		Adds new root node.
		"""
		available = True

		for item in self.__list:
			if item["name"] == name:
				available = False

				break

		if not available:
			raise NameError(f"root node '{name}' already exists")
		else:
			self.__list.append({
				"name": name,
				"attrs": attrs,
				"child": [],
				"value": value
			})