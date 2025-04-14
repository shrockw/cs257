
def get_data(filename):
	with open(filename, "r", encoding="utf-8") as f:
		data = f.readlines()
	return data