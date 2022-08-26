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

See solution in ![README.md](README.md)
