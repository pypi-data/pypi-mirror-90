enc_in = {
		"&01": "<",
		"&02": " ",
		"&03": "=",
	}

enc_out = {
	"<": "&01",
	" ": "&02",
	"=": "&03"
}

def create_node(node: dict):
	if node != "" and node != None:
		name = node["name"]
		attrs_ = node["attrs"]
		attrs = ""

		for attr in attrs_:
			value = attrs_[attr]

			for enc_out_piece in enc_out:
				value = value.replace(enc_out_piece, enc_out[enc_out_piece])

			attrs += f" {attr}=\"{value}\""

		child = node["value"]

		for enc_out_piece in enc_out:
			child = child.replace(enc_out_piece, enc_out[enc_out_piece])

		for child_ in node["child"]:
			child += create_node(child_)

		return f"<{name}{attrs}>{child}</{name}>"