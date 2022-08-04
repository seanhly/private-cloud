def group_exists(group: str):
	with open("/etc/group", "r") as f:
		return group in {
			line.split(":", 1)[0]
			for line in f.read().split("\n")
		}
