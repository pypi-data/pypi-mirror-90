
from typing import final

from . import chain
from . import Link
from .response import Response

class Request():

	def __init__(self, value = None):
		self.__value = value
		self.__link_class = Link

	@final
	def __and__(self, right):
		self.__link_class = right

		return self

	@final
	def __or__(self, right):
		if (right != chain):
			return self.__handle(right)

	def __link(self, handler: callable):
		return self.__link_class.create(handler)

	def __handle(self, handler: callable):
		result = self.__link(handler) \
			.handle(self.__value)

		return (
			self,
			result,
		)[isinstance(result, Response)]
