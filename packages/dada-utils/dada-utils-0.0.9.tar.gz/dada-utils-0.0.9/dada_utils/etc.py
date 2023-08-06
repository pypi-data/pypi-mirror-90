# -*- coding: utf-8 -*-
"""
Random helper functions / decorators
This library should not import from other modules.
"""
from functools import wraps
from typing import Union, Any, Dict, Optional, List

# ////////


def unlist(lst: Union[list, Any]) -> Any:
    """
    Get the first value of a list
    param v:
    """
    if isinstance(lst, list):
        if not len(lst):
            return None
    return lst[0]


def dict_filter_nulls(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Filter null values from a dictionary
    :param data: The data to filter as a dict
    :return dict
    """
    return {
        k: v
        for k, v in data.items()
        if (v is not None and str(v).strip() != "")
        and (k is not None and str(k).strip() != "")
    }


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def get_fields_data(
    fields: dict, prefix: Optional[str] = None, defaults: Dict[str, Any] = {}
) -> AttrDict:
    """
    Get fields data as dict, adding a prefix to the field name
    :param fields: a dictionary of fields
    :param prefix: the prefix to prepend to every field name
    :param defaults: the defaults to overwrite with parsed fields.
    :return dict
    """
    if prefix:
        if not prefix.endswith("_"):
            prefix += "_"
    if not prefix:
        prefix = ""

    def _prefix(k):
        if k.startswith(prefix):
            return k
        return f"{prefix}{k}"

    if not defaults:
        defaults = {}
    default_fields = {_prefix(k): v for k, v in dict_filter_nulls(defaults).items()}
    new_fields = {_prefix(k): v for k, v in dict_filter_nulls(fields).items()}
    default_fields.update(new_fields)
    return AttrDict(default_fields)


def uniq(lst: List[Any], idfun=lambda x: x) -> List[Any]:
    """
    Order-preserving unique function.
    :param lst: The list to make unique
    :param idfun: The function to create the elements ID
    :return list
    """
    # order preserving
    seen = {}
    result = []
    for item in lst:
        marker = idfun(item)
        if marker in seen:
            continue
        seen[marker] = 1
        result.append(item)
    return result


def memoized_property(fget):
    """
    Return a property attribute for new-style classes that only calls its getter on the first
    access. The result is stored and on subsequent accesses is returned, preventing the need to
    call the getter any more.
    Example::
        >>> class C(object):
        ...     load_name_count = 0
        ...     @memoized_property
        ...     def name(self):
        ...         "name's docstring"
        ...         self.load_name_count += 1
        ...         return "the name"
        >>> c = C()
        >>> c.load_name_count
        0
        >>> c.name
        "the name"
        >>> c.load_name_count
        1
        >>> c.name
        "the name"
        >>> c.load_name_count
        1
    """
    attr_name = "_{0}".format(fget.__name__)

    @wraps(fget)
    def fget_memoized(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fget(self))
        return getattr(self, attr_name)

    return property(fget_memoized)
