
from __future__ import annotations
from typing import final

from .response import Response
from .smart_self_static_factory import SmartSelfStaticFactory

class Link(metaclass = SmartSelfStaticFactory):

	def __init__(self, handler: callable):
		self.__handler = handler

	@final
	def __call__(self, request):
		return self.handle(request)

	def handle(self, request):
		result = self.__handler(request)

		return self._validate_result(result)

	def _validate_result(self, result):
		if (result is not None):
			return self._response(result)

	@final
	def _response(self, value):
		return Response(value)
