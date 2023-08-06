*****************
fieldtypes module
*****************

SQL data types
==============

Source: http://pys60.garage.maemo.org/doc/s60/node100.html

See Table 5.1 for a summary of mapping between SQL and Python data types.
The col function can extract any value except LONG VARBINARY and return it
as the proper Python value. In addition, the col_raw function can extract any
column type except LONG VARCHAR and LONG VARBINARY as raw binary data and
return it as a Python string.

Inserting, updating, or searching for BINARY, VARBINARY, or LONG VARBINARY
values is not supported. BINARY and VARBINARY values can be read with col or
col_raw.

+----------------------+-------------------------+--------------+-----------+
|SQL type              |  Symbian column type    | Python type  | Supported |
|                      |  (in the DBMS C++ API)  |              |           |
+----------------------+-------------------------+--------------+-----------+
|BIT                   |  EDbColBit              | int          | yes       |
+----------------------+-------------------------+--------------+-----------+
|TINYINT               |  EDbColInt8             | int          | yes       |
+----------------------+-------------------------+--------------+-----------+
|UNSIGNED TINYINT      |  EDbColUint8            | int          | yes       |
+----------------------+-------------------------+--------------+-----------+
|SMALLINT              |  EDbColInt16            | int          | yes       |
+----------------------+-------------------------+--------------+-----------+
|UNSIGNED SMALLINT     |  EDbColUint16           | int          | yes       |
+----------------------+-------------------------+--------------+-----------+
|INTEGER               |  EDbColInt32            | int          | yes       |
+----------------------+-------------------------+--------------+-----------+
|UNSIGNED INTEGER      |  EDbColUint32           | int          | yes       |
+----------------------+-------------------------+--------------+-----------+
|UNSIGNED INTEGER      |  EDbColUint32           | int          | yes       |
+----------------------+-------------------------+--------------+-----------+
|COUNTER               |  EDbColUint32 (1)       | int          | yes       |
+----------------------+-------------------------+--------------+-----------+
|BIGINT                |  EDbColInt64            | long         | yes       |
+----------------------+-------------------------+--------------+-----------+
|REAL                  |  EDbColReal32           | float        | yes       |
+----------------------+-------------------------+--------------+-----------+
|FLOAT                 |  EDbColReal64           | float        | yes       |
+----------------------+-------------------------+--------------+-----------+
|DOUBLE                |  EDbColReal64           | float        | yes       |
+----------------------+-------------------------+--------------+-----------+
|DOUBLE PRECISION      |  EDbColReal64           | float        | yes       |
+----------------------+-------------------------+--------------+-----------+
|DATE                  |  EDbColDateTime         | float (2)    | yes       |
+----------------------+-------------------------+--------------+-----------+
|TIME                  |  EDbColDateTime         | float (2)    | yes       |
+----------------------+-------------------------+--------------+-----------+
|TIMESTAMP             |  EDbColDateTime         | float (2)    | yes       |
+----------------------+-------------------------+--------------+-----------+
|CHAR(n)               |  EDbColText             | Unicode      | yes       |
+----------------------+-------------------------+--------------+-----------+
|VARCHAR(n)            |  EDbColText             | Unicode      | yes       |
+----------------------+-------------------------+--------------+-----------+
|LONG VARCHAR          |  EDbColLongText         | Unicode      | yes       |
+----------------------+-------------------------+--------------+-----------+
|BINARY(n)             |  EDbColBinary           | str          | read only |
+----------------------+-------------------------+--------------+-----------+
|VARBINARY(n)          |  EDbColBinary           | str          | read only |
+----------------------+-------------------------+--------------+-----------+
|LONG VARBINARY        |  EDbColLongBinary       | n/a          | no        |
+----------------------+-------------------------+--------------+-----------+

(1) with the TDbCol::EAutoIncrement attribute
(2) or long, with col_rawtime


MySql data types
================

Text types
----------

:CHAR(size):        Holds a fixed length string (can contain letters,
                    numbers, and special characters). The fixed size is
                    specified in parenthesis. Can store up to 255 characters
:VARCHAR(size):     Holds a variable length string (can contain letters,
                    numbers, and special characters). The maximum size is
                    specified in parenthesis. Can store up to 255 characters.
                    Note: If you put a greater value than 255 it will be
                    converted to a TEXT type
:TINYTEXT:          Holds a string with a maximum length of 255 characters
:TEXT:              Holds a string with a maximum length of 65,535 characters
:BLOB:              For BLOBs (Binary Large OBjects). Holds up to 65,535 bytes
                    of data
:MEDIUMTEXT:        Holds a string with a max. length of 16,777,215 characters
:MEDIUMBLOB:        For BLOBs (Binary Large OBjects). Holds up to
                    16,777,215 bytes of data
:LONGTEXT:          Holds a string with a maximum length of
                    4,294,967,295 characters
:LONGBLOB:          For BLOBs (Binary Large OBjects). Holds up to
                    4,294,967,295 bytes of data
:ENUM(x,y,z,etc.):  Let you enter a list of possible values. You can list up to
                    65535 values in an ENUM list. If a value is inserted that is
                    not in the list, a default value will be inserted.

                    Note:
                        The values are sorted in the order you enter them.
                        You enter the possible values in this format: ENUM('X','Y','Z')

                        SET:
                            Similar to ENUM except that SET may contain up to 64 list
                            items and can store more than one choice

Number types
------------

:TINYINT(size): 	 -128 to 127 normal. 0 to 255 UNSIGNED*. The maximum number of
                  digits may be specified in parenthesis
:SMALLINT(size): 	 -32768 to 32767 normal. 0 to 65535 UNSIGNED*. The maximum
                  number of digits may be specified in parenthesis
:MEDIUMINT(size): -8388608 to 8388607 normal. 0 to 16777215 UNSIGNED*.
                  The maximum number of digits may be specified in parenthesis
:INT(size): 	 -2147483648 to 2147483647 normal. 0 to 4294967295 UNSIGNED*.
                  The maximum number of digits may be specified in parenthesis
:BIGINT(size): 	 -9223372036854775808 to 9223372036854775807 normal. 0 to
                  18446744073709551615 UNSIGNED*. The maximum number of digits
                  may be specified in parenthesis
:FLOAT(size,d): 	 A small number with a floating decimal point. The maximum
                  number of digits may be specified in the size parameter.
                  The maximum number of digits to the right of the decimal
                  point is specified in the d parameter
:DOUBLE(size,d): 	 A large number with a floating decimal point. The maximum
                  number of digits may be specified in the size parameter.
                  The maximum number of digits to the right of the decimal
                  point is specified in the d parameter
:DECIMAL(size,d): A DOUBLE stored as a string , allowing for a fixed decimal
                  point. The maximum number of digits may be specified in the
                  size parameter. The maximum number of digits to the right of
                  the decimal point is specified in the d parameter