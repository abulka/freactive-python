# Freactive 

A simple reactive library for Python - use in Flet, wxPython and other imperative frameworks

## Usage

1. Copy `freactive.py` into your project and import the decorator `autoproperty`.

```python
from freactive import autoproperty
```

2. Create a model class and use the decorator to create reactive properties.

```python
@autoproperty('counter', default_value=100, callback=update_counter_ui)
@autoproperty('weather', default_value='sunny', callback=update_weather_ui)
class Model:
    pass

model = Model()
```

3. In your UI framework event handlers set properties on the model. **Do not** manually update the UI in these event handlers (that's just too imperative!).

4. Place the code which updates the UI into the `callback` functions referred to by the `@autoproperty` decorator.

See the [Flet](https://flet.dev/docs/) example below for a simple runnable application using this approach.

## The `autoproperty` decorator

Adds a simple form of reactivity to any class.

- Automatically creates a getter and setter for the class attribute `name` being passed in. 
- The `callback` function, if present, is called when the attribute state changes, the two arguments are the attribute name and the new value. 

Additionally:

- A special class property `_auto_properties` is created which contains a list of all auto properties. Use this for reference.
- A special `boot` method is created which sets the values of all auto properties to their current values, thereby triggering all the callbacks.  This is good for setting up the initial state of the application.

> Theoretically, since the decorated `Model` is in fact a `Subject` in a Subject-Observer design pattern, I initially considered implementing the decorator 'callback' function differently, and have it call an Observer object's `onNotify()` method which would update the UI. Such an object would have been a kind of `Controller`. However, this approach was not taken because it requires creating a new Observer object for each model property, whereas callback functions are simpler.


# Putting Reactivity back into Flet

Is Flet's reversion to imperative programming a step backwards?  These days I am used to reactive programming, e.g. in vuejs, 
its nice to be able to update data and have all the UI update automatically.  I like model (state) to UI auto binding.

## Possible Solution

Instead of imperitively allowing the Flet UI control event callbacks e.g.
`on_click`, to update the UI directly, we can use a more reactive programming
approach to update the UI. 

We do this by introducing a level of indirection
whereby the Flet UI control events callbacks instead update a model, and then
the model notifies the UI abstractly, via special observing UI callback
functions e.g. `update_counter_ui`.  

The benefit of this approach is that the UI
will be updated automatically whenever the model changes by any other means e.g.
business logic. The updating of the UI becomes a separate concern to the
business logic updating of the model, which brings the architecture more in line
with frameworks like Vuejs and even Flutter.

Example `flet_example1.py`

```python
import flet
from flet import ElevatedButton, Page, TextField
from freactive import autoproperty


def main(page: Page):

    def incrementCounter(e):
        model.counter += 1  # don't update the UI directly, update the model instead

    def changeWeather(e):
        model.weather = 'rainy'

    tb1 = TextField(label="")
    b = ElevatedButton(text="Increment", on_click=incrementCounter)
    tb2 = TextField(label="")
    b2 = ElevatedButton(text="Change Weather", on_click=changeWeather)
    page.add(tb1, b, tb2, b2)

    # Define observing callback functions for the model attributes - these update the UI

    def update_counter_ui(arg1, arg2=None):
        tb1.value = arg2
        page.update()

    def update_weather_ui(arg1, arg2=None):
        tb2.value = arg2
        page.update()

    # Define the model

    @autoproperty('counter', default_value=100, callback=update_counter_ui)
    @autoproperty('weather', default_value='sunny', callback=update_weather_ui)
    class Model:
        pass

    model = Model()
    model.boot()  # causes all observing callbacks to be called, which updates the UI with the initial state of the model


flet.app(target=main)
```

## Resources

See https://flet.dev/

See discord chat https://discord.com/channels/981374556059086931/1000264673284857866

See [My musings on reactivity](./musings.md)

