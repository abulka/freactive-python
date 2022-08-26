"""
Example of adding some form of reactive programming to Flet.

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
"""

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
