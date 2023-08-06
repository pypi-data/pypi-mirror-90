
class SmartSelfStaticFactory(type):

	def create(cls, *args, **kwargs):
		return isinstance(args[0], cls) \
			and args[0] \
			or super(SmartSelfStaticFactory, cls) \
				.__call__(*args, **kwargs)
