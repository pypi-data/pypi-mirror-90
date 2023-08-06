# hxss.responsibility

Simple implementation of `chain of responsibilities` pattern.

```python
result = chain(request) [ & DefaultLinkClass] [ | <callable|Link>] | chain
```

## Installation

### pip: `hxss.responsibility`

### aur: `python-hxss-responsibility`

## Usage

```python
from hxss.responsibility import chain

def none(value):
	pass

def increment(value):
	return value + 1

def decrement(value):
	return value - 1

request = 1

result = chain(request) | none | increment | decrement | chain
assert(result == 2)

result = chain(request) | none | decrement | increment | chain
assert(result == 0)

result = chain(request) | none | none | none | chain
assert(result == None)
```

## Basics

Chain of responsibilities sequentially handles request by every link until response returned.

By default every `not None` value considered as valid response(some kind of Null coalescing operator):

```python
handled = []

def wrap(func):
	def wrapper(value):
		handled.append(func.__name__)
		return func(value)

	return wrapper

result = chain(request) \
	| wrap(none) \
	| wrap(increment) \
	| wrap(decrement) \
	| chain
assert(result == 2)
assert(handled == ['none', 'increment'])
```

## Lifecycle

* `chain` function creates new `Request`
* every `callable` passed to `Request` by `|` operator wraps into `Link` which handles the request
* once `Link` returns valid `Response` all next `callables` will be ignored
* `| chain` operator forces to return raw response value

## Customization

* custom result validation:
```python
from hxss.responsibility import Link

class FinalLink(Link):
	def _validate_result(self, result): # see default Link implementation
		return self._response(result)

result = chain(1) | FinalLink(none) | increment | decrement | chain
assert(result == None)
```

* custom independent link:
```python
class CustomLink(Link):
	def __init__(self):
		pass

	def handle(self, request):
		result = calc_result(request)

		return self._response(result)

result = chain(1) | increment | CustomLink() | decrement | chain
```

* custom default link:
```python
class InversedLink(Link):
	def _validate_result(self, result):
		if (result is None):
			return self._response(result)

result = chain(1) & InversedLink | increment | CustomLink() | decrement | chain
assert(result == None)
```
