from web2tree.core.constructions.skeleton_construction import wrap_into_div


def _with_attributes_updated(func):
    def wrapped(self, *args, **kwargs):
        got = func(self, *args, **kwargs)
        self._refresh_attributes()
        return got

    return wrapped


class Node:
    def __init__(self, element, content=None, extract_attrs=None, **attributes):
        self.element = element
        self._props = attributes.pop("props", None)
        self._states = attributes.pop("states", None)
        for attributes in (self._props, self._states):
            assert isinstance(
                attributes, dict
            ), "props or states is supposed to have dictionary data type."
        self.content = content
        self.extract_attrs = extract_attrs
        self._refresh_attributes()

    def _refresh_attributes(self):
        self.attributes = {"props": self._props, "states": self.states}
        self.attrs = None
        if self.extract_attrs is not None:
            self.attrs = self.extract_attrs(self._props, self._states)

    @property
    def props(self):
        return self._props

    @props.setter
    @_with_attributes_updated
    def props(self, new_props):
        assert isinstance(
            new_props, dict
        ), "props is supposed to have dictionary data type."
        self._props = new_props

    @property
    def states(self):
        return self._states

    @states.setter
    @_with_attributes_updated
    def states(self, new_states):
        assert isinstance(
            new_states, dict
        ), "states is supposed to have dictionary data type."
        self._states = new_states

    def to_skeleton(self):
        return wrap_into_div(
            to_be_wrapped=self.element.to_skeleton(
                content=self.content, attrs=self.attrs
            )
        )
