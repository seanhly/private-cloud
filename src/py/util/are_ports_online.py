from typing import Iterable
from socket import socket, AF_INET, SOCK_STREAM, timeout


def are_ports_online(
	host: str = "127.0.0.1", ports: Iterable[int] = None
) -> bool:
	the_socket = socket(AF_INET, SOCK_STREAM)
	the_socket.settimeout(2)
	try:
		for the_port in ports:
			the_socket.connect((host, the_port))
			the_socket.shutdown(2)
		return True
	except (timeout, ConnectionRefusedError, OSError):
		try:
			the_socket.shutdown(2)
		except OSError:
			return False
		return False
