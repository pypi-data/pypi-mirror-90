eXtensible Markup Lanuage Interface

-----------------------------------

**Opening the file**

First of all, you have to import `xml` class from the `xmli` module. Then, open an XML file by syntax: `file = xml("path_to_file.xml")`

List of methods available for `xml` class instance:

`__str__(self: object) -> object`
Returns `xml` class representation of an XML file (Python `list`).

`__call__(self: object) -> str`
Returns composed XML file code.

`update(self: object) -> None`
Updates the XML file.

`get_root_node(self: object) -> xml_node`
If root node present, returns it as `xml_node` class instance.

**Managing XML nodes**

When you've opened the file and retrieved it's root node, you can now set attributes, add children (sub-nodes) set the value of the root node or just change it's name.

List of methods available for `xml_node` class instance:

`__str__(self: object) -> object`
Returns `xml_node` class representation of an XML node (Python `dict`).

`__call__(self: object) -> str`
Returns composed XML node.

`get_value(self: object) -> str`
Retrieves the value of an XML node.

`set_value(self: object, value: str) -> None`
Changes the value of an XML node.

`get_attr(self: object, name: str) -> str or None`
If an attribute is present, function retrieves it's value and returns it.

`set_attr(self: object, name: str, value: str) -> None`
Redefines an attribute of XML node. If attribute is not present, new will be created.

-------------------------------------------------------------------------------------

**Other**

**Encoding**

By default, when XML file is composed or parsed, it goes through a process of encoding. This simple method prevents from many issues when parsing an XML file. Default encoding can be found in `xmli.libs.shared` (`enc_in` - used when parsing XML file, `enc_out` - used when composing XML file).

-------------

Last changes:

* none
