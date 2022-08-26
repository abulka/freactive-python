# freactive - simple reactivity

def autoproperty(name, can_get=True, can_set=True, allow_null=False, default_value=0, callback=None):
    """Decorator function which auto creates a getter and setter for the class attribute 'name' being passed in. 
    The 'callback' function, if present, is called when the attribute state changes, the arguments are the attribute name and the new value.
    A special class property '_auto_properties' is created which contains a list of all auto properties.
    A special boot method is created which sets the values of all auto properties to their current values, 
    thereby triggering all the callbacks.  This is good for setting up the initial state of the application.
    """
    attribute_name = '_' + name

    def getter(self):
        return getattr(self, attribute_name, default_value)

    def setter(self, value):
        if not allow_null and value is None:
            raise ValueError('Cannot set {} to None'.format(name))
        setattr(self, attribute_name, value)
        if callback:
            callback(name, value)

    prop = property(getter if can_get else None, setter if can_set else None)

    def boot(self):
        for auto_prop in self._auto_properties:
            setattr(self, auto_prop, getattr(self, auto_prop))

    def decorator(cls):
        setattr(cls, name, prop)

        # add boot function if not already present
        if not getattr(cls, 'boot', None):
            setattr(cls, 'boot', boot)

        # add auto property if not already present, which records all the auto properties
        if not getattr(cls, '_auto_properties', None):
            setattr(cls, '_auto_properties', [])

        getattr(cls, '_auto_properties').append(name)

        return cls

    return decorator


if __name__ == '__main__':

    # observing callbacks, typically used for updating the UI
    def exampleObserver1(arg1, arg2=None):
        print('observing change in', arg1, 'to', arg2)

    def weatherChanged(arg1, arg2=None):
        print('weather changed', 'to', arg2)

    @autoproperty('counter', can_get=True, can_set=True, allow_null=False, default_value=10, callback=exampleObserver1)
    @autoproperty('total', can_get=True, can_set=True, allow_null=False, default_value=0, callback=exampleObserver1)
    @autoproperty('weather', can_get=True, can_set=True, allow_null=False, default_value='sunny', callback=weatherChanged)
    class ExampleModel:
        pass

    model = ExampleModel()
    print('_auto_properties are', model._auto_properties)

    print('initial values', 'counter', model.counter,
          'total', model.total, 'weather', model.weather)
    model.boot()
    model.counter = 100
    model.counter = 200
    model.total += 1
    model.weather = "stormy"
