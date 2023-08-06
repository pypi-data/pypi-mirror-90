enc_in = {
		"{RIGHT}": ">",
		"{SPACE}": " ",
		"{EQUAL}": "=",
		"{NL}": "\n",
		"{TAB}": "\t",
		"{BR}": "<br/>"
}

enc_out = {
	">": "{RIGHT}",
	" ": "{SPACE}",
	"=": "{EQUAL}",
	"\n": "{NL}",
	"\t": "{TAB}",
	"<br/>": "{BR}"
}

def create_node(node: dict):
	if node != "" and node != None:
		name = node["name"]
		attrs_ = node["attrs"]
		attrs = ""
		comments = ""

		for attr in attrs_:
			value = attrs_[attr]

			for enc_out_piece in enc_out:
				value = value.replace(enc_out_piece, enc_out[enc_out_piece])

			attrs += f" {attr}=\"{value}\""

		for comment in node["comms"]:
			comments += f"<!--{comment}-->"

		child = ""

		for enc_out_piece in enc_out:
			child = child.replace(enc_out_piece, enc_out[enc_out_piece])

		for child_ in node["child"]:
			child += create_node(child_)

		child += node["value"]

		return f"<{name}{attrs}>{comments}{child}</{name}>"