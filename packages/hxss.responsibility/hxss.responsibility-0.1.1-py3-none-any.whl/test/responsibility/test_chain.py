
import unittest

from hxss.responsibility import chain, Link

class TestChain(unittest.TestCase):

	def setUp(self):
		self.handled = []

	def test_flow(self):
		none = self.none
		increment = self.increment
		decrement = self.decrement

		result = chain(1) | none | increment | decrement | chain
		self.assertEqual(result, 2)
		self.assertEqual(self.handled, ['none', 'increment'])

		self.setUp()
		result = chain(1) | none | decrement | increment | chain
		self.assertEqual(result, 0)
		self.assertEqual(self.handled, ['none', 'decrement'])

		self.setUp()
		result = chain(1) | none | none | none | chain
		self.assertEqual(result, None)
		self.assertEqual(self.handled, ['none', 'none', 'none'])

	def test_custom_result_validation(self):
		none = self.none
		increment = self.increment
		decrement = self.decrement

		class FinalLink(Link):
			def _validate_result(self, result):
				return self._response(result)

		result = chain(1) | FinalLink(none) | increment | decrement | chain
		self.assertEqual(result, None)
		self.assertEqual(self.handled, ['none'])

	def test_custom_link(self):
		increment = self.increment
		decrement = self.decrement

		handled = self.handled

		class CustomLink(Link):
			def __init__(self):
				pass

			def handle(self, request):
				handled.append('CustomLink')
				return self._response(None)

		result = chain(1) | CustomLink() | increment | decrement | chain
		self.assertEqual(result, None)
		self.assertEqual(self.handled, ['CustomLink'])

	def test_custom_request(self):
		none = self.none
		increment = self.increment
		decrement = self.decrement

		class InversedLink(Link):
			def _validate_result(self, result):
				if (result is None):
					return self._response(result)

		result = chain(1) & InversedLink | increment | none | decrement | chain
		self.assertEqual(result, None)
		self.assertEqual(self.handled, ['increment', 'none'])

	def none(self, value):
		self.handled.append('none')

	def increment(self, value):
		self.handled.append('increment')

		return value + 1

	def decrement(self, value):
		self.handled.append('decrement')

		return value - 1
