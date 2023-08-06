# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class TimePicker(Component):
    """A TimePicker component.


Keyword arguments:
- id (string; optional): todo
- value (string; optional)
- defaultValue (string; default moment().format('YYYY-MM-DDTHH:MM:SS.mmmmmm'))
- className (string; optional): Dash-assigned callback that should be called whenever any of the
properties change
- style (dict; optional)
- changed (dict; optional): changed has the following type: dict containing keys 'time', 'timeString'.
Those keys have the following types:
  - time (string; optional): todo
  - timeString (string; optional): todo"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, value=Component.UNDEFINED, defaultValue=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, changed=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'value', 'defaultValue', 'className', 'style', 'changed']
        self._type = 'TimePicker'
        self._namespace = 'dash_ant_design'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'value', 'defaultValue', 'className', 'style', 'changed']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(TimePicker, self).__init__(**args)
