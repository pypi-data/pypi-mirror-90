# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class TreeSelect(Component):
    """A TreeSelect component.


Keyword arguments:
- id (string; optional): todo
- treeData (list; optional): todo
- showCheckedStrategy (string; optional): todo
- treeCheckable (boolean; optional): todo
- disabled (boolean; optional)
- defaultValue (list of strings; optional)
- treeCheckStrictly (boolean; optional): todo
- selected (string; optional): todo
- style (dict; optional)
- expanded (list of strings; optional): todo
- changed (dict; optional): todo. changed has the following type: list of dicts containing keys 'label', 'value'.
Those keys have the following types:
  - label (string; optional): todo
  - value (string; optional): todo"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, treeData=Component.UNDEFINED, showCheckedStrategy=Component.UNDEFINED, treeCheckable=Component.UNDEFINED, disabled=Component.UNDEFINED, defaultValue=Component.UNDEFINED, treeCheckStrictly=Component.UNDEFINED, selected=Component.UNDEFINED, style=Component.UNDEFINED, expanded=Component.UNDEFINED, changed=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'treeData', 'showCheckedStrategy', 'treeCheckable', 'disabled', 'defaultValue', 'treeCheckStrictly', 'selected', 'style', 'expanded', 'changed']
        self._type = 'TreeSelect'
        self._namespace = 'dash_ant_design'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'treeData', 'showCheckedStrategy', 'treeCheckable', 'disabled', 'defaultValue', 'treeCheckStrictly', 'selected', 'style', 'expanded', 'changed']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(TreeSelect, self).__init__(**args)
