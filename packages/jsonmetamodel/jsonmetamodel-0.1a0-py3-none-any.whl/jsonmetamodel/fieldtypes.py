# -*- coding: utf-8 -*-
"""
.. autoclass:: jsonmetamodel.IDataType

.. autoclass:: jsonmetamodel.SqlDouble

.. autoclass:: jsonmetamodel.JsonInteger

.. autoclass:: jsonmetamodel.SqlInteger

.. autoclass:: jsonmetamodel.SqlBoolean

.. autoclass:: jsonmetamodel.JsonString

.. autoclass:: jsonmetamodel.SqlChar
"""
import logging
from typing import Any, List, Union, Callable, Optional, Tuple
import warnings
from abc import ABC, abstractmethod

logger = logging.getLogger("jsonmetamodel")


SQLCHAR_MAXIMUM_STRING_LENGTH = 255

SQL_INT_MINIMUM = -2147483648
SQL_INT_MAXIMUM = 2147483647


ValueIsValid = bool
ValidationErrorMessage = str
ValidationResult = Tuple[ValueIsValid, ValidationErrorMessage]


class ADataType(ABC):
    """"""

    def __init__(
        self,
        default: Optional[Any] = None,
        checkgroups: Optional[List[str]] = None,
        primekey: Optional[str] = None,
        allows_none=True,
        **additional_arguments
    ):
        """
        Basic field to define data types within a *jsonmetamodel.JsonModel*.

        Args:
            default:
            checkgroups(Optional[str, List[str]]):
                Declares the group name(s) this field is assigned to. Default
                is no assignment represented as an empty list.

            primekey(Optional[str]):
                The key name the field is assigned within the resulting
                dictionary. It can differ from the attributes name, which
                is the default value, if *primekey* is not assigned.

            allows_none(bool):
                States if 'None' values are allowed for this field. Default
                behaviour allows 'None' values. This is important, since if
                'None' values are forbidden, the value needs to be converted
                into the targeted data type.

            **additional_arguments
        """
        self._attribute_name = None
        self._primekey = primekey
        if checkgroups is None:
            self._checkgroups = ()
        elif isinstance(checkgroups, str):
            self._checkgroups = (checkgroups,)
        elif isinstance(checkgroups, (list, tuple)):
            self._checkgroups = checkgroups
        else:
            raise TypeError("'checkgroups' must be a list")
        self._default_value = None
        self._default_value = self(default)
        self.allows_none = allows_none
        self._additional_arguments = dict(additional_arguments)

    @property
    def primekey(self):
        if self._primekey is None:
            return self._attribute_name
        return self._primekey

    @property
    def attribute_name(self):
        return self._attribute_name

    def set_attribute_name(self, attribute_name: str):
        """
        Defines in which attribute of an `JsonModel` this object is
        declared.

        Args:
            attribute_name (str):
                blockname of attribute in a `JsonModel`

        Returns:
            bool:
                If name was set.
        """
        if self._attribute_name is None:
            self._attribute_name = attribute_name

    def grab(self, key, failedreturn=None):
        try:
            result = self._additional_arguments[key]
            return result
        except KeyError:
            return failedreturn

    def put(self, key, value):
        """
        Puts a key-value pair into the additional arguments of this field.

        Args:
            key(Hashable):

            value(Any):

        Returns:

        """
        self._additional_arguments[key] = value

    @abstractmethod
    def validate(self, value_to_validate) -> ValidationResult:
        """
        Validates the value, returning a *ValidationResult*.

        Args:
            value_to_validate(Any):
                The type which is validated within the scope of this field.

        Returns:
            ValidationResult(Tuple[bool, str]):
                Tuple of *ValueIsValid* stating if the value is within the
                bounds of this field and *ValidationErrorMessage* explaining
                the reason if its not the case.
        """
        pass

    @property
    def default(self):
        return self._default_value

    @property
    def checkgroups(self):
        """
        A list of groups this attribute is assigned to.

        Returns:
            list of str:
                Group names this attribute is assigned to.
        """
        return self._checkgroups

    @abstractmethod
    def __call__(self, incoming_data):
        """
        Converts `incoming_data` to the destined data type of this
        class.

        Args:
            incoming_data(Any):
                Data, which should be converted.

        Raises:
            ValueError:
                If `incoming_data` could not be converted into the
                destined data type of this class.

        Returns:
            Destined data type.
        """
        pass

    def to_targettype(self, value):
        """
        Does nothing, but passes the value through. This functionality is
        proposed for objects, which are no built in data types.
        """
        warnings.warn("Deprecated method; use class-call instead.", DeprecationWarning)
        return self.__call__(value)

    def encode(self, value):
        """
        Does nothing, but passes the value through. This functionality is
        proposed for objects, which are no built in data types.
        """
        warnings.warn(
            "Deprecated method; use class-call instead.", DeprecationWarning
        )
        return value


class IDataType(ADataType):
    """
    This class is deprecated and will be replaced by ADataType.

    """

    def __init__(
        self,
        default: Optional[Any] = None,
        checkgroups: Optional[List[str]] = None,
        primekey: Optional[str] = None,
        allows_none=True,
        **additional_arguments
    ):
        """
        Basic field to define data types within a *jsonmetamodel.JsonModel*.

        Args:
            default(Optional[Any]):
                The default value for this field.

            checkgroups(Optional[str, List[str]]):
                Declares the group name(s) this field is assigned to. Default
                is no assignment represented as an empty list.

            primekey(Optional[str]):
                The key name the field is assigned within the resulting
                dictionary. It can differ from the attributes name, which
                is the default value, if *primekey* is not assigned.

            allows_none(bool):
                States if 'None' values are allowed for this field. Default
                behaviour allows 'None' values. This is important, since if
                'None' values are forbidden, the value needs to be converted
                into the targeted data type.

            **additional_arguments
        """
        warnings.warn("IDataType is replaced by ADataType", DeprecationWarning)
        warnings.warn("IDataType is replaced by ADataType", FutureWarning)
        super().__init__(
            default=default,
            checkgroups=checkgroups,
            primekey=primekey,
            allows_none=allows_none,
        )


def returns_none_if_allowed(
    idatatype_call_function: Callable[[ADataType, Any], Any]
) -> Callable[[ADataType, Any], Any]:
    """
    Wrapper for functions returning 'None' values directly if the
    IDataType-Instance of the given *idatatype_call_function* allows them.
    If not a ValueError is raised.

    Raises:
        ValueError:
            Raised if 'None' values are not allowed, but received.

    Args:
        idatatype_call_function(Callable[[IDataType, Any], Any]):
            Conversion function of the parent IDataType-Instance.

    Returns:
        Callable[[IDataType, Any], Any]:
            check_if_none_is_allowed(
                this_idatatype_instance: IDataType,
                incoming_data_for_conversion
            )
    """

    def check_if_none_is_allowed(
        this_idatatype_instance: ADataType, incoming_data_for_conversion
    ):
        if incoming_data_for_conversion is None:
            if this_idatatype_instance.allows_none:
                return incoming_data_for_conversion
            raise ValueError(
                "'{}' does not allows 'None' values. You need to define an value "
                "fitting to {}.".format(
                    this_idatatype_instance.attribute_name,
                    this_idatatype_instance.__class__.__name__,
                )
            )
        return idatatype_call_function(
            this_idatatype_instance, incoming_data_for_conversion
        )

    return check_if_none_is_allowed


class JsonObject(ADataType):
    def __call__(self, incoming_data):
        return incoming_data

    def validate(self, value_to_validate) -> ValidationResult:
        raise NotImplementedError("validate is not implemented within this version.")


class AnyType(ADataType):
    """
    This should pass any data type or value through.

    Examples:

        >>> values_of_any_type = AnyType()
        >>> values_of_any_type(1)
        1
        >>> values_of_any_type("2")
        '2'
        >>> values_of_any_type(dict())
        {}
    """

    def __call__(self, incoming_data):
        return incoming_data

    def validate(self, value_to_validate) -> ValidationResult:
        return (True, "")


class SqlDouble(ADataType):
    """
    Examples:

        from jsonmetamodel import SqlDouble
        >>> a_floating_point_number = SqlDouble(default=0.0)
        >>> a_floating_point_number(1.2345)
        1.2345
        >>> a_floating_point_number("1.2345")
        1.2345
        >>> a_floating_point_number(1/100)
        0.01
    """

    def __init__(self, default: Optional[float] = 0.0, **additional_arguments):
        """

        Args:
            default(Optional[float]):
                The default value for this field.

            checkgroups(Optional[str, List[str]]):
                See ADataType

            primekey(Optional[str]):
                See ADataType

            allows_none(bool):
                See ADataType

            **additional_arguments:
        """
        try:
            if default is not None:
                default = float(default)
            else:
                default = None
        except:
            default = 0.0
        super().__init__(default, **additional_arguments)

    @returns_none_if_allowed
    def __call__(self, value):
        try:
            result = float(value)
        except Exception:
            result = self._default_value
        return result

    def validate(self, value_to_validate) -> ValidationResult:
        raise NotImplementedError("validate is not implemented within this version.")


class JsonInteger(ADataType):
    """
    Converts a `Any` to a string using the `str` method.

    Examples:

        >>> any_int = JsonInteger(default=0)
        >>> any_int("13")
        13

    Note:
        For more details search for json-schema.org.

    Args:
        default(Optional[int]):
            The default value for this field.

        checkgroups(Optional[str, List[str]]):
            See ADataType

        primekey(Optional[str]):
            See ADataType

        allows_none(bool):
            See ADataType

        multipleOf (int):
            Numbers can be restricted to a multiple of a given number, using the
                        multipleOf keyword. It may be set to any positive number.

        minimum (int):
            Validated for minimum <= x

        exclusiveMinimum (int):
            Validated for minimum < x

        maximum (int):
            Validated for x >= maximum

                exclusiveMaximum (int)
                        Validated for x > maximum

        checkgroups Optional(List[str]):
            Declares a list of group names, this field is assigned to.
            Default is no group assignment.
    """

    KEYWORDS = [
        "multipleOf",
        "minimum",
        "exclusiveMinimum",
        "maximum",
        "exclusiveMaximum",
    ]

    def __init__(self, default: int = 0, **additional_arguments):
        super().__init__(default, **additional_arguments)

    @returns_none_if_allowed
    def __call__(self, incoming_data: Union[str, int, float]) -> int:
        """
        Converts `incoming_data` into an integer. Valid data can be
        numbers represented as string, int or float.

        Args:
            incoming_data:
                Incoming data to be converted into an integer.

        Raises:
            ValueError:
                If `incoming_data` could not be converted.

        Returns:
            int
        """
        try:
            result = int(incoming_data)
            return result
        except ValueError:
            pass
        potential_float = float(incoming_data)
        return int(potential_float)

    def validate(self, value_to_validate) -> ValidationResult:
        raise NotImplementedError(
            "validate is not implemented within this version. A validation of this type"
            "needs to consider the specific KEYWORDS of the integer described by"
            "jsonschema.org"
        )


class SqlInteger(JsonInteger):
    def __init__(self, default=0, **additional_arguments):
        super().__init__(default=default, **additional_arguments)

    @returns_none_if_allowed
    def __call__(self, incoming_data) -> int:
        integer_value = super().__call__(incoming_data)
        if integer_value < SQL_INT_MINIMUM or SQL_INT_MAXIMUM < integer_value:
            raise ValueError(
                "SQL INT only allows values within the range of {} to {}. "
                "Given value was {}.".format(
                    SQL_INT_MINIMUM, SQL_INT_MAXIMUM, integer_value
                )
            )
        return integer_value


class SqlBoolean(ADataType):
    def __init__(self, default=False, allow_none=False, **additional_arguments):
        try:
            default = bool(self._decodestring(default))
        except:
            default = False
        super().__init__(default, **additional_arguments)

    @staticmethod
    def _decodestring(value):
        if isinstance(value, str):
            if value == "":
                return False
            if value == "1":
                return True
            if value.lower() in "truewahr":
                return True
            return False
        return value

    @returns_none_if_allowed
    def __call__(self, incoming_data):
        """
        Returns `false` for any number not being 1 and any string not
         being literal 'true' or 'wahr'; else returns true.

        Args:
            incoming_data:

        Raises:
            ValueError:
                If a 'conversion' didn't succeed.

        Returns:
            bool
        """
        result = bool(self._decodestring(incoming_data))
        return result

    def validate(self, value_to_validate) -> ValidationResult:
        raise NotImplementedError("validate is not implemented within this version.")


class JsonString(ADataType):
    """
    Converts a `Any` to a string using the `str` method.

    Note:
        For more details search for json-schema.org.

    Args:
        columnname (str):
            Key's name of the attribute within the source dictionary.

        default (str):
            Default value for this attribute.

        minLength (int):
            Json-schema field defining the items minimum length.

        maxLength (int):
            Json-schema field defining the items maximum length.

        pattern (str):
            Json-schema field defining a regular exression the value
            needs to match to.

        format (str):
            Json-schema field defining a specific format for this value.
    """

    KEYWORDS = ["minLength", "maxLength", "pattern", "format"]

    def __init__(
        self,
        default="",
        minLength: int = None,
        maxLength: int = None,
        pattern: str = None,
        format: str = None,
        **additional_arguments
    ):
        self._format = format
        self._pattern = pattern
        self._maxLength = maxLength
        self._minLength = minLength
        super().__init__(default, **additional_arguments)

    @returns_none_if_allowed
    def __call__(self, data):
        result = str(data)
        if self._maxLength is not None and self._maxLength < len(result):
            result = result[: self._maxLength]
        if self._minLength is not None and self._minLength > len(result):
            raise ValueError(
                "Given `data` is to short. Necessary length is "
                "{}".format(self._minLength)
            )
        return result

    def to_targettype(self, value):
        warnings.warn("Deprecated method; use class-call instead.", DeprecationWarning)
        return self(value)

    def validate(self, value_to_validate) -> ValidationResult:
        raise NotImplementedError(
            "validate is not implemented within this version. A validation of this type"
            "needs to consider the specific KEYWORDS of the string described by"
            "jsonschema.org"
        )


class SqlChar(JsonString):
    """
    Converts a `Any` to a string using the `str` method.

    Note:
        For more details search for json-schema.org.

    Args:
        columnname (str):
            Key's name of the attribute within the source dictionary.

        default (str):
            Default value for this attribute.

        minLength (int):
            Json-schema field defining the items minimum length.

        maxLength (int):
            Json-schema field defining the items maximum length. For
            SqlChar it is set to 255.

        pattern (str):
            Json-schema field defining a regular exression the value
            needs to match to.

        format (str):
            Json-schema field defining a specific format for this value.
    """

    def __init__(
        self,
        default="",
        minLength: int = None,
        pattern: str = None,
        format: str = None,
        **additional_arguments
    ):
        super().__init__(default, **additional_arguments)
        self._format = format
        self._pattern = pattern
        self._maxLength = SQLCHAR_MAXIMUM_STRING_LENGTH
        self._minLength = minLength
