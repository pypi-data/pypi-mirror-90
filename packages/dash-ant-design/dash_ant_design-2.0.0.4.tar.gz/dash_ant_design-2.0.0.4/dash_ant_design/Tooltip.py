# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Tooltip(Component):
    """A Tooltip component.
ExampleComponent is an example component.
It takes a property, `label`, and
displays it.
It renders an input with the property `value`
which is editable by the user.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional)
- id (string; optional): The ID used to identify this component in Dash callbacks
- title (string; optional): A label that will be printed when this component is rendered.
- arrowPointAtCenter (boolean; optional): A label that will be printed when this component is rendered.
- autoAdjustOverflow (boolean; optional): A label that will be printed when this component is rendered.
- color (string; optional): The value displayed in the input
- defaultVisible (boolean; optional)
- destroyTooltipOnHide (boolean; optional)
- mouseEnterDelay (number; optional)
- mouseLeaveDelay (number; optional)
- overlayClassName (string; optional)
- placement (string; optional)
- trigger (list of strings; optional)
- visible (boolean; optional)"""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, title=Component.UNDEFINED, arrowPointAtCenter=Component.UNDEFINED, autoAdjustOverflow=Component.UNDEFINED, color=Component.UNDEFINED, defaultVisible=Component.UNDEFINED, destroyTooltipOnHide=Component.UNDEFINED, mouseEnterDelay=Component.UNDEFINED, mouseLeaveDelay=Component.UNDEFINED, overlayClassName=Component.UNDEFINED, placement=Component.UNDEFINED, trigger=Component.UNDEFINED, visible=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'title', 'arrowPointAtCenter', 'autoAdjustOverflow', 'color', 'defaultVisible', 'destroyTooltipOnHide', 'mouseEnterDelay', 'mouseLeaveDelay', 'overlayClassName', 'placement', 'trigger', 'visible']
        self._type = 'Tooltip'
        self._namespace = 'dash_ant_design'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'title', 'arrowPointAtCenter', 'autoAdjustOverflow', 'color', 'defaultVisible', 'destroyTooltipOnHide', 'mouseEnterDelay', 'mouseLeaveDelay', 'overlayClassName', 'placement', 'trigger', 'visible']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Tooltip, self).__init__(children=children, **args)
