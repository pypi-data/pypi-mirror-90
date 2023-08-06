# -*- coding: utf-8 -*-
"""
Basic Usage of **JsonModel**
============================

JsonModel is designed to pre-define a dictionary with type testing and conversion. Its
secondary task is to eliminate occuring magic constants of dictionary keys.

.. testsetup::

   from jsonmetamodel import JsonModel, JsonInteger, JsonString

class definition
----------------

A JsonModel is defined by declaring attributes with *IDataType*, which defines

.. testcode::

    class Person(JsonModel):
        name = JsonString(default="Not Sure")
        age = JsonInteger(default=538)

    print(Person())

.. testoutput::

    MappingTreeItem({'name': 'Not Sure', 'age': 538})


access to dictionary key values
-------------------------------

The key values can be obtained by *attribute_name* of the declared *IDataType*
attributes of a JsonModel.

.. testcode::

    richard_watterson = Person({'age': 538, 'name': 'Richard Watterson'})
    richard_watterson[Person.age.attribute_name] = "38"
    print(richard_watterson[Person.age.attribute_name])

.. testoutput::

    38

The JsonModel-class
===================

.. autoclass:: JsonModel
   :members:

"""

import logging
import copy
from jsonmetamodel.fieldtypes import ADataType
from augmentedtree import (
    augment_datastructure,
    MappingTreeItem,
)
from typing import Mapping, Optional, Dict
from dicthandling import keep_keys


LOGGER = logging.getLogger("jsonmetamodel")


# The custom dictionary
class _member_table(dict):
    """
    Class member table for the Model class.

    Attributes
    ----------
    :Fields: Contains IDataType Objects as column data type definitions.
    :Defaults: Contains a dictionary with the default values.
    :KeyPairs: Contains a dictionary with the Attribute-Key and its column key
    :ColumnNames: List of column names.
    """

    def __init__(self):
        self.field_types: dict = {}
        self.defaults: dict = {}
        self.attribute_names: dict = {}
        self.primarykeys: dict = {}

    def __setitem__(self, attribute_name, attribute_value):
        # if the key is not already defined, add to the
        # list of keys.
        if isinstance(attribute_value, ADataType):
            # if no different columnname was defined the attribute name is
            # used as the dictionary key.
            attribute_value.set_attribute_name(attribute_name)
            attributes_destination_name = attribute_value.primekey
            self.field_types[attributes_destination_name] = attribute_value
            self.attribute_names[attribute_name] = attributes_destination_name
            self.primarykeys[attributes_destination_name] = attribute_name
            # Call superclass to add Additional attribute
            # dict.__setitem__(self, attribute_name, value_or_idatatype.columnname)
            self.defaults[attributes_destination_name] = attribute_value.default
        dict.__setitem__(self, attribute_name, attribute_value)


class JsonModelClass(type):
    # The prepare function
    @classmethod
    def __prepare__(mcs, name, bases):  # No keywords in this case
        finalTable = _member_table()
        for base in bases:
            finalTable.field_types.update(base.field_types)
            finalTable.defaults.update(base.defaults)
            finalTable.attribute_names.update(base.attribute_names)
            finalTable.primarykeys.update(base.primarykeys)
        return finalTable

    # The metaclass invocation
    def __new__(mcs, name, bases, classdict):
        # Note that we replace the classdict with a regular
        # dict before passing it to the superclass, so that we
        # don't continue to record member names after the class
        # has been created.
        _result = type.__new__(mcs, name, bases, dict(classdict))
        _result.defaults = classdict.defaults
        _result.field_types = classdict.field_types
        _result.attribute_names = classdict.attribute_names
        _result.primarykeys = classdict.primarykeys
        return _result


class JsonModel(metaclass=JsonModelClass):
    def __new__(
        cls, data: Mapping = None, use_model_keyorder: bool = False, **kwargs
    ) -> MappingTreeItem:
        """
        The **JsonModel**-class is an interface like definition of dictionaries
        with type checking and conversion capabilities.

        Examples:

            >>> from jsonmetamodel import JsonModel, JsonInteger, JsonString
            >>> class Person(JsonModel):
            ...     name = JsonString(default="Not Sure")
            ...     age = JsonInteger(default=538)
            ...
            >>> Person()
            MappingTreeItem({'name': 'Not Sure', 'age': 538})

            >>> class ABunchOfItems(JsonModel):
            ...     any = JsonString()
            ...     thing = JsonString()
            ...     here = JsonString()
            ...     and_a = JsonModel()
            ...     lot = JsonModel()
            ...
            >>> ABunchOfItems(any='value and', lot='more')
            MappingTreeItem({'any': 'value and', 'thing': '', 'here': '', 'lot': 'more'})

        Args:
            data (Mapping):
                This given data as a Mapping will update the predefined fields
                of this class.

            use_model_keyorder (bool):
                States if the key order of this class will be forced upon the
                result. If not, the order of the incoming data is used.

            **kwargs: iterable if data is given.

        Returns:
            MappingTreeItem (Mapping)
        """
        return cls._get_treeitem(data, use_model_keyorder, **kwargs)

    @classmethod
    def _get_keypairs_of_different_associations(cls):
        result = {}
        for attributen_name, primarykey in cls.attribute_names.items():
            if attributen_name != primarykey:
                result[attributen_name] = primarykey
        return result

    @classmethod
    def _override_data_with_keyword_arguments(
        cls, data: Optional[Mapping], overriding_kwargs: dict
    ) -> dict:
        """
        .. doctest::
           :hide:

            >>> from jsonmetamodel import JsonModel, JsonInteger, JsonString
            >>> class Person(JsonModel):
            ...     name = JsonString(default="Not Sure")
            ...     age = JsonInteger(default=538)
            ...
            >>> sample_data = {"something": "not_in_person", "age": 1}
            >>> fake_kwargs = {"age": 4}
            >>> Person._override_data_with_keyword_arguments(sample_data, fake_kwargs)
            {'name': 'Not Sure', 'age': 4, 'something': 'not_in_person'}

        Args:
            data(Optional[Mapping]):
                Mapping which is going to be overriden by additional keyword
                arguments.

            overriding_kwargs(Dict):
                Given keyword arguments, which override the given data.

        Returns:
            dict
        """
        required_defaults = cls.defaults.copy()
        if data is not None:
            required_defaults.update(data)
        required_defaults.update(overriding_kwargs)
        return required_defaults

    @classmethod
    def _retrieve_default(cls) -> MappingTreeItem:
        """
        .. doctest::
           :hide:

            >>> from jsonmetamodel import JsonModel, JsonInteger, JsonString
            >>> class Person(JsonModel):
            ...     name = JsonString(default="Not Sure")
            ...     age = JsonInteger(default=538)
            ...
            >>> Person._retrieve_default()
            MappingTreeItem({'name': 'Not Sure', 'age': 538})

        Returns:
            MappingTreeItem
        """
        default_data = cls.defaults.copy()
        treeitem: MappingTreeItem = augment_datastructure(nested_data=default_data, )
        treeitem.set_field_types(cls.field_types.copy())
        return treeitem

    @classmethod
    def _get_treeitem(
        cls, data: Mapping, use_model_keyorder: bool, **kwargs
    ) -> MappingTreeItem:
        do_retrieve_complete_default = (data is None) and (not kwargs)
        if do_retrieve_complete_default:
            return cls._retrieve_default()

        overridden_data = cls._override_data_with_keyword_arguments(data, kwargs)
        requested_names = set(list(overridden_data))
        needed_names = set(cls.primarykeys)
        fieldnames_to_add = needed_names.difference(requested_names)
        fieldnames_to_convert = requested_names.intersection(needed_names)

        for fieldname in fieldnames_to_convert:
            try:
                value_to_convert = overridden_data[fieldname]
                converter = cls.field_types[fieldname]
                overridden_data[fieldname] = converter(value_to_convert)
            except ValueError:
                errormsg = (
                    "Given value for field `{}` could not be converted into"
                    " destined type `{}`.".format(fieldname, cls.field_types[fieldname])
                )
                raise ValueError(errormsg)

        if use_model_keyorder:
            resulting_data = cls.defaults.copy()
            resulting_data.update(overridden_data)
        else:
            for fieldname in fieldnames_to_add:
                overridden_data[fieldname] = cls.defaults[fieldname]
            resulting_data = overridden_data

        different_keypairs = cls._get_keypairs_of_different_associations()
        treeitem_with_modelattributes = augment_datastructure(
            nested_data=resulting_data,
        )
        treeitem_with_modelattributes.set_field_types(cls.field_types.copy())
        treeitem_with_modelattributes.set_keypairs_of_related_values(different_keypairs)
        return treeitem_with_modelattributes

    @classmethod
    def extract(cls, data: Mapping, checkgroup_name: str = None) -> MappingTreeItem:
        """
        Returns an *AttributedMappingTreeItem* of this class with the
        values of *data* for keys which fit to this class.

        Args:
            data (dict):
                Data which shall be used.

            checkgroup_name (str; optional):
                default = None; Group which should be extracted.

        Returns:
            AttributedMappingTreeItem:
                Intersection between data and this JsonModel's attributes.
        """
        if not isinstance(data, dict):
            raise ValueError("Given data has to be a dictionary.")
        field_names_to_keep = cls.get_checkgroup_membernames(checkgroup_name)
        result = keep_keys(data, field_names_to_keep)
        return cls(result)

    @classmethod
    def intersect(cls, incoming_data: dict):
        """
        Intersection of fields within the `incoming_data` and this
        JsonModels definition.

        Args:
            incoming_data (dict):
                Data which fields intersecting with this JsonModel
                should remain.
        Returns:
            MappingTreeItem:
                Returning fields, which are fields of this JsonModel,
                but does not fill in missing fields into data.

        Examples:

            >>> from jsonmetamodel import JsonModel, JsonString
            >>> class Fruit(JsonModel):
            ...     color = JsonString()
            ...     type = JsonString()
            ...
            >>> apple = {'type': 'apple', 'color': 'red', 'variety': 'Golden Delicious'}
            >>> Fruit.intersect(apple)
            MappingTreeItem({'type': 'apple', 'color': 'red'})

        """
        if not isinstance(incoming_data, Mapping):
            raise ValueError("Given data has to be a Mapping.")
        remaining_data = copy.deepcopy(incoming_data)
        existing_field_names = list(incoming_data)
        for fieldname in existing_field_names:
            if fieldname not in cls.primarykeys:
                remaining_data.pop(fieldname)

        different_keypairs = cls._get_keypairs_of_different_associations()
        treeitem_with_modelattributes = augment_datastructure(
            nested_data=remaining_data,
        )
        treeitem_with_modelattributes.set_field_types(cls.field_types.copy())
        treeitem_with_modelattributes.set_keypairs_of_related_values(different_keypairs)
        return treeitem_with_modelattributes

    @classmethod
    def get_blank(cls) -> dict:
        """
        Returns a dictionary with the default values as a copy.

        Returns:
            dict:
                Dictionary with default values of this JsonModel

        Examples:

            >>> from jsonmetamodel import JsonModel, JsonInteger, JsonString
            >>> class Person(JsonModel):
            ...     name = JsonString(default="Not Sure")
            ...     age = JsonInteger(default=538)
            ...
            >>> Person.get_blank()
            {'name': 'Not Sure', 'age': 538}

        """
        return cls.defaults.copy()

    @classmethod
    def check(cls, data: Mapping, checkgroup_name: str = None) -> bool:
        """
        Checks if given data fits to the defined fields of this
        JsonModel and/or specific checkgroup.

        Args:
            data (Mapping):
                Data which should be checked.

            checkgroup_name (str; optional):
                default = None; blockname of 'checkgroup' which should be
                used.

        Returns:
            boolean
        """
        if not isinstance(data, Mapping):
            return False

        mandatory_field_names = cls.get_checkgroup_membernames(checkgroup_name)

        for typed_attribute_name in mandatory_field_names:
            if typed_attribute_name not in data:
                return False
        return True

    @classmethod
    def get_checkgroup_membernames(cls, checkgroup_name):
        if checkgroup_name is None:
            return cls.attribute_names
        checkgroup_member_names = []
        for typed_attribute_name, type_field in cls.field_types.items():
            if checkgroup_name not in type_field.checkgroups:
                continue
            checkgroup_member_names.append(typed_attribute_name)
        if not checkgroup_member_names:
            raise KeyError(
                "Checkgroup `{}` doesn't exist within "
                "{}".format(checkgroup_name, cls.__name__)
            )
        return checkgroup_member_names


if __name__ == '__main__':
    import doctest
    doctest.testmod()
