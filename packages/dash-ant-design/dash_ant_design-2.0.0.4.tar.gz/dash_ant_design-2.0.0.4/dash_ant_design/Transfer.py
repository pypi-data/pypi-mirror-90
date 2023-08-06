# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Transfer(Component):
    """A Transfer component.
ExampleComponent is an example component.
It takes a property, `label`, and
displays it.
It renders an input with the property `value`
which is editable by the user.

Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks
- dataSource (dict; optional): A label that will be printed when this component is rendered. dataSource has the following type: list of dicts containing keys 'key', 'title', 'description', 'disabled'.
Those keys have the following types:
  - key (string; optional)
  - title (string; optional)
  - description (string; optional)
  - disabled (boolean; optional)
- disabled (boolean; optional): A label that will be printed when this component is rendered.
- oneWay (boolean; optional)
- operations (list of strings; optional)
- pagination (boolean; optional)
- selectedKeys (list of strings; optional)
- showSearch (boolean; optional)
- showSelectAll (boolean; optional)
- targetKeys (list of strings; optional)
- listStyle (dict; optional)
- titles (list of strings; optional)
- changed (list of strings; optional)
- sourceSelectedKeys (list of strings; optional)
- targetSelectedKeys (list of strings; optional)"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, dataSource=Component.UNDEFINED, disabled=Component.UNDEFINED, oneWay=Component.UNDEFINED, operations=Component.UNDEFINED, pagination=Component.UNDEFINED, selectedKeys=Component.UNDEFINED, showSearch=Component.UNDEFINED, showSelectAll=Component.UNDEFINED, targetKeys=Component.UNDEFINED, listStyle=Component.UNDEFINED, titles=Component.UNDEFINED, changed=Component.UNDEFINED, sourceSelectedKeys=Component.UNDEFINED, targetSelectedKeys=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'dataSource', 'disabled', 'oneWay', 'operations', 'pagination', 'selectedKeys', 'showSearch', 'showSelectAll', 'targetKeys', 'listStyle', 'titles', 'changed', 'sourceSelectedKeys', 'targetSelectedKeys']
        self._type = 'Transfer'
        self._namespace = 'dash_ant_design'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'dataSource', 'disabled', 'oneWay', 'operations', 'pagination', 'selectedKeys', 'showSearch', 'showSelectAll', 'targetKeys', 'listStyle', 'titles', 'changed', 'sourceSelectedKeys', 'targetSelectedKeys']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Transfer, self).__init__(**args)
