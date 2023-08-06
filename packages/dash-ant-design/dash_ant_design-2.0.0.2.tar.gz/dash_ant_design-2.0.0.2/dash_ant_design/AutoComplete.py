# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class AutoComplete(Component):
    """An AutoComplete component.
ExampleComponent is an example component.
It takes a property, `label`, and
displays it.
It renders an input with the property `value`
which is editable by the user.

Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks
- allowClear (boolean; optional): A label that will be printed when this component is rendered.
- autoFocus (boolean; optional)
- backfill (boolean; optional)
- defaultActiveFirstOption (boolean; optional)
- defaultOpen (boolean; optional)
- defaultValue (string; optional)
- disabled (boolean; optional)
- dropdownClassName (string; optional)
- notFoundContent (string; optional)
- open (boolean; optional)
- options (dict; optional): options has the following type: list of dicts containing keys 'label', 'value'.
Those keys have the following types:
  - label (string; optional): todo
  - value (string; optional): todo
- placeholder (string; optional)
- style (dict; optional)
- value (string; optional): The value displayed in the input"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, allowClear=Component.UNDEFINED, autoFocus=Component.UNDEFINED, backfill=Component.UNDEFINED, defaultActiveFirstOption=Component.UNDEFINED, defaultOpen=Component.UNDEFINED, defaultValue=Component.UNDEFINED, disabled=Component.UNDEFINED, dropdownClassName=Component.UNDEFINED, notFoundContent=Component.UNDEFINED, open=Component.UNDEFINED, options=Component.UNDEFINED, placeholder=Component.UNDEFINED, style=Component.UNDEFINED, value=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'allowClear', 'autoFocus', 'backfill', 'defaultActiveFirstOption', 'defaultOpen', 'defaultValue', 'disabled', 'dropdownClassName', 'notFoundContent', 'open', 'options', 'placeholder', 'style', 'value']
        self._type = 'AutoComplete'
        self._namespace = 'dash_ant_design'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'allowClear', 'autoFocus', 'backfill', 'defaultActiveFirstOption', 'defaultOpen', 'defaultValue', 'disabled', 'dropdownClassName', 'notFoundContent', 'open', 'options', 'placeholder', 'style', 'value']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(AutoComplete, self).__init__(**args)
