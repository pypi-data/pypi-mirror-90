
from typing import final

from . import chain

class Response():

	@final
	def __init__(self, value):
		self.__value = value

	@final
	def get_value(self):
		return self.__value

	@final
	def __or__(self, right):
		return (
			lambda: self,
			lambda: self.get_value(),
		)[right == chain]()
