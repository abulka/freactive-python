# Mucking around with Flet - which is Python driven Flutter

See https://flet.dev/

See discord chat https://discord.com/channels/981374556059086931/1000264673284857866

## Examples

Most examples are copied from the help.

See `text2.py` for a more customised example.

# Musings on reactivity

Is Flet's reversion to imperative programming a step backwards?  Now that I am used to reactive programming, e.g. in vuejs, 
its nice to be able to update data and have all the UI update automatically.  I like model (state) to UI auto binding.

## Flet
In Flet you have to manually update each UI control (which are built via code) property
manually - there is no 'model state' behind the UI control except what you
maintain manually, viz. explicitly updating the model and then also updating the
UI control - a contamination of concerns which cries out for an observing
'Controller' class solution. We will look at this.


```python
counter = 100;                  # STATE
def incrementCounter(e):
    counter += 1                # CODE WHICH CHANGES STATE
    tb1.value = counter         # IMPERATIVE - explicit update of UI
    page.update()               # IMPERATIVE - explicit update of UI whereas in Vuejs and Flutter it is implicit !!!!!

tb1.value = counter             # IMPERATIVE - explicit update of UI (initial state refected to UI)

tb1 = TextField(label="")       # UI WIDGET - DOES NOT REFERENCE STATE
b = ElevatedButton(text="Submit", on_click=incrementCounter)
```

Calling page.update is not so bad, instead of waiting for some magic implicit update to happen...
> Note, there are other places where you have to do an update.  I mean, `drag1.py` shows you can do more nuanced
`e.control.update()` calls but it seems that `page.update()` also works in those cases - so is the nuanced call needed?

But the point is, the lack of proper model to UI binding.

## Flutter
In flutter you have your UI widgets (built via code) refer to state and state
changes are propagated automatically to the UI.  E.g.

```dart
class _MyHomePageState extends State<MyHomePage> {
  int counter = 100;           // STATE
  void incrementCounter() {
    setState(() {
        counter++;             // CODE WHICH CHANGES STATE
    });
  }  
...
    Text(
        '$counter',            // UI WIDGET - REFERENCES STATE
```

## Vuejs
In Vuejs you have your UI components (which uniquely, are built via a HTML
template, not code) refer to state and state changes are propagated
automatically to the UI.  E.g.

```js
let counter = ref(100)          // STATE
function incrementCounter() {
  counter.value++;             // CODE WHICH CHANGES STATE
```
```html
<template>
    <div>
        <h1>{{ counter }}</h1>
        <button @click="incrementCounter">
            Increment
        </button>
    </div>
</template>
```

# Putting Reactivity back into Flet

See example `freactive1-works.py`

Instead of imperitively allowing the Flet UI control event callbacks e.g.
`on_click`, to update the UI directly, we can use a more reactive programming
approach to update the UI. We do this by introducing a level of indirection
whereby the Flet UI control events callbacks instead update a model, and then
the model notifies the UI abstractly, via special observing UI callback
functions e.g. `update_counter_ui`.  The benefit of this approach is that the UI
will be updated automatically whenever the model changes by any other means e.g.
business logic. The updating of the UI becomes a separate concern to the
business logic updating of the model, which brings the architecture more in line
with frameworks like Vuejs and even Flutter.

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

