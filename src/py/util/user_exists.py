def user_exists(user: str):
	with open("/etc/passwd", "r") as f:
		return user in {
			line.split(":", 1)[0]
			for line in f.read().split("\n")
		}
