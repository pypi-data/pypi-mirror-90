
def chain(request_value = None):
	from .request import Request

	return Request(request_value)

from .link import Link
