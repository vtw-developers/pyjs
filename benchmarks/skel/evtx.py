# SPDX-FileCopyrightText: Willi Ballenthin
# SPDX-License-Identifier: Apache-2.0

### SKEL HEAD BEGIN
def user_get_type(obj):
    if hasattr(obj, '_class_name'):
        return "<function " + obj._class_name.split(";")[0] + " >"
    else:
        return type(obj)


def user_check_type(obj, _type):
    if str(_type).startswith("<class") and str(_type).split("'")[1] in ["dict", "object"]:
        return isinstance(obj, _type)
    elif hasattr(obj, '_class_name'):
        if "function" in str(_type):
            for i in obj._class_name.split(";"):
                if i == str(_type).split(" ")[1]:
                    return True
            return False
    else:
        if str(_type).startswith("<function"):
            typename = str(_type).split(" ")[1]
            if typename == 'func_dict':
                return isinstance(obj, dict)
        return isinstance(obj, _type)


def SkelClass(class_name, super_class=None):
    if super_class is None:
        class myclass:
            _class_name = class_name
    else:
        class myclass(super_class):
            _class_name = class_name
    return myclass()

### SKEL HEAD END

import base64
import binascii
import datetime
import mmap
import re
import os
import os.path
import struct
import xml.sax.saxutils
from functools import partial, wraps

NAME_PATTERN = re.compile(r"[a-zA-Z_][a-zA-Z_\-]*")


class SYSTEM_TOKENS:
    EndOfStreamToken = 0x00
    OpenStartElementToken = 0x01
    CloseStartElementToken = 0x02
    CloseEmptyElementToken = 0x03
    CloseElementToken = 0x04
    ValueToken = 0x05
    AttributeToken = 0x06
    CDataSectionToken = 0x07
    EntityReferenceToken = 0x08
    ProcessingInstructionTargetToken = 0x0A
    ProcessingInstructionDataToken = 0x0B
    TemplateInstanceToken = 0x0C
    NormalSubstitutionToken = 0x0D
    ConditionalSubstitutionToken = 0x0E
    StartOfStreamToken = 0x0F

class NODE_TYPES:
    NULL = 0x00
    WSTRING = 0x01
    STRING = 0x02
    SIGNED_BYTE = 0x03
    UNSIGNED_BYTE = 0x04
    SIGNED_WORD = 0x05
    UNSIGNED_WORD = 0x06
    SIGNED_DWORD = 0x07
    UNSIGNED_DWORD = 0x08
    SIGNED_QWORD = 0x09
    UNSIGNED_QWORD = 0x0A
    FLOAT = 0x0B
    DOUBLE = 0x0C
    BOOLEAN = 0x0D
    BINARY = 0x0E
    GUID = 0x0F
    SIZE = 0x10
    FILETIME = 0x11
    SYSTEMTIME = 0x12
    SID = 0x13
    HEX32 = 0x14
    HEX64 = 0x15
    BXML = 0x21
    WSTRINGARRAY = 0x81

def memoize(param_0, decorated_object = None):
    """cache the return value of a method

    From http://code.activestate.com/recipes/577452-a-memoize-decorator-for-instance-methods/

    This class is meant to be used as a decorator of methods. The return value
    from a given method invocation will be cached on the instance whose method
    was invoked. All arguments passed to a method decorated with memoize must
    be hashable.

    If a memoized method is invoked directly on its class the result will not
    be cached. Instead the method will be invoked like a static method:
    class Obj(object):
        @memoize
        def add_to(self, arg):
            return self + arg
    Obj.add_to(1) # not enough arguments
    Obj.add_to(1, 2) # returns 3, result is not cached
    """
    def __init__(func):
        ### --- BLOCK BEGIN 1
        class_var.func = func
        ### --- BLOCK END 1
    
    
    
    def __get__(obj, objtype):
        ### --- BLOCK BEGIN 2
        if obj is None:
            return class_var.func
        return partial(class_var, obj)
        ### --- BLOCK END 2
    
    
    
    def __call__(*args):
        kw = {}
        ### --- BLOCK BEGIN 3
        obj = args[0]
        try:
            cache = obj.__cache
        except AttributeError:
            cache = obj.__cache = {}
        key = (class_var.func, args, frozenset(list(kw.items())))
        if key not in cache:
            cache[key] = class_var.func(*args)
        return cache[key]
        ### --- BLOCK END 3
    
    
    
    class_var = SkelClass('memoize')

    tmp_f = param_0
    def self_func(*args):
        return tmp_f(*args[1:])
    param_0 = self_func

    class_var.__init__ = __init__
    class_var.__get__ = __get__
    class_var.__call__ = __call__
    __init__(param_0)

    def self_call(*args):
        return __call__(decorated_object, *args)

    return self_call


def align(offset, alignment):
    """
    Return the offset aligned to the nearest greater given alignment
    Arguments:
    - `offset`: An integer
    - `alignment`: An integer
    """
    ### --- BLOCK BEGIN 4
    if offset % alignment == 0:
        return offset
    return offset + (alignment - (offset % alignment))
    ### --- BLOCK END 4



def dosdate(dosdate, dostime):
    """
    `dosdate`: 2 bytes, little endian.
    `dostime`: 2 bytes, little endian.
    returns: datetime.datetime or datetime.datetime.min on error
    """
    ### --- BLOCK BEGIN 5
    try:
        t = ord(dosdate[1]) << 8
        t |= ord(dosdate[0])
        day = t & 0b0000000000011111
        month = (t & 0b0000000111100000) >> 5
        year = (t & 0b1111111000000000) >> 9
        year += 1980
        t = ord(dostime[1]) << 8
        t |= ord(dostime[0])
        sec = t & 0b0000000000011111
        sec *= 2
        minute = (t & 0b0000011111100000) >> 5
        hour = (t & 0b1111100000000000) >> 11
        return datetime.datetime(year, month, day, hour, minute, sec)
    except ValueError:
        return datetime.datetime.min
    ### --- BLOCK END 5



def parse_filetime(qword):
    ### --- BLOCK BEGIN 6
    if qword == 0:
        return datetime.datetime.min
    try:
        return datetime.datetime.fromtimestamp(float(qword) * 1e-7 - 11644473600, datetime.timezone.utc)
    except (ValueError, OSError):
        return datetime.datetime.min
    ### --- BLOCK END 6



def BinaryParserException(param_0):
    """
    Base Exception class for binary parsing.
    """
    def __init__(value):
        """
            Constructor.
            Arguments:
            - `value`: A string description.
            """
        ### --- BLOCK BEGIN 7
        
        class_var._value = value
        ### --- BLOCK END 7
    
    
    
    def __repr__():
        ### --- BLOCK BEGIN 8
        return "BinaryParserException({!r})".format(class_var._value)
        ### --- BLOCK END 8
    
    
    
    def __str__():
        ### --- BLOCK BEGIN 9
        return "Binary Parser Exception: {}".format(class_var._value)
        ### --- BLOCK END 9
    
    
    
    class_var = Exception()
    class_var._class_name = 'BinaryParserException;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.__repr__ = __repr__
    class_var.__str__ = __str__
    __init__(param_0)
    return class_var


def ParseException(param_0):
    """
    An exception to be thrown during binary parsing, such as
    when an invalid header is encountered.
    """
    def __init__(value):
        """
            Constructor.
            Arguments:
            - `value`: A string description.
            """
        ### --- BLOCK BEGIN 10
        
        pass
        ### --- BLOCK END 10
    
    
    
    def __repr__():
        ### --- BLOCK BEGIN 11
        return "ParseException({!r})".format(class_var._value)
        ### --- BLOCK END 11
    
    
    
    def __str__():
        ### --- BLOCK BEGIN 12
        return "Parse Exception({})".format(class_var._value)
        ### --- BLOCK END 12
    
    
    
    class_var = BinaryParserException(param_0)
    class_var._class_name = 'ParseException;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.__repr__ = __repr__
    class_var.__str__ = __str__
    __init__(param_0)
    return class_var


def OverrunBufferException(param_0, param_1):
    def __init__(readOffs, bufLen):
        ### --- BLOCK BEGIN 13
        tvalue = "read: {}, buffer length: {}".format(hex(readOffs), hex(bufLen))
        
        ### --- BLOCK END 13
    
    
    
    def __repr__():
        ### --- BLOCK BEGIN 14
        return "OverrunBufferException({!r})".format(class_var._value)
        ### --- BLOCK END 14
    
    
    
    def __str__():
        ### --- BLOCK BEGIN 15
        return "Tried to parse beyond the end of the file ({})".format(class_var._value)
        ### --- BLOCK END 15
    
    
    
    class_var = ParseException('Error: Type not support')
    class_var._class_name = 'OverrunBufferException;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.__repr__ = __repr__
    class_var.__str__ = __str__
    __init__(param_0, param_1)
    return class_var


def Block(param_0, param_1):
    """
    Base class for structure blocks in binary parsing.
    A block is associated with a offset into a byte-string.
    """
    def __init__(buf, offset):
        """
            Constructor.
            Arguments:
            - `buf`: Byte string containing stuff to parse.
            - `offset`: The offset into the buffer at which the block starts.
            """
        ### --- BLOCK BEGIN 16
        class_var._buf = buf
        class_var._offset = offset
        class_var._implicit_offset = 0
        ### --- BLOCK END 16
    
    
    
    def __repr__():
        ### --- BLOCK BEGIN 17
        return "Block(buf={!r}, offset={!r})".format(class_var._buf, class_var._offset)
        ### --- BLOCK END 17
    
    
    
    def __str__():
        ### --- BLOCK BEGIN 18
        return str(class_var)
        ### --- BLOCK END 18
    
    
    
    def declare_field(type, name, offset=None, length=None):
        def no_length_handler():
            ### --- BLOCK BEGIN 19
            f = getattr(class_var, "unpack_" + type)
            return f(offset)
            ### --- BLOCK END 19
        
        
        
        def explicit_length_handler():
            ### --- BLOCK BEGIN 20
            f = getattr(class_var, "unpack_" + type)
            return f(offset, length)
            ### --- BLOCK END 20
        
        
        
        """
            Declaratively add fields to this block.
            This method will dynamically add corresponding
              offset and unpacker methods to this block.
            Arguments:
            - `type`: A string. Should be one of the unpack_* types.
            - `name`: A string.
            - `offset`: A number.
            - `length`: (Optional) A number. For (w)strings, length in chars.
            """
        ### --- BLOCK BEGIN 21
        if offset is None:
            offset = class_var._implicit_offset
        if length is None:
            setattr(class_var, name, no_length_handler)
        else:
            setattr(class_var, name, explicit_length_handler)
        setattr(class_var, "_off_" + name, offset)
        if type == "byte":
            class_var._implicit_offset = offset + 1
        elif type == "int8":
            class_var._implicit_offset = offset + 1
        elif type == "word":
            class_var._implicit_offset = offset + 2
        elif type == "word_be":
            class_var._implicit_offset = offset + 2
        elif type == "int16":
            class_var._implicit_offset = offset + 2
        elif type == "dword":
            class_var._implicit_offset = offset + 4
        elif type == "dword_be":
            class_var._implicit_offset = offset + 4
        elif type == "int32":
            class_var._implicit_offset = offset + 4
        elif type == "qword":
            class_var._implicit_offset = offset + 8
        elif type == "int64":
            class_var._implicit_offset = offset + 8
        elif type == "float":
            class_var._implicit_offset = offset + 4
        elif type == "double":
            class_var._implicit_offset = offset + 8
        elif type == "dosdate":
            class_var._implicit_offset = offset + 4
        elif type == "filetime":
            class_var._implicit_offset = offset + 8
        elif type == "systemtime":
            class_var._implicit_offset = offset + 8
        elif type == "guid":
            class_var._implicit_offset = offset + 16
        elif type == "binary":
            class_var._implicit_offset = offset + length
        elif type == "string" and length is not None:
            class_var._implicit_offset = offset + length
        elif type == "wstring" and length is not None:
            class_var._implicit_offset = offset + (2 * length)
        elif "string" in type and length is None:
            raise ParseException("Implicit offset not supported " "for dynamic length strings")
        else:
            raise ParseException("Implicit offset not supported " "for type: {}".format(type))
        ### --- BLOCK END 21
    
    
    
    def current_field_offset():
        ### --- BLOCK BEGIN 22
        return class_var._implicit_offset
        ### --- BLOCK END 22
    
    
    
    def unpack_byte(offset):
        """
            Returns a little-endian unsigned byte from the relative offset.
            Arguments:
            - `offset`: The relative offset from the start of the block.
            Throws:
            - `OverrunBufferException`
            """
        ### --- BLOCK BEGIN 23
        o = class_var._offset + offset
        try:
            return struct.unpack_from("<B", class_var._buf, o)[0]
        except struct.error:
            raise OverrunBufferException(o, len(class_var._buf))
        ### --- BLOCK END 23
    
    
    
    def unpack_int8(offset):
        """
            Returns a little-endian signed byte from the relative offset.
            Arguments:
            - `offset`: The relative offset from the start of the block.
            Throws:
            - `OverrunBufferException`
            """
        ### --- BLOCK BEGIN 24
        o = class_var._offset + offset
        try:
            return struct.unpack_from("<b", class_var._buf, o)[0]
        except struct.error:
            raise OverrunBufferException(o, len(class_var._buf))
        ### --- BLOCK END 24
    
    
    
    def unpack_word(offset):
        """
            Returns a little-endian unsigned WORD (2 bytes) from the
              relative offset.
            Arguments:
            - `offset`: The relative offset from the start of the block.
            Throws:
            - `OverrunBufferException`
            """
        ### --- BLOCK BEGIN 25
        o = class_var._offset + offset
        try:
            return struct.unpack_from("<H", class_var._buf, o)[0]
        except struct.error:
            raise OverrunBufferException(o, len(class_var._buf))
        ### --- BLOCK END 25
    
    
    
    def unpack_word_be(offset):
        """
            Returns a big-endian unsigned WORD (2 bytes) from the
              relative offset.
            Arguments:
            - `offset`: The relative offset from the start of the block.
            Throws:
            - `OverrunBufferException`
            """
        ### --- BLOCK BEGIN 26
        o = class_var._offset + offset
        try:
            return struct.unpack_from(">H", class_var._buf, o)[0]
        except struct.error:
            raise OverrunBufferException(o, len(class_var._buf))
        ### --- BLOCK END 26
    
    
    
    def unpack_int16(offset):
        """
            Returns a little-endian signed WORD (2 bytes) from the
              relative offset.
            Arguments:
            - `offset`: The relative offset from the start of the block.
            Throws:
            - `OverrunBufferException`
            """
        ### --- BLOCK BEGIN 27
        o = class_var._offset + offset
        try:
            return struct.unpack_from("<h", class_var._buf, o)[0]
        except struct.error:
            raise OverrunBufferException(o, len(class_var._buf))
        ### --- BLOCK END 27
    
    
    
    def pack_word(offset, word):
        """
            Applies the little-endian WORD (2 bytes) to the relative offset.
            Arguments:
            - `offset`: The relative offset from the start of the block.
            - `word`: The data to apply.
            """
        ### --- BLOCK BEGIN 28
        o = class_var._offset + offset
        return struct.pack_into("<H", class_var._buf, o, word)
        ### --- BLOCK END 28
    
    
    
    def unpack_dword(offset):
        """
            Returns a little-endian DWORD (4 bytes) from the relative offset.
            Arguments:
            - `offset`: The relative offset from the start of the block.
            Throws:
            - `OverrunBufferException`
            """
        ### --- BLOCK BEGIN 29
        o = class_var._offset + offset
        try:
            return struct.unpack_from("<I", class_var._buf, o)[0]
        except struct.error:
            raise OverrunBufferException(o, len(class_var._buf))
        ### --- BLOCK END 29
    
    
    
    def unpack_dword_be(offset):
        """
            Returns a big-endian DWORD (4 bytes) from the relative offset.
            Arguments:
            - `offset`: The relative offset from the start of the block.
            Throws:
            - `OverrunBufferException`
            """
        ### --- BLOCK BEGIN 30
        o = class_var._offset + offset
        try:
            return struct.unpack_from(">I", class_var._buf, o)[0]
        except struct.error:
            raise OverrunBufferException(o, len(class_var._buf))
        ### --- BLOCK END 30
    
    
    
    def unpack_int32(offset):
        """
            Returns a little-endian signed integer (4 bytes) from the
              relative offset.
            Arguments:
            - `offset`: The relative offset from the start of the block.
            Throws:
            - `OverrunBufferException`
            """
        ### --- BLOCK BEGIN 31
        o = class_var._offset + offset
        try:
            return struct.unpack_from("<i", class_var._buf, o)[0]
        except struct.error:
            raise OverrunBufferException(o, len(class_var._buf))
        ### --- BLOCK END 31
    
    
    
    def unpack_qword(offset):
        """
            Returns a little-endian QWORD (8 bytes) from the relative offset.
            Arguments:
            - `offset`: The relative offset from the start of the block.
            Throws:
            - `OverrunBufferException`
            """
        ### --- BLOCK BEGIN 32
        o = class_var._offset + offset
        try:
            return struct.unpack_from("<Q", class_var._buf, o)[0]
        except struct.error:
            raise OverrunBufferException(o, len(class_var._buf))
        ### --- BLOCK END 32
    
    
    
    def unpack_int64(offset):
        """
            Returns a little-endian signed 64-bit integer (8 bytes) from
              the relative offset.
            Arguments:
            - `offset`: The relative offset from the start of the block.
            Throws:
            - `OverrunBufferException`
            """
        ### --- BLOCK BEGIN 33
        o = class_var._offset + offset
        try:
            return struct.unpack_from("<q", class_var._buf, o)[0]
        except struct.error:
            raise OverrunBufferException(o, len(class_var._buf))
        ### --- BLOCK END 33
    
    
    
    def unpack_float(offset):
        """
            Returns a single-precision float (4 bytes) from
              the relative offset.  IEEE 754 format.
            Arguments:
            - `offset`: The relative offset from the start of the block.
            Throws:
            - `OverrunBufferException`
            """
        ### --- BLOCK BEGIN 34
        o = class_var._offset + offset
        try:
            return struct.unpack_from("<f", class_var._buf, o)[0]
        except struct.error:
            raise OverrunBufferException(o, len(class_var._buf))
        ### --- BLOCK END 34
    
    
    
    def unpack_double(offset):
        """
            Returns a double-precision float (8 bytes) from
              the relative offset.  IEEE 754 format.
            Arguments:
            - `offset`: The relative offset from the start of the block.
            Throws:
            - `OverrunBufferException`
            """
        ### --- BLOCK BEGIN 35
        o = class_var._offset + offset
        try:
            return struct.unpack_from("<d", class_var._buf, o)[0]
        except struct.error:
            raise OverrunBufferException(o, len(class_var._buf))
        ### --- BLOCK END 35
    
    
    
    def unpack_binary(offset, length):
        """
            Returns raw binary data from the relative offset with the given length.
            Arguments:
            - `offset`: The relative offset from the start of the block.
            - `length`: The length of the binary blob. If zero, the empty string
                zero length is returned.
            Throws:
            - `OverrunBufferException`
            """
        ### --- BLOCK BEGIN 36
        if not length:
            return ("".encode("ascii"))
        o = class_var._offset + offset
        try:
            return (struct.unpack_from("<{}s".format(length), class_var._buf, o)[0])
        except struct.error:
            raise OverrunBufferException(o, len(class_var._buf))
        ### --- BLOCK END 36
    
    
    
    def unpack_string(offset, length):
        """
            Returns a string from the relative offset with the given length.
            Arguments:
            - `offset`: The relative offset from the start of the block.
            - `length`: The length of the string.
            Throws:
            - `OverrunBufferException`
            """
        ### --- BLOCK BEGIN 37
        return class_var.unpack_binary(offset, length).decode("ascii")
        ### --- BLOCK END 37
    
    
    
    def unpack_wstring(offset, length):
        """
            Returns a string from the relative offset with the given length,
            where each character is a wchar (2 bytes)
            Arguments:
            - `offset`: The relative offset from the start of the block.
            - `length`: The length of the string.
            Throws:
            - `UnicodeDecodeError`
            """
        ### --- BLOCK BEGIN 38
        start = class_var._offset + offset
        end = class_var._offset + offset + 2 * length
        try:
            return bytes(class_var._buf[start:end]).decode("utf16")
        except AttributeError:  # already a 'str' ?
            return bytes(class_var._buf[start:end]).decode("utf16")
        ### --- BLOCK END 38
    
    
    
    def unpack_dosdate(offset):
        """
            Returns a datetime from the DOSDATE and DOSTIME starting at
            the relative offset.
            Arguments:
            - `offset`: The relative offset from the start of the block.
            Throws:
            - `OverrunBufferException`
            """
        ### --- BLOCK BEGIN 39
        try:
            o = class_var._offset + offset
            return dosdate(class_var._buf[o : o + 2], class_var._buf[o + 2 : o + 4])
        except struct.error:
            raise OverrunBufferException(o, len(class_var._buf))
        ### --- BLOCK END 39
    
    
    
    def unpack_filetime(offset):
        """
            Returns a datetime from the QWORD Windows timestamp starting at
            the relative offset.
            Arguments:
            - `offset`: The relative offset from the start of the block.
            Throws:
            - `OverrunBufferException`
            """
        ### --- BLOCK BEGIN 40
        return parse_filetime(class_var.unpack_qword(offset))
        ### --- BLOCK END 40
    
    
    
    def unpack_systemtime(offset):
        """
            Returns a datetime from the QWORD Windows SYSTEMTIME timestamp
              starting at the relative offset.
            Arguments:
            - `offset`: The relative offset from the start of the block.
            Throws:
            - `OverrunBufferException`
            """
        ### --- BLOCK BEGIN 41
        o = class_var._offset + offset
        try:
            parts = struct.unpack_from("<HHHHHHHH", class_var._buf, o)
        except struct.error:
            raise OverrunBufferException(o, len(class_var._buf))
        return datetime.datetime(
        parts[0], parts[1], parts[3], parts[4], parts[5], parts[6], parts[7]  # skip part 2 (day of week)
        )
        ### --- BLOCK END 41
    
    
    
    def unpack_guid(offset):
        """
            Returns a string containing a GUID starting at the relative offset.
            Arguments:
            - `offset`: The relative offset from the start of the block.
            Throws:
            - `OverrunBufferException`
            """
        ### --- BLOCK BEGIN 42
        o = class_var._offset + offset
        try:
            _bin = bytes(class_var._buf[o : o + 16])
        except IndexError:
            raise OverrunBufferException(o, len(class_var._buf))
        # Yeah, this is ugly
        h = [_bin[i] for i in range(len(_bin))]
        return """{:02x}{:02x}{:02x}{:02x}-{:02x}{:02x}-{:02x}{:02x}-{:02x}{:02x}-{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}""".format(
        h[3], h[2], h[1], h[0], h[5], h[4], h[7], h[6], h[8], h[9], h[10], h[11], h[12], h[13], h[14], h[15]
        )
        ### --- BLOCK END 42
    
    
    
    def absolute_offset(offset):
        """
            Get the absolute offset from an offset relative to this block
            Arguments:
            - `offset`: The relative offset into this block.
            """
        ### --- BLOCK BEGIN 43
        return class_var._offset + offset
        ### --- BLOCK END 43
    
    
    
    def offset():
        """
            Equivalent to self.absolute_offset(0x0), which is the starting
              offset of this block.
            """
        ### --- BLOCK BEGIN 44
        return class_var._offset
        ### --- BLOCK END 44
    
    
    
    class_var = SkelClass('Block')
    class_var.__init__ = __init__
    class_var.__repr__ = __repr__
    class_var.__str__ = __str__
    class_var.declare_field = declare_field
    class_var.current_field_offset = current_field_offset
    class_var.unpack_byte = unpack_byte
    class_var.unpack_int8 = unpack_int8
    class_var.unpack_word = unpack_word
    class_var.unpack_word_be = unpack_word_be
    class_var.unpack_int16 = unpack_int16
    class_var.pack_word = pack_word
    class_var.unpack_dword = unpack_dword
    class_var.unpack_dword_be = unpack_dword_be
    class_var.unpack_int32 = unpack_int32
    class_var.unpack_qword = unpack_qword
    class_var.unpack_int64 = unpack_int64
    class_var.unpack_float = unpack_float
    class_var.unpack_double = unpack_double
    class_var.unpack_binary = unpack_binary
    class_var.unpack_string = unpack_string
    class_var.unpack_wstring = unpack_wstring
    class_var.unpack_dosdate = unpack_dosdate
    class_var.unpack_filetime = unpack_filetime
    class_var.unpack_systemtime = unpack_systemtime
    class_var.unpack_guid = unpack_guid
    class_var.absolute_offset = absolute_offset
    class_var.offset = offset
    __init__(param_0, param_1)
    return class_var


def SuppressConditionalSubstitution(param_0):
    """
    This exception is to be thrown to indicate that a conditional
      substitution evaluated to NULL, and the parent element should
      be suppressed. This exception should be caught at the first
      opportunity, and must not propagate far up the call chain.

    Strategy:
      AttributeNode catches this, .xml() --> ""
      StartOpenElementNode catches this for each child, ensures
        there's at least one useful value.  Or, .xml() --> ""
    """
    def __init__(msg):
        ### --- BLOCK BEGIN 45
        
        pass
        ### --- BLOCK END 45
    
    
    
    class_var = Exception(param_0)
    class_var._class_name = 'SuppressConditionalSubstitution;' + class_var._class_name
    class_var.__init__ = __init__
    __init__(param_0)
    return class_var


def UnexpectedStateException(param_0):
    """
    UnexpectedStateException is an exception to be thrown when the parser
      encounters an unexpected value or state. This probably means there
      is a bug in the parser, but could stem from a corrupted input file.
    """
    def __init__(msg):
        ### --- BLOCK BEGIN 46
        
        pass
        ### --- BLOCK END 46
    
    
    
    class_var = ParseException(param_0)
    class_var._class_name = 'UnexpectedStateException;' + class_var._class_name
    class_var.__init__ = __init__
    __init__(param_0)
    return class_var


def BXmlNode(param_0, param_1, param_2, param_3):
    def __init__(buf, offset, chunk, parent):
        ### --- BLOCK BEGIN 47
        
        class_var._chunk = chunk
        class_var._parent = parent
        ### --- BLOCK END 47
    
    
    
    def __repr__():
        ### --- BLOCK BEGIN 48
        return "BXmlNode(buf={!r}, offset={!r}, chunk={!r}, parent={!r})".format(
        class_var._buf, class_var.offset(), class_var._chunk, class_var._parent
        )
        ### --- BLOCK END 48
    
    
    
    def __str__():
        ### --- BLOCK BEGIN 49
        return "BXmlNode(offset={})".format(hex(class_var.offset()))
        ### --- BLOCK END 49
    
    
    
    def dump():
        ### --- BLOCK BEGIN 50
        b = class_var._buf[class_var.offset() : class_var.offset() + class_var.length()]
        return hexdump.hexdump(b, result="return")
        ### --- BLOCK END 50
    
    
    
    def tag_length():
        """
            This method must be implemented and overridden for all BXmlNodes.
            @return An integer specifying the length of this tag, not including
              its children.
            """
        ### --- BLOCK BEGIN 51
        raise NotImplementedError("tag_length not implemented for {!r}").format(class_var)
        ### --- BLOCK END 51
    
    
    
    def _children(max_children, end_tokens):
        """
            @return A list containing all of the children BXmlNodes.
            """
        ### --- BLOCK BEGIN 52
        ret = []
        ofs = class_var.tag_length()
        if max_children:
            gen = list(range(max_children))
        else:
            gen = user_infinite_counter()
        for _ in gen:
        # we lose error checking by masking off the higher nibble,
        #   but, some tokens like 0x01, make use of the flags nibble.
            token = class_var.unpack_byte(ofs) & 0x0F
            try:
                HandlerNodeClass = node_dispatch_table[token]
                child = HandlerNodeClass(class_var._buf, class_var.offset() + ofs, class_var._chunk, class_var)
            except IndexError:
                raise ParseException("Unexpected token {:02X} at {}".format(token, class_var.absolute_offset(0x0) + ofs))
            ret.append(child)
            ofs += child.length()
            if token in end_tokens:
                break
            if child.find_end_of_stream():
                break
        return ret
        ### --- BLOCK END 52
    
    
    
    def children():
        ### --- BLOCK BEGIN 53
        return class_var._children(None, [0x00])
        ### --- BLOCK END 53
    
    
    
    def length():
        """
            @return An integer specifying the length of this tag and all
              its children.
            """
        ### --- BLOCK BEGIN 54
        ret = class_var.tag_length()
        for child in class_var.children():
            ret += child.length()
        return ret
        ### --- BLOCK END 54
    
    
    
    def find_end_of_stream():
        ### --- BLOCK BEGIN 55
        for child in class_var.children():
            if user_check_type(child, EndOfStreamNode):
                return child
            ret = child.find_end_of_stream()
            if ret:
                return ret
        return None
        ### --- BLOCK END 55
    
    
    
    class_var = Block(param_0, param_1)
    class_var._class_name = 'BXmlNode;' + class_var._class_name
    children = memoize(children, class_var)
    
    length = memoize(length, class_var)
    
    find_end_of_stream = memoize(find_end_of_stream, class_var)
    
    class_var.__init__ = __init__
    class_var.__repr__ = __repr__
    class_var.__str__ = __str__
    class_var.dump = dump
    class_var.tag_length = tag_length
    class_var._children = _children
    class_var.children = children
    class_var.length = length
    class_var.find_end_of_stream = find_end_of_stream
    __init__(param_0, param_1, param_2, param_3)
    return class_var


def NameStringNode(param_0, param_1, param_2, param_3):
    def __init__(buf, offset, chunk, parent):
        ### --- BLOCK BEGIN 56
        
        class_var.declare_field("dword", "next_offset", 0x0, None)
        class_var.declare_field("word", "hash", None, None)
        class_var.declare_field("word", "string_length", None, None)
        class_var.declare_field("wstring", "string", length=class_var.string_length())
        ### --- BLOCK END 56
    
    
    
    def __repr__():
        ### --- BLOCK BEGIN 57
        return "NameStringNode(buf={!r}, offset={!r}, chunk={!r})".format(class_var._buf, class_var.offset(), class_var._chunk)
        ### --- BLOCK END 57
    
    
    
    def __str__():
        ### --- BLOCK BEGIN 58
        return "NameStringNode(offset={}, length={}, end={})".format(
        hex(class_var.offset()), hex(class_var.length()), hex(class_var.offset() + class_var.length())
        )
        ### --- BLOCK END 58
    
    
    
    def string():
        ### --- BLOCK BEGIN 59
        return str(class_var._string())
        ### --- BLOCK END 59
    
    
    
    def tag_length():
        ### --- BLOCK BEGIN 60
        return (class_var.string_length() * 2) + 8
        ### --- BLOCK END 60
    
    
    
    def length():
        ### --- BLOCK BEGIN 61
        return class_var.tag_length() + 2
        ### --- BLOCK END 61
    
    
    
    class_var = BXmlNode(param_0, param_1, param_2, param_3)
    class_var._class_name = 'NameStringNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.__repr__ = __repr__
    class_var.__str__ = __str__
    class_var.string = string
    class_var.tag_length = tag_length
    class_var.length = length
    __init__(param_0, param_1, param_2, param_3)
    return class_var


def TemplateNode(param_0, param_1, param_2, param_3):
    def __init__(buf, offset, chunk, parent):
        ### --- BLOCK BEGIN 62
        
        class_var.declare_field("dword", "next_offset", 0x0, None)
        class_var.declare_field("dword", "template_id", None, None)
        class_var.declare_field("guid", "guid", 0x04, None)
        # unsure why this overlaps
        class_var.declare_field("dword", "data_length", None, None)
        ### --- BLOCK END 62
    
    
    
    def __repr__():
        ### --- BLOCK BEGIN 63
        return "TemplateNode(buf={!r}, offset={!r}, chunk={!r}, parent={!r})".format(
        class_var._buf, class_var.offset(), class_var._chunk, class_var._parent
        )
        ### --- BLOCK END 63
    
    
    
    def __str__():
        ### --- BLOCK BEGIN 64
        return "TemplateNode(offset={}, guid={}, length={})".format(hex(class_var.offset()), class_var.guid(), hex(class_var.length()))
        ### --- BLOCK END 64
    
    
    
    def tag_length():
        ### --- BLOCK BEGIN 65
        return 0x18
        ### --- BLOCK END 65
    
    
    
    def length():
        ### --- BLOCK BEGIN 66
        return class_var.tag_length() + class_var.data_length()
        ### --- BLOCK END 66
    
    
    
    class_var = BXmlNode(param_0, param_1, param_2, param_3)
    class_var._class_name = 'TemplateNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.__repr__ = __repr__
    class_var.__str__ = __str__
    class_var.tag_length = tag_length
    class_var.length = length
    __init__(param_0, param_1, param_2, param_3)
    return class_var


def EndOfStreamNode(param_0, param_1, param_2, param_3):
    """
    The binary XML node for the system token 0x00.

    This is the "end of stream" token. It may never actually
      be instantiated here.
    """
    def __init__(buf, offset, chunk, parent):
        ### --- BLOCK BEGIN 67
        
        pass
        ### --- BLOCK END 67
    
    
    
    def __repr__():
        ### --- BLOCK BEGIN 68
        return "EndOfStreamNode(buf={!r}, offset={!r}, chunk={!r}, parent={!r})".format(
        class_var._buf, class_var.offset(), class_var._chunk, class_var._parent
        )
        ### --- BLOCK END 68
    
    
    
    def __str__():
        ### --- BLOCK BEGIN 69
        return "EndOfStreamNode(offset={}, length={}, token={})".format(hex(class_var.offset()), hex(class_var.length()), 0x00)
        ### --- BLOCK END 69
    
    
    
    def flags():
        ### --- BLOCK BEGIN 70
        return class_var.token() >> 4
        ### --- BLOCK END 70
    
    
    
    def tag_length():
        ### --- BLOCK BEGIN 71
        return 1
        ### --- BLOCK END 71
    
    
    
    def length():
        ### --- BLOCK BEGIN 72
        return 1
        ### --- BLOCK END 72
    
    
    
    def children():
        ### --- BLOCK BEGIN 73
        return []
        ### --- BLOCK END 73
    
    
    
    class_var = BXmlNode(param_0, param_1, param_2, param_3)
    class_var._class_name = 'EndOfStreamNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.__repr__ = __repr__
    class_var.__str__ = __str__
    class_var.flags = flags
    class_var.tag_length = tag_length
    class_var.length = length
    class_var.children = children
    __init__(param_0, param_1, param_2, param_3)
    return class_var


def OpenStartElementNode(param_0, param_1, param_2, param_3):
    """
    The binary XML node for the system token 0x01.

    This is the "open start element" token.
    """
    def __init__(buf, offset, chunk, parent):
        ### --- BLOCK BEGIN 74
        
        class_var.declare_field("byte", "token", 0x0, None)
        class_var.declare_field("word", "unknown0", None, None)
        # TODO(wb): use this size() field.
        class_var.declare_field("dword", "size", None, None)
        class_var.declare_field("dword", "string_offset", None, None)
        class_var._tag_length = 11
        class_var._element_type = 0
        if class_var.flags() & 0x04:
            class_var._tag_length += 4
        if class_var.string_offset() > class_var.offset() - class_var._chunk._offset:
            new_string = class_var._chunk.add_string(class_var.string_offset(), parent=class_var)
            class_var._tag_length += new_string.length()
        ### --- BLOCK END 74
    
    
    
    def __repr__():
        ### --- BLOCK BEGIN 75
        return "OpenStartElementNode(buf={!r}, offset={!r}, chunk={!r})".format(class_var._buf, class_var.offset(), class_var._chunk)
        ### --- BLOCK END 75
    
    
    
    def __str__():
        ### --- BLOCK BEGIN 76
        return "OpenStartElementNode(offset={}, name={}, length={}, token={}, end={}, taglength={}, endtag={})".format(
        hex(class_var.offset()),
        class_var.tag_name(),
        hex(class_var.length()),
        hex(class_var.token()),
        hex(class_var.offset() + class_var.length()),
        hex(class_var.tag_length()),
        hex(class_var.offset() + class_var.tag_length()),
        )
        ### --- BLOCK END 76
    
    
    
    def is_empty_node():
        ### --- BLOCK BEGIN 77
        for child in class_var.children():
            if user_get_type(child) is CloseEmptyElementNode:
                return True
        return False
        ### --- BLOCK END 77
    
    
    
    def flags():
        ### --- BLOCK BEGIN 78
        return class_var.token() >> 4
        ### --- BLOCK END 78
    
    
    
    def tag_name():
        ### --- BLOCK BEGIN 79
        return class_var._chunk.strings()[class_var.string_offset()].string()
        ### --- BLOCK END 79
    
    
    
    def tag_length():
        ### --- BLOCK BEGIN 80
        return class_var._tag_length
        ### --- BLOCK END 80
    
    
    
    def verify():
        ### --- BLOCK BEGIN 81
        return class_var.flags() & 0x0B == 0 and class_var.opcode() & 0x0F == 0x01
        ### --- BLOCK END 81
    
    
    
    def children():
        ### --- BLOCK BEGIN 82
        return class_var._children(None, [SYSTEM_TOKENS.CloseElementToken, SYSTEM_TOKENS.CloseEmptyElementToken])
        ### --- BLOCK END 82
    
    
    
    class_var = BXmlNode(param_0, param_1, param_2, param_3)
    class_var._class_name = 'OpenStartElementNode;' + class_var._class_name
    is_empty_node = memoize(is_empty_node, class_var)
    
    tag_name = memoize(tag_name, class_var)
    
    children = memoize(children, class_var)
    
    class_var.__init__ = __init__
    class_var.__repr__ = __repr__
    class_var.__str__ = __str__
    class_var.is_empty_node = is_empty_node
    class_var.flags = flags
    class_var.tag_name = tag_name
    class_var.tag_length = tag_length
    class_var.verify = verify
    class_var.children = children
    __init__(param_0, param_1, param_2, param_3)
    return class_var


def CloseStartElementNode(param_0, param_1, param_2, param_3):
    """
    The binary XML node for the system token 0x02.

    This is the "close start element" token.
    """
    def __init__(buf, offset, chunk, parent):
        ### --- BLOCK BEGIN 83
        
        class_var.declare_field("byte", "token", 0x0, None)
        ### --- BLOCK END 83
    
    
    
    def __repr__():
        ### --- BLOCK BEGIN 84
        return "CloseStartElementNode(buf={!r}, offset={!r}, chunk={!r}, parent={!r})".format(
        class_var._buf, class_var.offset(), class_var._chunk, class_var._parent
        )
        ### --- BLOCK END 84
    
    
    
    def __str__():
        ### --- BLOCK BEGIN 85
        return "CloseStartElementNode(offset={}, length={}, token={})".format(
        hex(class_var.offset()), hex(class_var.length()), hex(class_var.token())
        )
        ### --- BLOCK END 85
    
    
    
    def flags():
        ### --- BLOCK BEGIN 86
        return class_var.token() >> 4
        ### --- BLOCK END 86
    
    
    
    def tag_length():
        ### --- BLOCK BEGIN 87
        return 1
        ### --- BLOCK END 87
    
    
    
    def length():
        ### --- BLOCK BEGIN 88
        return 1
        ### --- BLOCK END 88
    
    
    
    def children():
        ### --- BLOCK BEGIN 89
        return []
        ### --- BLOCK END 89
    
    
    
    def verify():
        ### --- BLOCK BEGIN 90
        return class_var.flags() & 0x0F == 0 and class_var.opcode() & 0x0F == 0x02
        ### --- BLOCK END 90
    
    
    
    class_var = BXmlNode(param_0, param_1, param_2, param_3)
    class_var._class_name = 'CloseStartElementNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.__repr__ = __repr__
    class_var.__str__ = __str__
    class_var.flags = flags
    class_var.tag_length = tag_length
    class_var.length = length
    class_var.children = children
    class_var.verify = verify
    __init__(param_0, param_1, param_2, param_3)
    return class_var


def CloseEmptyElementNode(param_0, param_1, param_2, param_3):
    """
    The binary XML node for the system token 0x03.
    """
    def __init__(buf, offset, chunk, parent):
        ### --- BLOCK BEGIN 91
        
        class_var.declare_field("byte", "token", 0x0, None)
        ### --- BLOCK END 91
    
    
    
    def __repr__():
        ### --- BLOCK BEGIN 92
        return "CloseEmptyElementNode(buf={!r}, offset={!r}, chunk={!r}, parent={!r})".format(
        class_var._buf, class_var.offset(), class_var._chunk, class_var._parent
        )
        ### --- BLOCK END 92
    
    
    
    def __str__():
        ### --- BLOCK BEGIN 93
        return "CloseEmptyElementNode(offset={}, length={}, token={})".format(
        hex(class_var.offset()), hex(class_var.length()), hex(0x03)
        )
        ### --- BLOCK END 93
    
    
    
    def flags():
        ### --- BLOCK BEGIN 94
        return class_var.token() >> 4
        ### --- BLOCK END 94
    
    
    
    def tag_length():
        ### --- BLOCK BEGIN 95
        return 1
        ### --- BLOCK END 95
    
    
    
    def length():
        ### --- BLOCK BEGIN 96
        return 1
        ### --- BLOCK END 96
    
    
    
    def children():
        ### --- BLOCK BEGIN 97
        return []
        ### --- BLOCK END 97
    
    
    
    class_var = BXmlNode(param_0, param_1, param_2, param_3)
    class_var._class_name = 'CloseEmptyElementNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.__repr__ = __repr__
    class_var.__str__ = __str__
    class_var.flags = flags
    class_var.tag_length = tag_length
    class_var.length = length
    class_var.children = children
    __init__(param_0, param_1, param_2, param_3)
    return class_var


def CloseElementNode(param_0, param_1, param_2, param_3):
    """
    The binary XML node for the system token 0x04.

    This is the "close element" token.
    """
    def __init__(buf, offset, chunk, parent):
        ### --- BLOCK BEGIN 98
        
        class_var.declare_field("byte", "token", 0x0, None)
        ### --- BLOCK END 98
    
    
    
    def __repr__():
        ### --- BLOCK BEGIN 99
        return "CloseElementNode(buf={!r}, offset={!r}, chunk={!r}, parent={!r})".format(
        class_var._buf, class_var.offset(), class_var._chunk, class_var._parent
        )
        ### --- BLOCK END 99
    
    
    
    def __str__():
        ### --- BLOCK BEGIN 100
        return "CloseElementNode(offset={}, length={}, token={})".format(
        hex(class_var.offset()), hex(class_var.length()), hex(class_var.token())
        )
        ### --- BLOCK END 100
    
    
    
    def flags():
        ### --- BLOCK BEGIN 101
        return class_var.token() >> 4
        ### --- BLOCK END 101
    
    
    
    def tag_length():
        ### --- BLOCK BEGIN 102
        return 1
        ### --- BLOCK END 102
    
    
    
    def length():
        ### --- BLOCK BEGIN 103
        return 1
        ### --- BLOCK END 103
    
    
    
    def children():
        ### --- BLOCK BEGIN 104
        return []
        ### --- BLOCK END 104
    
    
    
    def verify():
        ### --- BLOCK BEGIN 105
        return class_var.flags() & 0x0F == 0 and class_var.opcode() & 0x0F == 0x04
        ### --- BLOCK END 105
    
    
    
    class_var = BXmlNode(param_0, param_1, param_2, param_3)
    class_var._class_name = 'CloseElementNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.__repr__ = __repr__
    class_var.__str__ = __str__
    class_var.flags = flags
    class_var.tag_length = tag_length
    class_var.length = length
    class_var.children = children
    class_var.verify = verify
    __init__(param_0, param_1, param_2, param_3)
    return class_var


def get_variant_value(buf, offset, chunk, parent, type_, length=None):
    """
    @return A VariantType subclass instance found in the given
      buffer and offset.
    """
    ### --- BLOCK BEGIN 106
    types = {
    NODE_TYPES.NULL: NullTypeNode,
    NODE_TYPES.WSTRING: WstringTypeNode,
    NODE_TYPES.STRING: StringTypeNode,
    NODE_TYPES.SIGNED_BYTE: SignedByteTypeNode,
    NODE_TYPES.UNSIGNED_BYTE: UnsignedByteTypeNode,
    NODE_TYPES.SIGNED_WORD: SignedWordTypeNode,
    NODE_TYPES.UNSIGNED_WORD: UnsignedWordTypeNode,
    NODE_TYPES.SIGNED_DWORD: SignedDwordTypeNode,
    NODE_TYPES.UNSIGNED_DWORD: UnsignedDwordTypeNode,
    NODE_TYPES.SIGNED_QWORD: SignedQwordTypeNode,
    NODE_TYPES.UNSIGNED_QWORD: UnsignedQwordTypeNode,
    NODE_TYPES.FLOAT: FloatTypeNode,
    NODE_TYPES.DOUBLE: DoubleTypeNode,
    NODE_TYPES.BOOLEAN: BooleanTypeNode,
    NODE_TYPES.BINARY: BinaryTypeNode,
    NODE_TYPES.GUID: GuidTypeNode,
    NODE_TYPES.SIZE: SizeTypeNode,
    NODE_TYPES.FILETIME: FiletimeTypeNode,
    NODE_TYPES.SYSTEMTIME: SystemtimeTypeNode,
    NODE_TYPES.SID: SIDTypeNode,
    NODE_TYPES.HEX32: Hex32TypeNode,
    NODE_TYPES.HEX64: Hex64TypeNode,
    NODE_TYPES.BXML: BXmlTypeNode,
    NODE_TYPES.WSTRINGARRAY: WstringArrayTypeNode,
    }
    try:
        TypeClass = types[type_]
    except IndexError:
        raise NotImplementedError("Type {} not implemented".format(type_))
    return TypeClass(buf, offset, chunk, parent, length)
    ### --- BLOCK END 106



def ValueNode(param_0, param_1, param_2, param_3):
    """
    The binary XML node for the system token 0x05.

    This is the "value" token.
    """
    def __init__(buf, offset, chunk, parent):
        ### --- BLOCK BEGIN 107
        
        class_var.declare_field("byte", "token", 0x0, None)
        class_var.declare_field("byte", "type", None, None)
        ### --- BLOCK END 107
    
    
    
    def __repr__():
        ### --- BLOCK BEGIN 108
        return "ValueNode(buf={!r}, offset={!r}, chunk={!r}, parent={!r})".format(
        class_var._buf, class_var.offset(), class_var._chunk, class_var._parent
        )
        ### --- BLOCK END 108
    
    
    
    def __str__():
        ### --- BLOCK BEGIN 109
        return "ValueNode(offset={}, length={}, token={}, value={})".format(
        hex(class_var.offset()), hex(class_var.length()), hex(class_var.token()), class_var.value().string()
        )
        ### --- BLOCK END 109
    
    
    
    def flags():
        ### --- BLOCK BEGIN 110
        return class_var.token() >> 4
        ### --- BLOCK END 110
    
    
    
    def value():
        ### --- BLOCK BEGIN 111
        return class_var.children()[0]
        ### --- BLOCK END 111
    
    
    
    def tag_length():
        ### --- BLOCK BEGIN 112
        return 2
        ### --- BLOCK END 112
    
    
    
    def children():
        ### --- BLOCK BEGIN 113
        child = get_variant_value(class_var._buf, class_var.offset() + class_var.tag_length(), class_var._chunk, class_var, class_var.type())
        return [child]
        ### --- BLOCK END 113
    
    
    
    def verify():
        ### --- BLOCK BEGIN 114
        return class_var.flags() & 0x0B == 0 and class_var.token() & 0x0F == SYSTEM_TOKENS.ValueToken
        ### --- BLOCK END 114
    
    
    
    class_var = BXmlNode(param_0, param_1, param_2, param_3)
    class_var._class_name = 'ValueNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.__repr__ = __repr__
    class_var.__str__ = __str__
    class_var.flags = flags
    class_var.value = value
    class_var.tag_length = tag_length
    class_var.children = children
    class_var.verify = verify
    __init__(param_0, param_1, param_2, param_3)
    return class_var


def AttributeNode(param_0, param_1, param_2, param_3):
    """
    The binary XML node for the system token 0x06.

    This is the "attribute" token.
    """
    def __init__(buf, offset, chunk, parent):
        ### --- BLOCK BEGIN 115
        
        class_var.declare_field("byte", "token", 0x0, None)
        class_var.declare_field("dword", "string_offset", None, None)
        class_var._name_string_length = 0
        if class_var.string_offset() > class_var.offset() - class_var._chunk._offset:
            new_string = class_var._chunk.add_string(class_var.string_offset(), parent=class_var)
            class_var._name_string_length += new_string.length()
        ### --- BLOCK END 115
    
    
    
    def __repr__():
        ### --- BLOCK BEGIN 116
        return "AttributeNode(buf={!r}, offset={!r}, chunk={!r}, parent={!r})".format(
        class_var._buf, class_var.offset(), class_var._chunk, class_var._parent
        )
        ### --- BLOCK END 116
    
    
    
    def __str__():
        ### --- BLOCK BEGIN 117
        return "AttributeNode(offset={}, length={}, token={}, name={}, value={})".format(
        hex(class_var.offset()), hex(class_var.length()), hex(class_var.token()), class_var.attribute_name(), class_var.attribute_value()
        )
        ### --- BLOCK END 117
    
    
    
    def flags():
        ### --- BLOCK BEGIN 118
        return class_var.token() >> 4
        ### --- BLOCK END 118
    
    
    
    def attribute_name():
        """
            @return A NameNode instance that contains the attribute name.
            """
        ### --- BLOCK BEGIN 119
        return class_var._chunk.strings()[class_var.string_offset()]
        ### --- BLOCK END 119
    
    
    
    def attribute_value():
        """
            @return A BXmlNode instance that is one of (ValueNode,
              ConditionalSubstitutionNode, NormalSubstitutionNode).
            """
        ### --- BLOCK BEGIN 120
        return class_var.children()[0]
        ### --- BLOCK END 120
    
    
    
    def tag_length():
        ### --- BLOCK BEGIN 121
        return 5 + class_var._name_string_length
        ### --- BLOCK END 121
    
    
    
    def verify():
        ### --- BLOCK BEGIN 122
        return class_var.flags() & 0x0B == 0 and class_var.opcode() & 0x0F == 0x06
        ### --- BLOCK END 122
    
    
    
    def children():
        ### --- BLOCK BEGIN 123
        return class_var._children(1, [0x00])
        ### --- BLOCK END 123
    
    
    
    class_var = BXmlNode(param_0, param_1, param_2, param_3)
    class_var._class_name = 'AttributeNode;' + class_var._class_name
    children = memoize(children, class_var)
    
    class_var.__init__ = __init__
    class_var.__repr__ = __repr__
    class_var.__str__ = __str__
    class_var.flags = flags
    class_var.attribute_name = attribute_name
    class_var.attribute_value = attribute_value
    class_var.tag_length = tag_length
    class_var.verify = verify
    class_var.children = children
    __init__(param_0, param_1, param_2, param_3)
    return class_var


def CDataSectionNode(param_0, param_1, param_2, param_3):
    """
    The binary XML node for the system token 0x07.

    This is the "CDATA section" system token.
    """
    def __init__(buf, offset, chunk, parent):
        ### --- BLOCK BEGIN 124
        
        class_var.declare_field("byte", "token", 0x0)
        class_var.declare_field("word", "string_length")
        class_var.declare_field("wstring", "cdata", length=class_var.string_length() - 2)
        ### --- BLOCK END 124
    
    
    
    def __repr__():
        ### --- BLOCK BEGIN 125
        return "CDataSectionNode(buf={!r}, offset={!r}, chunk={!r}, parent={!r})".format(
        class_var._buf, class_var.offset(), class_var._chunk, class_var._parent
        )
        ### --- BLOCK END 125
    
    
    
    def __str__():
        ### --- BLOCK BEGIN 126
        return "CDataSectionNode(offset={}, length={}, token={})".format(hex(class_var.offset()), hex(class_var.length()), 0x07)
        ### --- BLOCK END 126
    
    
    
    def flags():
        ### --- BLOCK BEGIN 127
        return class_var.token() >> 4
        ### --- BLOCK END 127
    
    
    
    def tag_length():
        ### --- BLOCK BEGIN 128
        return 0x3 + class_var.string_length()
        ### --- BLOCK END 128
    
    
    
    def length():
        ### --- BLOCK BEGIN 129
        return class_var.tag_length()
        ### --- BLOCK END 129
    
    
    
    def children():
        ### --- BLOCK BEGIN 130
        return []
        ### --- BLOCK END 130
    
    
    
    def verify():
        ### --- BLOCK BEGIN 131
        return class_var.flags() == 0x0 and class_var.token() & 0x0F == SYSTEM_TOKENS.CDataSectionToken
        ### --- BLOCK END 131
    
    
    
    class_var = BXmlNode(param_0, param_1, param_2, param_3)
    class_var._class_name = 'CDataSectionNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.__repr__ = __repr__
    class_var.__str__ = __str__
    class_var.flags = flags
    class_var.tag_length = tag_length
    class_var.length = length
    class_var.children = children
    class_var.verify = verify
    __init__(param_0, param_1, param_2, param_3)
    return class_var


def CharacterReferenceNode(param_0, param_1, param_2, param_3):
    """
    The binary XML node for the system token 0x08.

    This is an character reference node.  That is, something that represents
      a non-XML character, eg. & --> &#x0038;.
    """
    def __init__(buf, offset, chunk, parent):
        ### --- BLOCK BEGIN 132
        
        class_var.declare_field("byte", "token", 0x0)
        class_var.declare_field("word", "entity")
        class_var._tag_length = 3
        ### --- BLOCK END 132
    
    
    
    def __repr__():
        ### --- BLOCK BEGIN 133
        return "CharacterReferenceNode(buf={!r}, offset={!r}, chunk={!r}, parent={!r})".format(
        class_var._buf, class_var.offset(), class_var._chunk, class_var._parent
        )
        ### --- BLOCK END 133
    
    
    
    def __str__():
        ### --- BLOCK BEGIN 134
        return "CharacterReferenceNode(offset={}, length={}, token={})".format(
        hex(class_var.offset()), hex(class_var.length()), hex(0x08)
        )
        ### --- BLOCK END 134
    
    
    
    def entity_reference():
        ### --- BLOCK BEGIN 135
        return "&#x%04x;" % (class_var.entity())
        ### --- BLOCK END 135
    
    
    
    def flags():
        ### --- BLOCK BEGIN 136
        return class_var.token() >> 4
        ### --- BLOCK END 136
    
    
    
    def tag_length():
        ### --- BLOCK BEGIN 137
        return class_var._tag_length
        ### --- BLOCK END 137
    
    
    
    def children():
        ### --- BLOCK BEGIN 138
        return []
        ### --- BLOCK END 138
    
    
    
    class_var = BXmlNode(param_0, param_1, param_2, param_3)
    class_var._class_name = 'CharacterReferenceNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.__repr__ = __repr__
    class_var.__str__ = __str__
    class_var.entity_reference = entity_reference
    class_var.flags = flags
    class_var.tag_length = tag_length
    class_var.children = children
    __init__(param_0, param_1, param_2, param_3)
    return class_var


def EntityReferenceNode(param_0, param_1, param_2, param_3):
    """
    The binary XML node for the system token 0x09.

    This is an entity reference node.  That is, something that represents
      a non-XML character, eg. & --> &amp;.

    TODO(wb): this is untested.
    """
    def __init__(buf, offset, chunk, parent):
        ### --- BLOCK BEGIN 139
        
        class_var.declare_field("byte", "token", 0x0)
        class_var.declare_field("dword", "string_offset")
        class_var._tag_length = 5
        if class_var.string_offset() > class_var.offset() - class_var._chunk.offset():
            new_string = class_var._chunk.add_string(class_var.string_offset(), parent=class_var)
            class_var._tag_length += new_string.length()
        ### --- BLOCK END 139
    
    
    
    def __repr__():
        ### --- BLOCK BEGIN 140
        return "EntityReferenceNode(buf={!r}, offset={!r}, chunk={!r}, parent={!r})".format(
        class_var._buf, class_var.offset(), class_var._chunk, class_var._parent
        )
        ### --- BLOCK END 140
    
    
    
    def __str__():
        ### --- BLOCK BEGIN 141
        return "EntityReferenceNode(offset={}, length={}, token={})".format(
        hex(class_var.offset()), hex(class_var.length()), hex(0x09)
        )
        ### --- BLOCK END 141
    
    
    
    def entity_reference():
        ### --- BLOCK BEGIN 142
        return "&{};".format(class_var._chunk.strings()[class_var.string_offset()].string())
        ### --- BLOCK END 142
    
    
    
    def flags():
        ### --- BLOCK BEGIN 143
        return class_var.token() >> 4
        ### --- BLOCK END 143
    
    
    
    def tag_length():
        ### --- BLOCK BEGIN 144
        return class_var._tag_length
        ### --- BLOCK END 144
    
    
    
    def children():
        ### --- BLOCK BEGIN 145
        return []
        ### --- BLOCK END 145
    
    
    
    class_var = BXmlNode(param_0, param_1, param_2, param_3)
    class_var._class_name = 'EntityReferenceNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.__repr__ = __repr__
    class_var.__str__ = __str__
    class_var.entity_reference = entity_reference
    class_var.flags = flags
    class_var.tag_length = tag_length
    class_var.children = children
    __init__(param_0, param_1, param_2, param_3)
    return class_var


def ProcessingInstructionTargetNode(param_0, param_1, param_2, param_3):
    """
    The binary XML node for the system token 0x0A.

    TODO(wb): untested.
    """
    def __init__(buf, offset, chunk, parent):
        ### --- BLOCK BEGIN 146
        
        class_var.declare_field("byte", "token", 0x0)
        class_var.declare_field("dword", "string_offset")
        class_var._tag_length = 5
        if class_var.string_offset() > class_var.offset() - class_var._chunk.offset():
            new_string = class_var._chunk.add_string(class_var.string_offset(), parent=class_var)
            class_var._tag_length += new_string.length()
        ### --- BLOCK END 146
    
    
    
    def __repr__():
        ### --- BLOCK BEGIN 147
        return "ProcessingInstructionTargetNode(buf={!r}, offset={!r}, chunk={!r}, parent={!r})".format(
        class_var._buf, class_var.offset(), class_var._chunk, class_var._parent
        )
        ### --- BLOCK END 147
    
    
    
    def __str__():
        ### --- BLOCK BEGIN 148
        return "ProcessingInstructionTargetNode(offset={}, length={}, token={})".format(
        hex(class_var.offset()), hex(class_var.length()), hex(0x0A)
        )
        ### --- BLOCK END 148
    
    
    
    def processing_instruction_target():
        ### --- BLOCK BEGIN 149
        return "<?{}".format(class_var._chunk.strings()[class_var.string_offset()].string())
        ### --- BLOCK END 149
    
    
    
    def flags():
        ### --- BLOCK BEGIN 150
        return class_var.token() >> 4
        ### --- BLOCK END 150
    
    
    
    def tag_length():
        ### --- BLOCK BEGIN 151
        return class_var._tag_length
        ### --- BLOCK END 151
    
    
    
    def children():
        ### --- BLOCK BEGIN 152
        return []
        ### --- BLOCK END 152
    
    
    
    class_var = BXmlNode(param_0, param_1, param_2, param_3)
    class_var._class_name = 'ProcessingInstructionTargetNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.__repr__ = __repr__
    class_var.__str__ = __str__
    class_var.processing_instruction_target = processing_instruction_target
    class_var.flags = flags
    class_var.tag_length = tag_length
    class_var.children = children
    __init__(param_0, param_1, param_2, param_3)
    return class_var


def ProcessingInstructionDataNode(param_0, param_1, param_2, param_3):
    """
    The binary XML node for the system token 0x0B.

    TODO(wb): untested.
    """
    def __init__(buf, offset, chunk, parent):
        ### --- BLOCK BEGIN 153
        
        class_var.declare_field("byte", "token", 0x0)
        class_var.declare_field("word", "string_length")
        class_var._tag_length = 3 + (2 * class_var.string_length())
        if class_var.string_length() > 0:
            class_var._string = class_var.unpack_wstring(0x3, class_var.string_length())
        else:
            class_var._string = ""
        ### --- BLOCK END 153
    
    
    
    def __repr__():
        ### --- BLOCK BEGIN 154
        return "ProcessingInstructionDataNode(buf={!r}, offset={!r}, chunk={!r}, parent={!r})".format(
        class_var._buf, class_var.offset(), class_var._chunk, class_var._parent
        )
        ### --- BLOCK END 154
    
    
    
    def __str__():
        ### --- BLOCK BEGIN 155
        return "ProcessingInstructionDataNode(offset={}, length={}, token={})".format(
        hex(class_var.offset()), hex(class_var.length()), hex(0x0B)
        )
        ### --- BLOCK END 155
    
    
    
    def flags():
        ### --- BLOCK BEGIN 156
        return class_var.token() >> 4
        ### --- BLOCK END 156
    
    
    
    def string():
        ### --- BLOCK BEGIN 157
        if class_var.string_length() > 0:
            return " {}?>".format(class_var._string)
        else:
            return "?>"
        ### --- BLOCK END 157
    
    
    
    def tag_length():
        ### --- BLOCK BEGIN 158
        return class_var._tag_length
        ### --- BLOCK END 158
    
    
    
    def children():
        ### --- BLOCK BEGIN 159
        return []
        ### --- BLOCK END 159
    
    
    
    class_var = BXmlNode(param_0, param_1, param_2, param_3)
    class_var._class_name = 'ProcessingInstructionDataNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.__repr__ = __repr__
    class_var.__str__ = __str__
    class_var.flags = flags
    class_var.string = string
    class_var.tag_length = tag_length
    class_var.children = children
    __init__(param_0, param_1, param_2, param_3)
    return class_var


def TemplateInstanceNode(param_0, param_1, param_2, param_3):
    """
    The binary XML node for the system token 0x0C.
    """
    def __init__(buf, offset, chunk, parent):
        ### --- BLOCK BEGIN 160
        
        class_var.declare_field("byte", "token", 0x0, None)
        class_var.declare_field("byte", "unknown0", None, None)
        class_var.declare_field("dword", "template_id", None, None)
        class_var.declare_field("dword", "template_offset", None, None)
        class_var._data_length = 0
        if class_var.is_resident_template():
            new_template = class_var._chunk.add_template(class_var.template_offset(), parent=class_var)
            class_var._data_length += new_template.length()
        ### --- BLOCK END 160
    
    
    
    def __repr__():
        ### --- BLOCK BEGIN 161
        return "TemplateInstanceNode(buf={!r}, offset={!r}, chunk={!r}, parent={!r})".format(
        class_var._buf, class_var.offset(), class_var._chunk, class_var._parent
        )
        ### --- BLOCK END 161
    
    
    
    def __str__():
        ### --- BLOCK BEGIN 162
        return "TemplateInstanceNode(offset={}, length={}, token={})".format(
        hex(class_var.offset()), hex(class_var.length()), hex(0x0C)
        )
        ### --- BLOCK END 162
    
    
    
    def flags():
        ### --- BLOCK BEGIN 163
        return class_var.token() >> 4
        ### --- BLOCK END 163
    
    
    
    def is_resident_template():
        ### --- BLOCK BEGIN 164
        return class_var.template_offset() > class_var.offset() - class_var._chunk._offset
        ### --- BLOCK END 164
    
    
    
    def tag_length():
        ### --- BLOCK BEGIN 165
        return 10
        ### --- BLOCK END 165
    
    
    
    def length():
        ### --- BLOCK BEGIN 166
        return class_var.tag_length() + class_var._data_length
        ### --- BLOCK END 166
    
    
    
    def template():
        ### --- BLOCK BEGIN 167
        return class_var._chunk.templates()[class_var.template_offset()]
        ### --- BLOCK END 167
    
    
    
    def children():
        ### --- BLOCK BEGIN 168
        return []
        ### --- BLOCK END 168
    
    
    
    def find_end_of_stream():
        ### --- BLOCK BEGIN 169
        return class_var.template().find_end_of_stream()
        ### --- BLOCK END 169
    
    
    
    class_var = BXmlNode(param_0, param_1, param_2, param_3)
    class_var._class_name = 'TemplateInstanceNode;' + class_var._class_name
    find_end_of_stream = memoize(find_end_of_stream, class_var)
    
    class_var.__init__ = __init__
    class_var.__repr__ = __repr__
    class_var.__str__ = __str__
    class_var.flags = flags
    class_var.is_resident_template = is_resident_template
    class_var.tag_length = tag_length
    class_var.length = length
    class_var.template = template
    class_var.children = children
    class_var.find_end_of_stream = find_end_of_stream
    __init__(param_0, param_1, param_2, param_3)
    return class_var


def NormalSubstitutionNode(param_0, param_1, param_2, param_3):
    """
    The binary XML node for the system token 0x0D.

    This is a "normal substitution" token.
    """
    def __init__(buf, offset, chunk, parent):
        ### --- BLOCK BEGIN 170
        
        class_var.declare_field("byte", "token", 0x0, None)
        class_var.declare_field("word", "index", None, None)
        class_var.declare_field("byte", "type", None, None)
        ### --- BLOCK END 170
    
    
    
    def __repr__():
        ### --- BLOCK BEGIN 171
        return "NormalSubstitutionNode(buf={!r}, offset={!r}, chunk={!r}, parent={!r})".format(
        class_var._buf, class_var.offset(), class_var._chunk, class_var._parent
        )
        ### --- BLOCK END 171
    
    
    
    def __str__():
        ### --- BLOCK BEGIN 172
        return "NormalSubstitutionNode(offset={}, length={}, token={}, index={}, type={})".format(
        hex(class_var.offset()), hex(class_var.length()), hex(class_var.token()), class_var.index(), class_var.type()
        )
        ### --- BLOCK END 172
    
    
    
    def flags():
        ### --- BLOCK BEGIN 173
        return class_var.token() >> 4
        ### --- BLOCK END 173
    
    
    
    def tag_length():
        ### --- BLOCK BEGIN 174
        return 0x4
        ### --- BLOCK END 174
    
    
    
    def length():
        ### --- BLOCK BEGIN 175
        return class_var.tag_length()
        ### --- BLOCK END 175
    
    
    
    def children():
        ### --- BLOCK BEGIN 176
        return []
        ### --- BLOCK END 176
    
    
    
    def verify():
        ### --- BLOCK BEGIN 177
        return class_var.flags() == 0 and class_var.token() & 0x0F == SYSTEM_TOKENS.NormalSubstitutionToken
        ### --- BLOCK END 177
    
    
    
    class_var = BXmlNode(param_0, param_1, param_2, param_3)
    class_var._class_name = 'NormalSubstitutionNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.__repr__ = __repr__
    class_var.__str__ = __str__
    class_var.flags = flags
    class_var.tag_length = tag_length
    class_var.length = length
    class_var.children = children
    class_var.verify = verify
    __init__(param_0, param_1, param_2, param_3)
    return class_var


def ConditionalSubstitutionNode(param_0, param_1, param_2, param_3):
    """
    The binary XML node for the system token 0x0E.
    """
    def __init__(buf, offset, chunk, parent):
        ### --- BLOCK BEGIN 178
        
        class_var.declare_field("byte", "token", 0x0, None)
        class_var.declare_field("word", "index", None, None)
        class_var.declare_field("byte", "type", None, None)
        ### --- BLOCK END 178
    
    
    
    def __repr__():
        ### --- BLOCK BEGIN 179
        return "ConditionalSubstitutionNode(buf={!r}, offset={!r}, chunk={!r}, parent={!r})".format(
        class_var._buf, class_var.offset(), class_var._chunk, class_var._parent
        )
        ### --- BLOCK END 179
    
    
    
    def __str__():
        ### --- BLOCK BEGIN 180
        return "ConditionalSubstitutionNode(offset={}, length={}, token={})".format(
        hex(class_var.offset()), hex(class_var.length()), hex(0x0E)
        )
        ### --- BLOCK END 180
    
    
    
    def should_suppress(substitutions):
        ### --- BLOCK BEGIN 181
        sub = substitutions[class_var.index()]
        return user_get_type(sub) is NullTypeNode
        ### --- BLOCK END 181
    
    
    
    def flags():
        ### --- BLOCK BEGIN 182
        return class_var.token() >> 4
        ### --- BLOCK END 182
    
    
    
    def tag_length():
        ### --- BLOCK BEGIN 183
        return 0x4
        ### --- BLOCK END 183
    
    
    
    def length():
        ### --- BLOCK BEGIN 184
        return class_var.tag_length()
        ### --- BLOCK END 184
    
    
    
    def children():
        ### --- BLOCK BEGIN 185
        return []
        ### --- BLOCK END 185
    
    
    
    def verify():
        ### --- BLOCK BEGIN 186
        return class_var.flags() == 0 and class_var.token() & 0x0F == SYSTEM_TOKENS.ConditionalSubstitutionToken
        ### --- BLOCK END 186
    
    
    
    class_var = BXmlNode(param_0, param_1, param_2, param_3)
    class_var._class_name = 'ConditionalSubstitutionNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.__repr__ = __repr__
    class_var.__str__ = __str__
    class_var.should_suppress = should_suppress
    class_var.flags = flags
    class_var.tag_length = tag_length
    class_var.length = length
    class_var.children = children
    class_var.verify = verify
    __init__(param_0, param_1, param_2, param_3)
    return class_var


def StreamStartNode(param_0, param_1, param_2, param_3):
    """
    The binary XML node for the system token 0x0F.

    This is the "start of stream" token.
    """
    def __init__(buf, offset, chunk, parent):
        ### --- BLOCK BEGIN 187
        
        class_var.declare_field("byte", "token", 0x0, None)
        class_var.declare_field("byte", "unknown0", None, None)
        class_var.declare_field("word", "unknown1", None, None)
        ### --- BLOCK END 187
    
    
    
    def __repr__():
        ### --- BLOCK BEGIN 188
        return "StreamStartNode(buf={!r}, offset={!r}, chunk={!r}, parent={!r})".format(
        class_var._buf, class_var.offset(), class_var._chunk, class_var._parent
        )
        ### --- BLOCK END 188
    
    
    
    def __str__():
        ### --- BLOCK BEGIN 189
        return "StreamStartNode(offset={}, length={}, token={})".format(
        hex(class_var.offset()), hex(class_var.length()), hex(class_var.token())
        )
        ### --- BLOCK END 189
    
    
    
    def verify():
        ### --- BLOCK BEGIN 190
        return (
        class_var.flags() == 0x0
        and class_var.token() & 0x0F == SYSTEM_TOKENS.StartOfStreamToken
        and class_var.unknown0() == 0x1
        and class_var.unknown1() == 0x1
        )
        ### --- BLOCK END 190
    
    
    
    def flags():
        ### --- BLOCK BEGIN 191
        return class_var.token() >> 4
        ### --- BLOCK END 191
    
    
    
    def tag_length():
        ### --- BLOCK BEGIN 192
        return 4
        ### --- BLOCK END 192
    
    
    
    def length():
        ### --- BLOCK BEGIN 193
        return class_var.tag_length() + 0
        ### --- BLOCK END 193
    
    
    
    def children():
        ### --- BLOCK BEGIN 194
        return []
        ### --- BLOCK END 194
    
    
    
    class_var = BXmlNode(param_0, param_1, param_2, param_3)
    class_var._class_name = 'StreamStartNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.__repr__ = __repr__
    class_var.__str__ = __str__
    class_var.verify = verify
    class_var.flags = flags
    class_var.tag_length = tag_length
    class_var.length = length
    class_var.children = children
    __init__(param_0, param_1, param_2, param_3)
    return class_var


def RootNode(param_0, param_1, param_2, param_3):
    """
    The binary XML node for the Root node.
    """
    def __init__(buf, offset, chunk, parent):
        ### --- BLOCK BEGIN 195
        
        pass
        ### --- BLOCK END 195
    
    
    
    def __repr__():
        ### --- BLOCK BEGIN 196
        return "RootNode(buf={!r}, offset={!r}, chunk={!r}, parent={!r})".format(
        class_var._buf, class_var.offset(), class_var._chunk, class_var._parent
        )
        ### --- BLOCK END 196
    
    
    
    def __str__():
        ### --- BLOCK BEGIN 197
        return "RootNode(offset={}, length={})".format(hex(class_var.offset()), hex(class_var.length()))
        ### --- BLOCK END 197
    
    
    
    def tag_length():
        ### --- BLOCK BEGIN 198
        return 0
        ### --- BLOCK END 198
    
    
    
    def children():
        """
            @return The template instances which make up this node.
            """
        ### --- BLOCK BEGIN 199
        return class_var._children(None, [SYSTEM_TOKENS.EndOfStreamToken])
        ### --- BLOCK END 199
    
    
    
    def tag_and_children_length():
        """
            @return The length of the tag of this element, and the children.
              This does not take into account the substitutions that may be
              at the end of this element.
            """
        ### --- BLOCK BEGIN 200
        children_length = 0
        for child in class_var.children():
            children_length += child.length()
        return class_var.tag_length() + children_length
        ### --- BLOCK END 200
    
    
    
    def template_instance():
        """
            parse the template instance node.
            this is used to compute the location of the template definition structure.
    
            Returns:
              TemplateInstanceNode: the template instance.
            """
        ### --- BLOCK BEGIN 201
        ofs = class_var.offset()
        if class_var.unpack_byte(0x0) & 0x0F == 0xF:
            ofs += 4
        return TemplateInstanceNode(class_var._buf, ofs, class_var._chunk, class_var)
        ### --- BLOCK END 201
    
    
    
    def template():
        """
            parse the template referenced by this root node.
            note, this template structure is not guaranteed to be located within the root node's boundaries.
    
            Returns:
              TemplateNode: the template.
            """
        ### --- BLOCK BEGIN 202
        instance = class_var.template_instance()
        offset = class_var._chunk.offset() + instance.template_offset()
        node = TemplateNode(class_var._buf, offset, class_var._chunk, instance)
        return node
        ### --- BLOCK END 202
    
    
    
    def substitutions():
        """
            @return A list of VariantTypeNode subclass instances that
              contain the substitutions for this root node.
            """
        ### --- BLOCK BEGIN 203
        sub_decl = []
        sub_def = []
        ofs = class_var.tag_and_children_length()
        sub_count = class_var.unpack_dword(ofs)
        ofs += 4
        for _ in range(sub_count):
            size = class_var.unpack_word(ofs)
            type_ = class_var.unpack_byte(ofs + 0x2)
            sub_decl.append((size, type_))
            ofs += 4
        for size, type_ in sub_decl:
            val = get_variant_value(class_var._buf, class_var.offset() + ofs, class_var._chunk, class_var, type_, length=size)
            if abs(size - val.length()) > 4:
            # TODO(wb): This is a hack, so I'm sorry.
            #   But, we are not passing around a 'length' field,
            #   so we have to depend on the structure of each
            #   variant type.  It seems some BXmlTypeNode sizes
            #   are not exact.  Hopefully, this is just alignment.
            #   So, that's what we compensate for here.
                raise ParseException("Invalid substitution value size")
            sub_def.append(val)
            ofs += size
        return sub_def
        ### --- BLOCK END 203
    
    
    
    def length():
        ### --- BLOCK BEGIN 204
        ofs = class_var.tag_and_children_length()
        sub_count = class_var.unpack_dword(ofs)
        ofs += 4
        ret = ofs
        for _ in range(sub_count):
            size = class_var.unpack_word(ofs)
            ret += size + 4
            ofs += 4
        return ret
        ### --- BLOCK END 204
    
    
    
    class_var = BXmlNode(param_0, param_1, param_2, param_3)
    class_var._class_name = 'RootNode;' + class_var._class_name
    children = memoize(children, class_var)
    
    substitutions = memoize(substitutions, class_var)
    
    length = memoize(length, class_var)
    
    class_var.__init__ = __init__
    class_var.__repr__ = __repr__
    class_var.__str__ = __str__
    class_var.tag_length = tag_length
    class_var.children = children
    class_var.tag_and_children_length = tag_and_children_length
    class_var.template_instance = template_instance
    class_var.template = template
    class_var.substitutions = substitutions
    class_var.length = length
    __init__(param_0, param_1, param_2, param_3)
    return class_var


def VariantTypeNode(param_0, param_1, param_2, param_3, param_4):
    """ """
    def __init__(buf, offset, chunk, parent, length):
        ### --- BLOCK BEGIN 205
        
        class_var._length = length
        ### --- BLOCK END 205
    
    
    
    def __repr__():
        ### --- BLOCK BEGIN 206
        return "{}(buf={!r}, offset={}, chunk={!r})".format(
        class_var._class_name.split(';')[0], class_var._buf, hex(class_var.offset()), class_var._chunk
        )
        ### --- BLOCK END 206
    
    
    
    def __str__():
        ### --- BLOCK BEGIN 207
        return "{}(offset={}, length={}, string={})".format(
        class_var._class_name.split(';')[0], hex(class_var.offset()), hex(class_var.length()), class_var.string()
        )
        ### --- BLOCK END 207
    
    
    
    def tag_length():
        ### --- BLOCK BEGIN 208
        raise NotImplementedError("tag_length not implemented for {!r}".format(class_var))
        ### --- BLOCK END 208
    
    
    
    def length():
        ### --- BLOCK BEGIN 209
        return class_var.tag_length()
        ### --- BLOCK END 209
    
    
    
    def children():
        ### --- BLOCK BEGIN 210
        return []
        ### --- BLOCK END 210
    
    
    
    def string():
        ### --- BLOCK BEGIN 211
        raise NotImplementedError("string not implemented for {!r}".format(class_var))
        ### --- BLOCK END 211
    
    
    
    class_var = BXmlNode(param_0, param_1, param_2, param_3)
    class_var._class_name = 'VariantTypeNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.__repr__ = __repr__
    class_var.__str__ = __str__
    class_var.tag_length = tag_length
    class_var.length = length
    class_var.children = children
    class_var.string = string
    __init__(param_0, param_1, param_2, param_3, param_4)
    return class_var


# but satisfies the contract of VariantTypeNode, BXmlNode, but not Block

def NullTypeNode(param_0, param_1, param_2, param_3, param_4):
    """
    Variant type 0x00.
    """
    def __init__(buf, offset, chunk, parent, length):
        ### --- BLOCK BEGIN 212
        
        class_var._offset = offset
        class_var._length = length
        ### --- BLOCK END 212
    
    
    
    def __str__():
        ### --- BLOCK BEGIN 213
        return "NullTypeNode"
        ### --- BLOCK END 213
    
    
    
    def string():
        ### --- BLOCK BEGIN 214
        return ""
        ### --- BLOCK END 214
    
    
    
    def length():
        ### --- BLOCK BEGIN 215
        return class_var._length or 0
        ### --- BLOCK END 215
    
    
    
    def tag_length():
        ### --- BLOCK BEGIN 216
        return class_var._length or 0
        ### --- BLOCK END 216
    
    
    
    def children():
        ### --- BLOCK BEGIN 217
        return []
        ### --- BLOCK END 217
    
    
    
    def offset():
        ### --- BLOCK BEGIN 218
        return class_var._offset
        ### --- BLOCK END 218
    
    
    
    class_var = SkelClass('NullTypeNode')
    class_var.__init__ = __init__
    class_var.__str__ = __str__
    class_var.string = string
    class_var.length = length
    class_var.tag_length = tag_length
    class_var.children = children
    class_var.offset = offset
    __init__(param_0, param_1, param_2, param_3, param_4)
    return class_var


def WstringTypeNode(param_0, param_1, param_2, param_3, param_4):
    """
    Variant ttype 0x01.
    """
    def __init__(buf, offset, chunk, parent, length):
        ### --- BLOCK BEGIN 219
        
        if class_var._length is None:
            class_var.declare_field("word", "string_length", 0x0, None)
            class_var.declare_field("wstring", "_string", length=(class_var.string_length()))
        else:
            class_var.declare_field("wstring", "_string", 0x0, (class_var._length // 2))
        ### --- BLOCK END 219
    
    
    
    def tag_length():
        ### --- BLOCK BEGIN 220
        if class_var._length is None:
            return 2 + (class_var.string_length() * 2)
        return class_var._length
        ### --- BLOCK END 220
    
    
    
    def string():
        ### --- BLOCK BEGIN 221
        return class_var._string().rstrip("\x00")
        ### --- BLOCK END 221
    
    
    
    class_var = VariantTypeNode(param_0, param_1, param_2, param_3, param_4)
    class_var._class_name = 'WstringTypeNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.tag_length = tag_length
    class_var.string = string
    __init__(param_0, param_1, param_2, param_3, param_4)
    return class_var


def StringTypeNode(param_0, param_1, param_2, param_3, param_4):
    """
    Variant type 0x02.
    """
    def __init__(buf, offset, chunk, parent, length):
        ### --- BLOCK BEGIN 222
        
        if class_var._length is None:
            class_var.declare_field("word", "string_length", 0x0)
            class_var.declare_field("string", "_string", length=(class_var.string_length()))
        else:
            class_var.declare_field("string", "_string", 0x0, length=class_var._length)
        ### --- BLOCK END 222
    
    
    
    def tag_length():
        ### --- BLOCK BEGIN 223
        if class_var._length is None:
            return 2 + (class_var.string_length())
        return class_var._length
        ### --- BLOCK END 223
    
    
    
    def string():
        ### --- BLOCK BEGIN 224
        return class_var._string().rstrip("\x00")
        ### --- BLOCK END 224
    
    
    
    class_var = VariantTypeNode(param_0, param_1, param_2, param_3, param_4)
    class_var._class_name = 'StringTypeNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.tag_length = tag_length
    class_var.string = string
    __init__(param_0, param_1, param_2, param_3, param_4)
    return class_var


def SignedByteTypeNode(param_0, param_1, param_2, param_3, param_4):
    """
    Variant type 0x03.
    """
    def __init__(buf, offset, chunk, parent, length):
        ### --- BLOCK BEGIN 225
        
        class_var.declare_field("int8", "byte", 0x0)
        ### --- BLOCK END 225
    
    
    
    def tag_length():
        ### --- BLOCK BEGIN 226
        return 1
        ### --- BLOCK END 226
    
    
    
    def string():
        ### --- BLOCK BEGIN 227
        return str(class_var.byte())
        ### --- BLOCK END 227
    
    
    
    class_var = VariantTypeNode(param_0, param_1, param_2, param_3, param_4)
    class_var._class_name = 'SignedByteTypeNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.tag_length = tag_length
    class_var.string = string
    __init__(param_0, param_1, param_2, param_3, param_4)
    return class_var


def UnsignedByteTypeNode(param_0, param_1, param_2, param_3, param_4):
    """
    Variant type 0x04.
    """
    def __init__(buf, offset, chunk, parent, length):
        ### --- BLOCK BEGIN 228
        
        class_var.declare_field("byte", "byte", 0x0, None)
        ### --- BLOCK END 228
    
    
    
    def tag_length():
        ### --- BLOCK BEGIN 229
        return 1
        ### --- BLOCK END 229
    
    
    
    def string():
        ### --- BLOCK BEGIN 230
        return str(class_var.byte())
        ### --- BLOCK END 230
    
    
    
    class_var = VariantTypeNode(param_0, param_1, param_2, param_3, param_4)
    class_var._class_name = 'UnsignedByteTypeNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.tag_length = tag_length
    class_var.string = string
    __init__(param_0, param_1, param_2, param_3, param_4)
    return class_var


def SignedWordTypeNode(param_0, param_1, param_2, param_3, param_4):
    """
    Variant type 0x05.
    """
    def __init__(buf, offset, chunk, parent, length):
        ### --- BLOCK BEGIN 231
        
        class_var.declare_field("int16", "word", 0x0)
        ### --- BLOCK END 231
    
    
    
    def tag_length():
        ### --- BLOCK BEGIN 232
        return 2
        ### --- BLOCK END 232
    
    
    
    def string():
        ### --- BLOCK BEGIN 233
        return str(class_var.word())
        ### --- BLOCK END 233
    
    
    
    class_var = VariantTypeNode(param_0, param_1, param_2, param_3, param_4)
    class_var._class_name = 'SignedWordTypeNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.tag_length = tag_length
    class_var.string = string
    __init__(param_0, param_1, param_2, param_3, param_4)
    return class_var


def UnsignedWordTypeNode(param_0, param_1, param_2, param_3, param_4):
    """
    Variant type 0x06.
    """
    def __init__(buf, offset, chunk, parent, length):
        ### --- BLOCK BEGIN 234
        
        class_var.declare_field("word", "word", 0x0, None)
        ### --- BLOCK END 234
    
    
    
    def tag_length():
        ### --- BLOCK BEGIN 235
        return 2
        ### --- BLOCK END 235
    
    
    
    def string():
        ### --- BLOCK BEGIN 236
        return str(class_var.word())
        ### --- BLOCK END 236
    
    
    
    class_var = VariantTypeNode(param_0, param_1, param_2, param_3, param_4)
    class_var._class_name = 'UnsignedWordTypeNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.tag_length = tag_length
    class_var.string = string
    __init__(param_0, param_1, param_2, param_3, param_4)
    return class_var


def SignedDwordTypeNode(param_0, param_1, param_2, param_3, param_4):
    """
    Variant type 0x07.
    """
    def __init__(buf, offset, chunk, parent, length):
        ### --- BLOCK BEGIN 237
        
        class_var.declare_field("int32", "dword", 0x0)
        ### --- BLOCK END 237
    
    
    
    def tag_length():
        ### --- BLOCK BEGIN 238
        return 4
        ### --- BLOCK END 238
    
    
    
    def string():
        ### --- BLOCK BEGIN 239
        return str(class_var.dword())
        ### --- BLOCK END 239
    
    
    
    class_var = VariantTypeNode(param_0, param_1, param_2, param_3, param_4)
    class_var._class_name = 'SignedDwordTypeNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.tag_length = tag_length
    class_var.string = string
    __init__(param_0, param_1, param_2, param_3, param_4)
    return class_var


def UnsignedDwordTypeNode(param_0, param_1, param_2, param_3, param_4):
    """
    Variant type 0x08.
    """
    def __init__(buf, offset, chunk, parent, length):
        ### --- BLOCK BEGIN 240
        
        class_var.declare_field("dword", "dword", 0x0, None)
        ### --- BLOCK END 240
    
    
    
    def tag_length():
        ### --- BLOCK BEGIN 241
        return 4
        ### --- BLOCK END 241
    
    
    
    def string():
        ### --- BLOCK BEGIN 242
        return str(class_var.dword())
        ### --- BLOCK END 242
    
    
    
    class_var = VariantTypeNode(param_0, param_1, param_2, param_3, param_4)
    class_var._class_name = 'UnsignedDwordTypeNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.tag_length = tag_length
    class_var.string = string
    __init__(param_0, param_1, param_2, param_3, param_4)
    return class_var


def SignedQwordTypeNode(param_0, param_1, param_2, param_3, param_4):
    """
    Variant type 0x09.
    """
    def __init__(buf, offset, chunk, parent, length):
        ### --- BLOCK BEGIN 243
        
        class_var.declare_field("int64", "qword", 0x0)
        ### --- BLOCK END 243
    
    
    
    def tag_length():
        ### --- BLOCK BEGIN 244
        return 8
        ### --- BLOCK END 244
    
    
    
    def string():
        ### --- BLOCK BEGIN 245
        return str(class_var.qword())
        ### --- BLOCK END 245
    
    
    
    class_var = VariantTypeNode(param_0, param_1, param_2, param_3, param_4)
    class_var._class_name = 'SignedQwordTypeNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.tag_length = tag_length
    class_var.string = string
    __init__(param_0, param_1, param_2, param_3, param_4)
    return class_var


def UnsignedQwordTypeNode(param_0, param_1, param_2, param_3, param_4):
    """
    Variant type 0x0A.
    """
    def __init__(buf, offset, chunk, parent, length):
        ### --- BLOCK BEGIN 246
        
        class_var.declare_field("qword", "qword", 0x0, None)
        ### --- BLOCK END 246
    
    
    
    def tag_length():
        ### --- BLOCK BEGIN 247
        return 8
        ### --- BLOCK END 247
    
    
    
    def string():
        ### --- BLOCK BEGIN 248
        return str(class_var.qword())
        ### --- BLOCK END 248
    
    
    
    class_var = VariantTypeNode(param_0, param_1, param_2, param_3, param_4)
    class_var._class_name = 'UnsignedQwordTypeNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.tag_length = tag_length
    class_var.string = string
    __init__(param_0, param_1, param_2, param_3, param_4)
    return class_var


def FloatTypeNode(param_0, param_1, param_2, param_3, param_4):
    """
    Variant type 0x0B.
    """
    def __init__(buf, offset, chunk, parent, length):
        ### --- BLOCK BEGIN 249
        
        class_var.declare_field("float", "float", 0x0)
        ### --- BLOCK END 249
    
    
    
    def tag_length():
        ### --- BLOCK BEGIN 250
        return 4
        ### --- BLOCK END 250
    
    
    
    def string():
        ### --- BLOCK BEGIN 251
        return str(class_var.float())
        ### --- BLOCK END 251
    
    
    
    class_var = VariantTypeNode(param_0, param_1, param_2, param_3, param_4)
    class_var._class_name = 'FloatTypeNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.tag_length = tag_length
    class_var.string = string
    __init__(param_0, param_1, param_2, param_3, param_4)
    return class_var


def DoubleTypeNode(param_0, param_1, param_2, param_3, param_4):
    """
    Variant type 0x0C.
    """
    def __init__(buf, offset, chunk, parent, length):
        ### --- BLOCK BEGIN 252
        
        class_var.declare_field("double", "double", 0x0)
        ### --- BLOCK END 252
    
    
    
    def tag_length():
        ### --- BLOCK BEGIN 253
        return 8
        ### --- BLOCK END 253
    
    
    
    def string():
        ### --- BLOCK BEGIN 254
        return str(class_var.double())
        ### --- BLOCK END 254
    
    
    
    class_var = VariantTypeNode(param_0, param_1, param_2, param_3, param_4)
    class_var._class_name = 'DoubleTypeNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.tag_length = tag_length
    class_var.string = string
    __init__(param_0, param_1, param_2, param_3, param_4)
    return class_var


def BooleanTypeNode(param_0, param_1, param_2, param_3, param_4):
    """
    Variant type 0x0D.
    """
    def __init__(buf, offset, chunk, parent, length):
        ### --- BLOCK BEGIN 255
        
        class_var.declare_field("int32", "int32", 0x0, None)
        ### --- BLOCK END 255
    
    
    
    def tag_length():
        ### --- BLOCK BEGIN 256
        return 4
        ### --- BLOCK END 256
    
    
    
    def string():
        ### --- BLOCK BEGIN 257
        if class_var.int32() > 0:
            return "True"
        return "False"
        ### --- BLOCK END 257
    
    
    
    class_var = VariantTypeNode(param_0, param_1, param_2, param_3, param_4)
    class_var._class_name = 'BooleanTypeNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.tag_length = tag_length
    class_var.string = string
    __init__(param_0, param_1, param_2, param_3, param_4)
    return class_var


def BinaryTypeNode(param_0, param_1, param_2, param_3, param_4):
    """
    Variant type 0x0E.

    String/XML representation is Base64 encoded.
    """
    def __init__(buf, offset, chunk, parent, length):
        ### --- BLOCK BEGIN 258
        
        if class_var._length is None:
            class_var.declare_field("dword", "size", 0x0)
            class_var.declare_field("binary", "binary", length=class_var.size())
        else:
            class_var.declare_field("binary", "binary", 0x0, class_var._length)
        ### --- BLOCK END 258
    
    
    
    def tag_length():
        ### --- BLOCK BEGIN 259
        if class_var._length is None:
            return 4 + class_var.size()
        return class_var._length
        ### --- BLOCK END 259
    
    
    
    def string():
        ### --- BLOCK BEGIN 260
        return base64.b64encode(class_var.binary()).decode("ascii")
        ### --- BLOCK END 260
    
    
    
    class_var = VariantTypeNode(param_0, param_1, param_2, param_3, param_4)
    class_var._class_name = 'BinaryTypeNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.tag_length = tag_length
    class_var.string = string
    __init__(param_0, param_1, param_2, param_3, param_4)
    return class_var


def GuidTypeNode(param_0, param_1, param_2, param_3, param_4):
    """
    Variant type 0x0F.
    """
    def __init__(buf, offset, chunk, parent, length):
        ### --- BLOCK BEGIN 261
        
        class_var.declare_field("guid", "guid", 0x0, None)
        ### --- BLOCK END 261
    
    
    
    def tag_length():
        ### --- BLOCK BEGIN 262
        return 16
        ### --- BLOCK END 262
    
    
    
    def string():
        ### --- BLOCK BEGIN 263
        return "{" + class_var.guid() + "}"
        ### --- BLOCK END 263
    
    
    
    class_var = VariantTypeNode(param_0, param_1, param_2, param_3, param_4)
    class_var._class_name = 'GuidTypeNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.tag_length = tag_length
    class_var.string = string
    __init__(param_0, param_1, param_2, param_3, param_4)
    return class_var


def SizeTypeNode(param_0, param_1, param_2, param_3, param_4):
    """
    Variant type 0x10.

    Note: Assuming sizeof(size_t) == 0x8.
    """
    def __init__(buf, offset, chunk, parent, length):
        ### --- BLOCK BEGIN 264
        
        if class_var._length == 0x4:
            class_var.declare_field("dword", "num", 0x0)
        elif class_var._length == 0x8:
            class_var.declare_field("qword", "num", 0x0)
        else:
            class_var.declare_field("qword", "num", 0x0)
        ### --- BLOCK END 264
    
    
    
    def tag_length():
        ### --- BLOCK BEGIN 265
        if class_var._length is None:
            return 8
        return class_var._length
        ### --- BLOCK END 265
    
    
    
    def string():
        ### --- BLOCK BEGIN 266
        return str(class_var.num())
        ### --- BLOCK END 266
    
    
    
    class_var = VariantTypeNode(param_0, param_1, param_2, param_3, param_4)
    class_var._class_name = 'SizeTypeNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.tag_length = tag_length
    class_var.string = string
    __init__(param_0, param_1, param_2, param_3, param_4)
    return class_var


def FiletimeTypeNode(param_0, param_1, param_2, param_3, param_4):
    """
    Variant type 0x11.
    """
    def __init__(buf, offset, chunk, parent, length):
        ### --- BLOCK BEGIN 267
        
        class_var.declare_field("filetime", "filetime", 0x0, None)
        ### --- BLOCK END 267
    
    
    
    def string():
        ### --- BLOCK BEGIN 268
        t = class_var.filetime().isoformat(" ")
        return "time not supported"
        ### --- BLOCK END 268
    
    
    
    def tag_length():
        ### --- BLOCK BEGIN 269
        return 8
        ### --- BLOCK END 269
    
    
    
    class_var = VariantTypeNode(param_0, param_1, param_2, param_3, param_4)
    class_var._class_name = 'FiletimeTypeNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.string = string
    class_var.tag_length = tag_length
    __init__(param_0, param_1, param_2, param_3, param_4)
    return class_var


def SystemtimeTypeNode(param_0, param_1, param_2, param_3, param_4):
    """
    Variant type 0x12.
    """
    def __init__(buf, offset, chunk, parent, length):
        ### --- BLOCK BEGIN 270
        
        class_var.declare_field("systemtime", "systemtime", 0x0)
        ### --- BLOCK END 270
    
    
    
    def tag_length():
        ### --- BLOCK BEGIN 271
        return 16
        ### --- BLOCK END 271
    
    
    
    def string():
        ### --- BLOCK BEGIN 272
        t = class_var.systemtime().isoformat(" ")
        return "time not supported"
        ### --- BLOCK END 272
    
    
    
    class_var = VariantTypeNode(param_0, param_1, param_2, param_3, param_4)
    class_var._class_name = 'SystemtimeTypeNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.tag_length = tag_length
    class_var.string = string
    __init__(param_0, param_1, param_2, param_3, param_4)
    return class_var


def SIDTypeNode(param_0, param_1, param_2, param_3, param_4):
    """
    Variant type 0x13.
    """
    def __init__(buf, offset, chunk, parent, length):
        ### --- BLOCK BEGIN 273
        
        class_var.declare_field("byte", "version", 0x0, None)
        class_var.declare_field("byte", "num_elements", None, None)
        class_var.declare_field("dword_be", "id_high", None, None)
        class_var.declare_field("word_be", "id_low", None, None)
        ### --- BLOCK END 273
    
    
    
    def elements():
        ### --- BLOCK BEGIN 274
        ret = []
        _tmp = class_var.num_elements()
        for i in range(_tmp):
            ret.append(class_var.unpack_dword(class_var.current_field_offset() + 4 * i))
        return ret
        ### --- BLOCK END 274
    
    
    
    def id():
        ### --- BLOCK BEGIN 275
        ret = "S-{}-{}".format(class_var.version(), (class_var.id_high() << 16) ^ class_var.id_low())
        for elem in class_var.elements():
            ret += "-{}".format(elem)
        return ret
        ### --- BLOCK END 275
    
    
    
    def tag_length():
        ### --- BLOCK BEGIN 276
        return 8 + 4 * class_var.num_elements()
        ### --- BLOCK END 276
    
    
    
    def string():
        ### --- BLOCK BEGIN 277
        return class_var.id()
        ### --- BLOCK END 277
    
    
    
    class_var = VariantTypeNode(param_0, param_1, param_2, param_3, param_4)
    class_var._class_name = 'SIDTypeNode;' + class_var._class_name
    elements = memoize(elements, class_var)
    
    id = memoize(id, class_var)
    
    class_var.__init__ = __init__
    class_var.elements = elements
    class_var.id = id
    class_var.tag_length = tag_length
    class_var.string = string
    __init__(param_0, param_1, param_2, param_3, param_4)
    return class_var


def Hex32TypeNode(param_0, param_1, param_2, param_3, param_4):
    """
    Variant type 0x14.
    """
    def __init__(buf, offset, chunk, parent, length):
        ### --- BLOCK BEGIN 278
        
        class_var.declare_field("binary", "hex", 0x0, 0x4)
        ### --- BLOCK END 278
    
    
    
    def tag_length():
        ### --- BLOCK BEGIN 279
        return 4
        ### --- BLOCK END 279
    
    
    
    def string():
        ### --- BLOCK BEGIN 280
        ret = "0x"
        b = class_var.hex()[::-1]
        for i in range(len(b)):
            ret += "{:02x}".format(b[i])
        return ret
        ### --- BLOCK END 280
    
    
    
    class_var = VariantTypeNode(param_0, param_1, param_2, param_3, param_4)
    class_var._class_name = 'Hex32TypeNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.tag_length = tag_length
    class_var.string = string
    __init__(param_0, param_1, param_2, param_3, param_4)
    return class_var


def Hex64TypeNode(param_0, param_1, param_2, param_3, param_4):
    """
    Variant type 0x15.
    """
    def __init__(buf, offset, chunk, parent, length):
        ### --- BLOCK BEGIN 281
        
        class_var.declare_field("binary", "hex", 0x0, 0x8)
        ### --- BLOCK END 281
    
    
    
    def tag_length():
        ### --- BLOCK BEGIN 282
        return 8
        ### --- BLOCK END 282
    
    
    
    def string():
        ### --- BLOCK BEGIN 283
        ret = "0x"
        b = class_var.hex()[::-1]
        for i in range(len(b)):
            ret += "{:02x}".format(b[i])
        return ret
        ### --- BLOCK END 283
    
    
    
    class_var = VariantTypeNode(param_0, param_1, param_2, param_3, param_4)
    class_var._class_name = 'Hex64TypeNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.tag_length = tag_length
    class_var.string = string
    __init__(param_0, param_1, param_2, param_3, param_4)
    return class_var


def BXmlTypeNode(param_0, param_1, param_2, param_3, param_4):
    """
    Variant type 0x21.
    """
    def __init__(buf, offset, chunk, parent, length):
        ### --- BLOCK BEGIN 284
        
        class_var._root = RootNode(buf, offset, chunk, class_var)
        ### --- BLOCK END 284
    
    
    
    def tag_length():
        ### --- BLOCK BEGIN 285
        return class_var._length or class_var._root.length()
        ### --- BLOCK END 285
    
    
    
    def string():
        ### --- BLOCK BEGIN 286
        return ""
        ### --- BLOCK END 286
    
    
    
    def root():
        ### --- BLOCK BEGIN 287
        return class_var._root
        ### --- BLOCK END 287
    
    
    
    class_var = VariantTypeNode(param_0, param_1, param_2, param_3, param_4)
    class_var._class_name = 'BXmlTypeNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.tag_length = tag_length
    class_var.string = string
    class_var.root = root
    __init__(param_0, param_1, param_2, param_3, param_4)
    return class_var


def WstringArrayTypeNode(param_0, param_1, param_2, param_3, param_4):
    """
    Variant ttype 0x81.
    """
    def __init__(buf, offset, chunk, parent, length):
        ### --- BLOCK BEGIN 288
        
        if class_var._length is None:
            class_var.declare_field("word", "binary_length", 0x0)
            class_var.declare_field("binary", "binary", length=(class_var.binary_length()))
        else:
            class_var.declare_field("binary", "binary", 0x0, (class_var._length))
        ### --- BLOCK END 288
    
    
    
    def tag_length():
        ### --- BLOCK BEGIN 289
        if class_var._length is None:
            return 2 + class_var.binary_length()
        return class_var._length
        ### --- BLOCK END 289
    
    
    
    def string():
        ### --- BLOCK BEGIN 290
        binary = class_var.binary()
        acc = []
        while len(binary) > 0:
            match = re.search(b"((?:[^\x00].)+)", binary)
            if match:
                frag = match.group()
                acc.append("<string>")
                acc.append(frag.decode("utf16"))
                acc.append("</string>\n")
                binary = binary[len(frag) + 2 :]
                if len(binary) == 0:
                    break
            frag = re.search(b"(\x00*)", binary).group()
            if len(frag) % 2 == 0:
                for _ in range(len(frag) // 2):
                    acc.append("<string></string>\n")
            else:
                raise ParseException("Error parsing uneven substring of NULLs")
            binary = binary[len(frag) :]
        return "".join(acc)
        ### --- BLOCK END 290
    
    
    
    class_var = VariantTypeNode(param_0, param_1, param_2, param_3, param_4)
    class_var._class_name = 'WstringArrayTypeNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.tag_length = tag_length
    class_var.string = string
    __init__(param_0, param_1, param_2, param_3, param_4)
    return class_var


def UnexpectedElementException(param_0):
    def __init__(msg):
        ### --- BLOCK BEGIN 291
        
        pass
        ### --- BLOCK END 291
    
    
    
    class_var = Exception(param_0)
    class_var._class_name = 'UnexpectedElementException;' + class_var._class_name
    class_var.__init__ = __init__
    __init__(param_0)
    return class_var


def escape_attr(s):
    '''
    escape the given string such that it can be placed in an XML attribute, like:

        <foo bar='$value'>

    Args:
      s (str): the string to escape.

    Returns:
      str: the escaped string.
    '''
    ### --- BLOCK BEGIN 292
    RESTRICTED_CHARS = re.compile('[\x01-\x08\x0B\x0C\x0E-\x1F\x7F-\x84\x86-\x9F]')
    esc = xml.sax.saxutils.quoteattr(s)
    esc = esc.encode('ascii', 'xmlcharrefreplace').decode('ascii')
    esc = RESTRICTED_CHARS.sub('', esc)
    return esc
    ### --- BLOCK END 292



def escape_value(s):
    '''
    escape the given string such that it can be placed in an XML value location, like:

        <foo>
          $value
        </foo>

    Args:
      s (str): the string to escape.

    Returns:
      str: the escaped string.
    '''
    ### --- BLOCK BEGIN 293
    RESTRICTED_CHARS = re.compile('[\x01-\x08\x0B\x0C\x0E-\x1F\x7F-\x84\x86-\x9F]')
    esc = xml.sax.saxutils.escape(s)
    esc = esc.encode('ascii', 'xmlcharrefreplace').decode('ascii')
    esc = RESTRICTED_CHARS.sub('', esc)
    return esc
    ### --- BLOCK END 293



def validate_name(s):
    """
    ensure the given name can be used as an XML entity name, such as tag or attribute name.

    Args:
      s (str): the string to validate.

    Raises:
      RuntimeError: if the string is not suitable to be an XML name.
    """
    ### --- BLOCK BEGIN 294
    if not NAME_PATTERN.match(s):
        raise RuntimeError("invalid xml name: %s" % (s))
    return s
    ### --- BLOCK END 294



def render_root_node_with_subs(root_node, subs):
    """
    render the given root node using the given substitutions into XML.

    Args:
      root_node (RootNode): the node to render.
      subs (list[str]): the substitutions that maybe included in the XML.

    Returns:
      str: the rendered XML document.
    """
    def rec(node, acc):
        ### --- BLOCK BEGIN 295
        if user_check_type(node, EndOfStreamNode):
            pass
            # intended
        elif user_check_type(node, OpenStartElementNode):
            acc.append("<")
            acc.append(node.tag_name())
            for child in node.children():
                if user_check_type(child, AttributeNode):
                    acc.append(" ")
                    acc.append(validate_name(child.attribute_name().string()))
                    acc.append('="')
                    # TODO: should use xml.sax.saxutils.quoteattr here
                    # but to do so, we'd need to ensure we're not double-quoting this value.
                    rec(child.attribute_value(), acc)
                    acc.append('"')
            acc.append(">")
            for child in node.children():
                rec(child, acc)
            acc.append("</")
            acc.append(validate_name(node.tag_name()))
            acc.append(">\n")
        elif user_check_type(node, CloseStartElementNode):
            pass
            # intended
        elif user_check_type(node, CloseEmptyElementNode):
            pass
            # intended
        elif user_check_type(node, CloseElementNode):
            pass
            # intended
        elif user_check_type(node, ValueNode):
            acc.append(escape_value(node.children()[0].string()))
        elif user_check_type(node, AttributeNode):
            pass
            # intended
        elif user_check_type(node, CDataSectionNode):
            acc.append("<![CDATA[")
            # TODO: is this correct escaping???
            acc.append(escape_value(node.cdata()))
            acc.append("]]>")
        elif user_check_type(node, EntityReferenceNode):
            acc.append(escape_value(node.entity_reference()))
        elif user_check_type(node, ProcessingInstructionTargetNode):
            acc.append(escape_value(node.processing_instruction_target()))
        elif user_check_type(node, ProcessingInstructionDataNode):
            acc.append(escape_value(node.string()))
        elif user_check_type(node, TemplateInstanceNode):
            raise UnexpectedElementException("TemplateInstanceNode")
        elif user_check_type(node, NormalSubstitutionNode):
            sub = subs[node.index()]
            if user_check_type(sub, BXmlTypeNode):
                sub = render_root_node(sub.root())
            else:
                sub = escape_value(sub.string())
            acc.append(sub)
        elif user_check_type(node, ConditionalSubstitutionNode):
            sub = subs[node.index()]
            if user_check_type(sub, BXmlTypeNode):
                sub = render_root_node(sub.root())
            else:
                sub = escape_value(sub.string())
            acc.append(sub)
        elif user_check_type(node, StreamStartNode):
            pass
            # intended
        ### --- BLOCK END 295
    
    
    
    ### --- BLOCK BEGIN 296
    acc = []
    for c in root_node.template().children():
        rec(c, acc)
    return "".join(acc)
    ### --- BLOCK END 296



def render_root_node(root_node):
    ### --- BLOCK BEGIN 297
    subs = []
    for sub in root_node.substitutions():
        if isinstance(sub, str):
            raise RuntimeError("string sub?")
        if sub is None:
            raise RuntimeError("null sub?")
        subs.append(sub)
    return render_root_node_with_subs(root_node, subs)
    ### --- BLOCK END 297



def evtx_record_xml_view(record, cache):
    """
    render the given record into an XML document.

    Args:
      record (Record): the record to render.

    Returns:
      str: the rendered XML document.
    """
    ### --- BLOCK BEGIN 298
    return render_root_node(record.root())
    ### --- BLOCK END 298



def evtx_chunk_xml_view(chunk):
    """
    Generate XML representations of the records in an EVTX chunk.

    Does not include the XML <?xml... header.
    Records are ordered by chunk.records()

    Args:
      chunk (Chunk): the chunk to render.

    Yields:
      tuple[str, Record]: the rendered XML document and the raw record.
    """
    ### --- BLOCK BEGIN 299
    for record in chunk.records():
        record_str = evtx_record_xml_view(record)
        yield record_str, record
    ### --- BLOCK END 299



def evtx_file_xml_view(file_header):
    """
    Generate XML representations of the records in an EVTX file.

    Does not include the XML <?xml... header.
    Records are ordered by file_header.chunks(), and then by chunk.records()

    Args:
      chunk (FileHeader): the file header to render.

    Yields:
      tuple[str, Record]: the rendered XML document and the raw record.
    """
    ### --- BLOCK BEGIN 300
    for chunk in file_header.chunks():
        for record in chunk.records():
            record_str = evtx_record_xml_view(record)
            yield record_str, record
    ### --- BLOCK END 300



def evtx_template_readable_view(root_node, cache):
    def rec(node, acc):
        ### --- BLOCK BEGIN 301
        if user_check_type(node,
        EndOfStreamNode):
            pass
            # intended
        elif user_check_type(node,
        OpenStartElementNode):
            acc.append("<")
            acc.append(
            node.tag_name())
            for child in node.children():
                if user_check_type(child,
                AttributeNode):
                    acc.append(" ")
                    acc.append(
                    child.attribute_name().string())
                    acc.append('="')
                    rec(child.attribute_value(), acc)
                    acc.append('"')
            acc.append(">")
            for child in node.children():
                rec(child, acc)
            acc.append("</")
            acc.append(
            node.tag_name())
            acc.append(">\n")
        elif user_check_type(node,
        CloseStartElementNode):
            pass
            # intended
        elif user_check_type(node,
        CloseEmptyElementNode):
            pass
            # intended
        elif user_check_type(node,
        CloseElementNode):
            pass
            # intended
        elif user_check_type(node,
        ValueNode):
            acc.append(
            node.children()[0].string())
        elif user_check_type(node,
        AttributeNode):
            pass
            # intended
        elif user_check_type(node,
        CDataSectionNode):
            acc.append("<![CDATA[")
            acc.append(node.cdata())
            acc.append("]]>")
        elif user_check_type(node,
        EntityReferenceNode):
            acc.append(
            node.entity_reference())
        elif user_check_type(node,
        ProcessingInstructionTargetNode):
            acc.append(
            node.processing_instruction_target())
        elif user_check_type(node,
        ProcessingInstructionDataNode):
            acc.append(
            node.string())
        elif user_check_type(node,
        TemplateInstanceNode):
            raise UnexpectedElementException("TemplateInstanceNode")
        elif user_check_type(node,
        NormalSubstitutionNode):
            acc.append("[Normal Substitution(index={}, type={})]".format(
            node.index(), node.type()))
        elif user_check_type(node,
        ConditionalSubstitutionNode):
            acc.append("[Conditional Substitution(index={}, type={})]".format(
            node.index(), node.type()))
        elif user_check_type(node,
        StreamStartNode):
            pass
            # intended
        ### --- BLOCK END 301
    
    
    
    ### --- BLOCK BEGIN 302
    acc = []
    for c in root_node.template().children():
        rec(c, acc)
    return "".join(acc)
    ### --- BLOCK END 302



def InvalidRecordException():
    def __init__():
        ### --- BLOCK BEGIN 303
        
        pass
        ### --- BLOCK END 303
    
    
    
    class_var = ParseException("Invalid record structure")
    class_var._class_name = 'InvalidRecordException;' + class_var._class_name
    class_var.__init__ = __init__
    __init__()
    return class_var


def Evtx(param_0):
    """
    A convenience class that makes it easy to open an
      EVTX file and start iterating the important structures.
    Note, this class must be used in a context statement
       (see the `with` keyword).
    Note, this class will mmap the target file, so ensure
      your platform supports this operation.
    """
    def __init__(filename):
        """
            @type filename:  str
            @param filename: A string that contains the path
              to the EVTX file to open.
            """
        ### --- BLOCK BEGIN 304
        class_var._filename = filename
        class_var._buf = None
        class_var._f = None
        class_var._fh = None
        ### --- BLOCK END 304
    
    
    
    def __enter__():
        ### --- BLOCK BEGIN 305
        class_var._f = open(class_var._filename, "rb")
        class_var._buf = mmap.mmap(class_var._f.fileno(), 0, access=mmap.ACCESS_READ)
        class_var._fh = FileHeader(class_var._buf, 0x0)
        return class_var
        ### --- BLOCK END 305
    
    
    
    def __exit__(type, value, traceback):
        ### --- BLOCK BEGIN 306
        class_var._buf.close()
        class_var._f.close()
        class_var._fh = None
        ### --- BLOCK END 306
    
    
    
    def ensure_contexted(func):
        """
            This decorator ensure that an instance of the
              Evtx class is used within a context statement.  That is,
              that the `with` statement is used, or `__enter__()`
              and `__exit__()` are called explicitly.
            """
        def wrapped(*args):
            kwargs = {}
            ### --- BLOCK BEGIN 307
            if class_var._buf is None:
                raise TypeError("An Evtx object must be used with" " a context (see the `with` statement).")
            else:
                return func(class_var, *args)
            ### --- BLOCK END 307
        
        
        wrapped = wraps(func)(wrapped)
        
        
        ### --- BLOCK BEGIN 308
        return wrapped
        ### --- BLOCK END 308
    
    
    
    def chunks():
        """
            Get each of the ChunkHeaders from within this EVTX file.
    
            @rtype generator of ChunkHeader
            @return A generator of ChunkHeaders from this EVTX file.
            """
        ### --- BLOCK BEGIN 309
        for chunk in class_var._fh.chunks():
            yield chunk
        ### --- BLOCK END 309
    
    
    
    def records():
        """
            Get each of the Records from within this EVTX file.
    
            @rtype generator of Record
            @return A generator of Records from this EVTX file.
            """
        ### --- BLOCK BEGIN 310
        for chunk in class_var.chunks():
            for record in chunk.records():
                yield record
        ### --- BLOCK END 310
    
    
    
    def get_record(record_num):
        """
            Get a Record by record number.
    
            @type record_num:  int
            @param record_num: The record number of the the record to fetch.
            @rtype Record or None
            @return The record request by record number, or None if
              the record is not found.
            """
        ### --- BLOCK BEGIN 311
        return class_var._fh.get_record(record_num)
        ### --- BLOCK END 311
    
    
    
    def get_file_header():
        ### --- BLOCK BEGIN 312
        return class_var._fh
        ### --- BLOCK END 312
    
    
    
    class_var = SkelClass('Evtx')
    chunks = ensure_contexted(chunks, class_var)
    
    records = ensure_contexted(records, class_var)
    
    get_record = ensure_contexted(get_record, class_var)
    
    get_file_header = ensure_contexted(get_file_header, class_var)
    
    class_var.__init__ = __init__
    class_var.__enter__ = __enter__
    class_var.__exit__ = __exit__
    class_var.ensure_contexted = ensure_contexted
    class_var.chunks = chunks
    class_var.records = records
    class_var.get_record = get_record
    class_var.get_file_header = get_file_header
    __init__(param_0)
    return class_var


def FileHeader(param_0, param_1):
    def __init__(buf, offset):
        ### --- BLOCK BEGIN 313
        
        class_var.declare_field("string", "magic", 0x0, 8)
        class_var.declare_field("qword", "oldest_chunk", None, None)
        class_var.declare_field("qword", "current_chunk_number", None, None)
        class_var.declare_field("qword", "next_record_number", None, None)
        class_var.declare_field("dword", "header_size", None, None)
        class_var.declare_field("word", "minor_version", None, None)
        class_var.declare_field("word", "major_version", None, None)
        class_var.declare_field("word", "header_chunk_size", None, None)
        class_var.declare_field("word", "chunk_count", None, None)
        class_var.declare_field("binary", "unused1", None, 0x4C)
        class_var.declare_field("dword", "flags", None, None)
        class_var.declare_field("dword", "checksum", None, None)
        ### --- BLOCK END 313
    
    
    
    def __repr__():
        ### --- BLOCK BEGIN 314
        return "FileHeader(buf={!r}, offset={!r})".format(class_var._buf, class_var._offset)
        ### --- BLOCK END 314
    
    
    
    def __str__():
        ### --- BLOCK BEGIN 315
        return "FileHeader(offset={})".format(hex(class_var._offset))
        ### --- BLOCK END 315
    
    
    
    def check_magic():
        """
            @return A boolean that indicates if the first eight bytes of
              the FileHeader match the expected magic value.
            """
        ### --- BLOCK BEGIN 316
        return class_var.magic() == "ElfFile\x00"
        ### --- BLOCK END 316
    
    
    
    def calculate_checksum():
        """
            @return A integer in the range of an unsigned int that
              is the calculated CRC32 checksum off the first 0x78 bytes.
              This is consistent with the checksum stored by the FileHeader.
            """
        ### --- BLOCK BEGIN 317
        return binascii.crc32(class_var.unpack_binary(0, 0x78)) & 0xFFFFFFFF
        ### --- BLOCK END 317
    
    
    
    def verify():
        """
            @return A boolean that indicates that the FileHeader
              successfully passes a set of heuristic checks that
              all EVTX FileHeaders should pass.
            """
        ### --- BLOCK BEGIN 318
        return (
        class_var.check_magic()
        and class_var.major_version() == 0x3
        and class_var.minor_version() == 0x1
        and class_var.header_chunk_size() == 0x1000
        and class_var.checksum() == class_var.calculate_checksum()
        )
        ### --- BLOCK END 318
    
    
    
    def is_dirty():
        """
            @return A boolean that indicates that the log has been
              opened and was changed, though not all changes might be
              reflected in the file header.
            """
        ### --- BLOCK BEGIN 319
        return class_var.flags() & 0x1 == 0x1
        ### --- BLOCK END 319
    
    
    
    def is_full():
        """
            @return A boolean that indicates that the log
              has reached its maximum configured size and the retention
              policy in effect does not allow to reclaim a suitable amount
              of space from the oldest records and an event message could
              not be written to the log file.
            """
        ### --- BLOCK BEGIN 320
        return class_var.flags() & 0x2 == 0x2
        ### --- BLOCK END 320
    
    
    
    def first_chunk():
        """
            @return A ChunkHeader instance that is the first chunk
              in the log file, which is always found directly after
              the FileHeader.
            """
        ### --- BLOCK BEGIN 321
        ofs = class_var._offset + class_var.header_chunk_size()
        return ChunkHeader(class_var._buf, ofs)
        ### --- BLOCK END 321
    
    
    
    def current_chunk():
        """
            @return A ChunkHeader instance that is the current chunk
              indicated by the FileHeader.
            """
        ### --- BLOCK BEGIN 322
        ofs = class_var._offset + class_var.header_chunk_size()
        ofs += class_var.current_chunk_number() * 0x10000
        return ChunkHeader(class_var._buf, ofs)
        ### --- BLOCK END 322
    
    
    
    def chunks(include_inactive):
        """
            @return A generator that yields the chunks of the log file
              starting with the first chunk, which is always found directly
              after the FileHeader.
    
            If `include_inactive` is set to true, enumerate chunks beyond those
            declared in the file header (and may therefore be corrupt).
            """
        ### --- BLOCK BEGIN 323
        if include_inactive:
            chunk_count = 1000000
        else:
            chunk_count = class_var.chunk_count()
        i = 0
        ofs = class_var._offset + class_var.header_chunk_size()
        while ofs + 0x10000 <= len(class_var._buf) and i < chunk_count:
            yield ChunkHeader(class_var._buf, ofs)
            ofs += 0x10000
            i += 1
        ### --- BLOCK END 323
    
    
    
    def get_record(record_num):
        """
            Get a Record by record number.
    
            @type record_num:  int
            @param record_num: The record number of the the record to fetch.
            @rtype Record or None
            @return The record request by record number, or None if the
              record is not found.
            """
        ### --- BLOCK BEGIN 324
        for chunk in class_var.chunks():
            first_record = chunk.log_first_record_number()
            last_record = chunk.log_last_record_number()
            if not (first_record <= record_num <= last_record):
                continue
            for record in chunk.records():
                if record.record_num() == record_num:
                    return record
        return None
        ### --- BLOCK END 324
    
    
    
    class_var = Block(param_0, param_1)
    class_var._class_name = 'FileHeader;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.__repr__ = __repr__
    class_var.__str__ = __str__
    class_var.check_magic = check_magic
    class_var.calculate_checksum = calculate_checksum
    class_var.verify = verify
    class_var.is_dirty = is_dirty
    class_var.is_full = is_full
    class_var.first_chunk = first_chunk
    class_var.current_chunk = current_chunk
    class_var.chunks = chunks
    class_var.get_record = get_record
    __init__(param_0, param_1)
    return class_var


def Template(param_0):
    def __init__(template_node):
        ### --- BLOCK BEGIN 325
        class_var._template_node = template_node
        class_var._xml = None
        ### --- BLOCK END 325
    
    
    
    def _load_xml():
        """
            TODO(wb): One day, nodes should generate format strings
              instead of the XML format made-up abomination.
            """
        ### --- BLOCK BEGIN 326
        if class_var._xml is not None:
            return
        matcher = r"\[(?:Normal|Conditional) Substitution\(index=(\d+), type=\d+\)\]"
        class_var._xml = re.sub(
        matcher, "{\\1:}", class_var._template_node.template_format().replace("{", "{{").replace("}", "}}")
        )
        ### --- BLOCK END 326
    
    
    
    def make_substitutions(substitutions):
        """
    
            @type substitutions: list of VariantTypeNode
            """
        ### --- BLOCK BEGIN 327
        class_var._load_xml()
        return class_var._xml.format(*[n.xml() for n in substitutions])
        ### --- BLOCK END 327
    
    
    
    def node():
        ### --- BLOCK BEGIN 328
        return class_var._template_node
        ### --- BLOCK END 328
    
    
    
    class_var = SkelClass('Template')
    class_var.__init__ = __init__
    class_var._load_xml = _load_xml
    class_var.make_substitutions = make_substitutions
    class_var.node = node
    __init__(param_0)
    return class_var


def ChunkHeader(param_0, param_1):
    def __init__(buf, offset):
        ### --- BLOCK BEGIN 329
        
        class_var._strings = None
        class_var._templates = None
        class_var.declare_field("string", "magic", 0x0, 8)
        class_var.declare_field("qword", "file_first_record_number", None, None)
        class_var.declare_field("qword", "file_last_record_number", None, None)
        class_var.declare_field("qword", "log_first_record_number", None, None)
        class_var.declare_field("qword", "log_last_record_number", None, None)
        class_var.declare_field("dword", "header_size", None, None)
        class_var.declare_field("dword", "last_record_offset", None, None)
        class_var.declare_field("dword", "next_record_offset", None, None)
        class_var.declare_field("dword", "data_checksum", None, None)
        class_var.declare_field("binary", "unused", None, 0x44)
        class_var.declare_field("dword", "header_checksum", None, None)
        ### --- BLOCK END 329
    
    
    
    def __repr__():
        ### --- BLOCK BEGIN 330
        return "ChunkHeader(buf={!r}, offset={!r})".format(class_var._buf, class_var._offset)
        ### --- BLOCK END 330
    
    
    
    def __str__():
        ### --- BLOCK BEGIN 331
        return "ChunkHeader(offset={})".format(hex(class_var._offset))
        ### --- BLOCK END 331
    
    
    
    def check_magic():
        """
            @return A boolean that indicates if the first eight bytes of
              the ChunkHeader match the expected magic value.
            """
        ### --- BLOCK BEGIN 332
        return class_var.magic() == "ElfChnk\x00"
        ### --- BLOCK END 332
    
    
    
    def calculate_header_checksum():
        """
            @return A integer in the range of an unsigned int that
              is the calculated CRC32 checksum of the ChunkHeader fields.
            """
        ### --- BLOCK BEGIN 333
        data = class_var.unpack_binary(0x0, 0x78)
        data += class_var.unpack_binary(0x80, 0x180)
        return binascii.crc32(data) & 0xFFFFFFFF
        ### --- BLOCK END 333
    
    
    
    def calculate_data_checksum():
        """
            @return A integer in the range of an unsigned int that
              is the calculated CRC32 checksum of the Chunk data.
            """
        ### --- BLOCK BEGIN 334
        data = class_var.unpack_binary(0x200, class_var.next_record_offset() - 0x200)
        return binascii.crc32(data) & 0xFFFFFFFF
        ### --- BLOCK END 334
    
    
    
    def verify():
        """
            @return A boolean that indicates that the FileHeader
              successfully passes a set of heuristic checks that
              all EVTX ChunkHeaders should pass.
            """
        ### --- BLOCK BEGIN 335
        return (
        class_var.check_magic()
        and class_var.calculate_header_checksum() == class_var.header_checksum()
        and class_var.calculate_data_checksum() == class_var.data_checksum()
        )
        ### --- BLOCK END 335
    
    
    
    def _load_strings():
        ### --- BLOCK BEGIN 336
        if class_var._strings is None:
            class_var._strings = {}
        for i in range(64):
            ofs = class_var.unpack_dword(0x80 + (i * 4))
            while ofs > 0:
                string_node = class_var.add_string(ofs, None)
                ofs = string_node.next_offset()
        ### --- BLOCK END 336
    
    
    
    def strings():
        """
            @return A dict(offset --> NameStringNode)
            """
        ### --- BLOCK BEGIN 337
        if not class_var._strings:
            class_var._load_strings()
        return class_var._strings
        ### --- BLOCK END 337
    
    
    
    def add_string(offset, parent):
        """
            @param offset An integer offset that is relative to the start of
              this chunk.
            @param parent (Optional) The parent of the newly created
               NameStringNode instance. (Default: this chunk).
            @return None
            """
        ### --- BLOCK BEGIN 338
        if class_var._strings is None:
            class_var._load_strings()
        string_node = NameStringNode(class_var._buf, class_var._offset + offset, class_var, parent or class_var)
        class_var._strings[offset] = string_node
        return string_node
        ### --- BLOCK END 338
    
    
    
    def _load_templates():
        """
            @return None
            """
        ### --- BLOCK BEGIN 339
        if class_var._templates is None:
            class_var._templates = {}
        for i in range(32):
            ofs = class_var.unpack_dword(0x180 + (i * 4))
            while ofs > 0:
            # unclear why these are found before the offset
            # this is a direct port from A.S.'s code
                token = class_var.unpack_byte(ofs - 10)
                pointer = class_var.unpack_dword(ofs - 4)
                if token != 0x0C or pointer != ofs:
                    ofs = 0
                    continue
                template = class_var.add_template(ofs, None)
                ofs = template.next_offset()
        ### --- BLOCK END 339
    
    
    
    def add_template(offset, parent):
        """
            @param offset An integer which contains the chunk-relative offset
               to a template to load into this Chunk.
            @param parent (Optional) The parent of the newly created
               TemplateNode instance. (Default: this chunk).
            @return Newly added TemplateNode instance.
            """
        ### --- BLOCK BEGIN 340
        if class_var._templates is None:
            class_var._load_templates()
        node = TemplateNode(class_var._buf, class_var._offset + offset, class_var, parent or class_var)
        class_var._templates[offset] = node
        return node
        ### --- BLOCK END 340
    
    
    
    def templates():
        """
            @return A dict(offset --> Template) of all encountered
              templates in this Chunk.
            """
        ### --- BLOCK BEGIN 341
        if not class_var._templates:
            class_var._load_templates()
        return class_var._templates
        ### --- BLOCK END 341
    
    
    
    def first_record():
        ### --- BLOCK BEGIN 342
        return Record(class_var._buf, class_var._offset + 0x200, class_var)
        ### --- BLOCK END 342
    
    
    
    def records():
        ### --- BLOCK BEGIN 343
        try:
            record = class_var.first_record()
        except InvalidRecordException:
            return
        while record._offset < class_var._offset + class_var.next_record_offset() and record.length() > 0:
            yield record
            try:
                record = Record(class_var._buf, record._offset + record.length(), class_var)
            except InvalidRecordException:
                return None
        ### --- BLOCK END 343
    
    
    
    class_var = Block(param_0, param_1)
    class_var._class_name = 'ChunkHeader;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.__repr__ = __repr__
    class_var.__str__ = __str__
    class_var.check_magic = check_magic
    class_var.calculate_header_checksum = calculate_header_checksum
    class_var.calculate_data_checksum = calculate_data_checksum
    class_var.verify = verify
    class_var._load_strings = _load_strings
    class_var.strings = strings
    class_var.add_string = add_string
    class_var._load_templates = _load_templates
    class_var.add_template = add_template
    class_var.templates = templates
    class_var.first_record = first_record
    class_var.records = records
    __init__(param_0, param_1)
    return class_var


def Record(param_0, param_1, param_2):
    def __init__(buf, offset, chunk):
        ### --- BLOCK BEGIN 344
        
        class_var._chunk = chunk
        class_var.declare_field("dword", "magic", 0x0, None)
        # 0x00002a2a
        class_var.declare_field("dword", "size", None, None)
        class_var.declare_field("qword", "record_num", None, None)
        class_var.declare_field("filetime", "timestamp", None, None)
        if class_var.size() > 0x10000:
            return None
        class_var.declare_field("dword", "size2", class_var.size() - 4, None)
        ### --- BLOCK END 344
    
    
    
    def __repr__():
        ### --- BLOCK BEGIN 345
        return "Record(buf={!r}, offset={!r})".format(class_var._buf, class_var._offset)
        ### --- BLOCK END 345
    
    
    
    def __str__():
        ### --- BLOCK BEGIN 346
        return "Record(offset={})".format(hex(class_var._offset))
        ### --- BLOCK END 346
    
    
    
    def root():
        ### --- BLOCK BEGIN 347
        return RootNode(class_var._buf, class_var._offset + 0x18, class_var._chunk, class_var)
        ### --- BLOCK END 347
    
    
    
    def length():
        ### --- BLOCK BEGIN 348
        return class_var.size()
        ### --- BLOCK END 348
    
    
    
    def verify():
        ### --- BLOCK BEGIN 349
        return class_var.size() == class_var.size2()
        ### --- BLOCK END 349
    
    
    
    def data():
        """
            Return the raw data block which makes up this record as a bytestring.
    
            @rtype str
            @return A string that is a copy of the buffer that makes
              up this record.
            """
        ### --- BLOCK BEGIN 350
        return class_var._buf[class_var.offset() : class_var.offset() + class_var.size()]
        ### --- BLOCK END 350
    
    
    
    def xml():
        """
            render the record into XML.
            does not include the xml declaration header.
    
            Returns:
              str: the rendered xml document.
            """
        ### --- BLOCK BEGIN 351
        return evtx_record_xml_view(class_var, None)
        ### --- BLOCK END 351
    
    
    
    class_var = Block(param_0, param_1)
    class_var._class_name = 'Record;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.__repr__ = __repr__
    class_var.__str__ = __str__
    class_var.root = root
    class_var.length = length
    class_var.verify = verify
    class_var.data = data
    class_var.xml = xml
    __init__(param_0, param_1, param_2)
    return class_var


expected_output1 = [
    {"start_file": 1, "end_file": 153, "start_log": 12049, "end_log": 12201},
    {"start_file": 154, "end_file": 336, "start_log": 12202, "end_log": 12384},
    {"start_file": 337, "end_file": 526, "start_log": 12385, "end_log": 12574},
    {"start_file": 527, "end_file": 708, "start_log": 12575, "end_log": 12756},
    {"start_file": 709, "end_file": 882, "start_log": 12757, "end_log": 12930},
    {"start_file": 883, "end_file": 1059, "start_log": 12931, "end_log": 13107},
    {"start_file": 1060, "end_file": 1241, "start_log": 13108, "end_log": 13289},
    {"start_file": 1242, "end_file": 1424, "start_log": 13290, "end_log": 13472},
    {"start_file": 1425, "end_file": 1601, "start_log": 13473, "end_log": 13649}]
expected_output2 = [
    {"start_file": 1, "end_file": 91, "start_log": 1, "end_log": 91},
    {"start_file": 92, "end_file": 177, "start_log": 92, "end_log": 177},
    {"start_file": 178, "end_file": 260, "start_log": 178, "end_log": 260},
    {"start_file": 261, "end_file": 349, "start_log": 261, "end_log": 349},
    {"start_file": 350, "end_file": 441, "start_log": 350, "end_log": 441},
    {"start_file": 442, "end_file": 530, "start_log": 442, "end_log": 530},
    {"start_file": 531, "end_file": 622, "start_log": 531, "end_log": 622},
    {"start_file": 623, "end_file": 711, "start_log": 623, "end_log": 711},
    {"start_file": 712, "end_file": 802, "start_log": 712, "end_log": 802},
    {"start_file": 803, "end_file": 888, "start_log": 803, "end_log": 888},
    {"start_file": 889, "end_file": 976, "start_log": 889, "end_log": 976},
    {"start_file": 977, "end_file": 1063, "start_log": 977, "end_log": 1063},
    {"start_file": 1064, "end_file": 1148, "start_log": 1064, "end_log": 1148},
    {"start_file": 1149, "end_file": 1239, "start_log": 1149, "end_log": 1239},
    {"start_file": 1240, "end_file": 1327, "start_log": 1240, "end_log": 1327},
    {"start_file": 1328, "end_file": 1414, "start_log": 1328, "end_log": 1414},
    {"start_file": 1415, "end_file": 1501, "start_log": 1415, "end_log": 1501},
    {"start_file": 1502, "end_file": 1587, "start_log": 1502, "end_log": 1587},
    {"start_file": 1588, "end_file": 1682, "start_log": 1588, "end_log": 1682},
    {"start_file": 1683, "end_file": 1766, "start_log": 1683, "end_log": 1766},
    {"start_file": 1767, "end_file": 1847, "start_log": 1767, "end_log": 1847},
    {"start_file": 1848, "end_file": 1942, "start_log": 1848, "end_log": 1942},
    {"start_file": 1943, "end_file": 2027, "start_log": 1943, "end_log": 2027},
    {"start_file": 2028, "end_file": 2109, "start_log": 2028, "end_log": 2109},
    {"start_file": 2110, "end_file": 2201, "start_log": 2110, "end_log": 2201},
    {"start_file": 2202, "end_file": 2261, "start_log": 2202, "end_log": 2261}]
expected_output3 = [
   "RootNode", None,
    [["StreamStartNode"],
     ["TemplateInstanceNode", None,
      [["TemplateNode", None,
        [["StreamStartNode"],
         ["OpenStartElementNode", "Event",
          [["AttributeNode", "xmlns",
            [["ValueNode", None,
              [["WstringTypeNode",
                "http://schemas.microsoft.com/win/2004/08/events/event"]]]]],
           ["CloseStartElementNode"],
           ["OpenStartElementNode", "System",
            [["CloseStartElementNode"],
             ["OpenStartElementNode", "Provider",
              [["AttributeNode", "Name",
                [["ValueNode", None,
                  [["WstringTypeNode", "Microsoft-Windows-Eventlog"]]]]],
               ["AttributeNode", "Guid",
                [["ValueNode", None,
                  [["WstringTypeNode",
                    "{fc65ddd8-d6ef-4962-83d5-6e5cfe9ce148}"]]]]],
               ["CloseEmptyElementNode"]]],
             ["OpenStartElementNode", "EventID",
              [["AttributeNode", "Qualifiers",
                [["ConditionalSubstitutionNode"]]],
               ["CloseStartElementNode"],
               ["ConditionalSubstitutionNode"],
               ["CloseElementNode"]]],
             ["OpenStartElementNode", "Version",
              [["CloseStartElementNode"],
               ["ConditionalSubstitutionNode"],
               ["CloseElementNode"]]],
             ["OpenStartElementNode", "Level",
              [["CloseStartElementNode"],
               ["ConditionalSubstitutionNode"],
               ["CloseElementNode"]]],
             ["OpenStartElementNode", "Task",
              [["CloseStartElementNode"],
               ["ConditionalSubstitutionNode"],
               ["CloseElementNode"]]],
             ["OpenStartElementNode", "Opcode",
              [["CloseStartElementNode"],
               ["ConditionalSubstitutionNode"],
               ["CloseElementNode"]]],
             ["OpenStartElementNode", "Keywords",
              [["CloseStartElementNode"],
               ["ConditionalSubstitutionNode"],
               ["CloseElementNode"]]],
             ["OpenStartElementNode", "TimeCreated",
              [["AttributeNode", "SystemTime",
                [["ConditionalSubstitutionNode"]]],
               ["CloseEmptyElementNode"]]],
             ["OpenStartElementNode", "EventRecordID",
              [["CloseStartElementNode"],
               ["ConditionalSubstitutionNode"],
               ["CloseElementNode"]]],
             ["OpenStartElementNode", "Correlation",
              [["AttributeNode", "ActivityID",
                [["ConditionalSubstitutionNode"]]],
               ["AttributeNode", "RelatedActivityID",
                [["ConditionalSubstitutionNode"]]],
               ["CloseEmptyElementNode"]]],
             ["OpenStartElementNode", "Execution",
              [["AttributeNode", "ProcessID",
                [["ConditionalSubstitutionNode"]]],
               ["AttributeNode", "ThreadID",
                [["ConditionalSubstitutionNode"]]],
               ["CloseEmptyElementNode"]]],
             ["OpenStartElementNode", "Channel",
              [["CloseStartElementNode"],
               ["ValueNode", None,
                [["WstringTypeNode", "System"]]],
               ["CloseElementNode"]]],
             ["OpenStartElementNode", "Computer",
              [["CloseStartElementNode"],
               ["ValueNode", None,
                [["WstringTypeNode", "WKS-WIN764BITB.shieldbase.local"]]],
               ["CloseElementNode"]]],
             ["OpenStartElementNode", "Security",
              [["AttributeNode", "UserID",
                [["ConditionalSubstitutionNode"]]],
               ["CloseEmptyElementNode"]]],
             ["CloseElementNode"]]],
           ["OpenStartElementNode", "UserData",
            [["CloseStartElementNode"],
             ["ConditionalSubstitutionNode"],
             ["CloseElementNode"]]],
           ["CloseElementNode"]]],
         ["EndOfStreamNode"]]]]],
     ["Substitutions", None,
      [["UnsignedByteTypeNode", "4"],
       ["UnsignedByteTypeNode", "0"],
       ["UnsignedWordTypeNode", "105"],
       ["UnsignedWordTypeNode", "105"],
       ["NullTypeNode"],
       ["Hex64TypeNode", "0x8000000000000000"],
       ["FiletimeTypeNode", "time not supported"],
       ["NullTypeNode"],
       ["UnsignedDwordTypeNode", "820"],
       ["UnsignedDwordTypeNode", "2868"],
       ["UnsignedQwordTypeNode", "12049"],
       ["UnsignedByteTypeNode", "0"],
       ["NullTypeNode"],
       ["NullTypeNode"],
       ["NullTypeNode"],
       ["NullTypeNode"],
       ["NullTypeNode"],
       ["NullTypeNode"],
       ["NullTypeNode"],
       ["BXmlTypeNode", None,
        [["RootNode", None,
          [["StreamStartNode"],
           ["TemplateInstanceNode", None,
            [["TemplateNode", None,
              [["StreamStartNode"],
               ["OpenStartElementNode", "AutoBackup",
                [["AttributeNode", "xmlns:auto-ns3",
                  [["ValueNode", None,
                    [["WstringTypeNode",
                      "http://schemas.microsoft.com/win/2004/08/events"]]]]],
                 ["AttributeNode", "xmlns",
                  [["ValueNode", None,
                    [["WstringTypeNode",
                      "http://manifests.microsoft.com/win/2004/08/windows/eventlog"]]]]],
                 ["CloseStartElementNode"],
                 ["OpenStartElementNode", "Channel",
                  [["CloseStartElementNode"],
                   ["NormalSubstitutionNode"],
                   ["CloseElementNode"]]],
                 ["OpenStartElementNode", "BackupPath",
                  [["CloseStartElementNode"],
                   ["NormalSubstitutionNode"],
                   ["CloseElementNode"]]],
                 ["CloseElementNode"]]],
               ["EndOfStreamNode"]]]]],
           ["Substitutions", None,
            [["WstringTypeNode", "System"],
             ["WstringTypeNode",
              r"C:\Windows\System32\Winevt\Logs\Archive-System-2012-03-14-04-17-39-932.evtx"]]]]]]]]]]]
expected_output4 = """\
<Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event"><System><Provider Name="Microsoft-Windows-Eventlog" Guid="{fc65ddd8-d6ef-4962-83d5-6e5cfe9ce148}"></Provider>
<EventID Qualifiers="">105</EventID>
<Version>0</Version>
<Level>4</Level>
<Task>105</Task>
<Opcode>0</Opcode>
<Keywords>0x8000000000000000</Keywords>
<TimeCreated SystemTime="time not supported"></TimeCreated>
<EventRecordID>12049</EventRecordID>
<Correlation ActivityID="" RelatedActivityID=""></Correlation>
<Execution ProcessID="820" ThreadID="2868"></Execution>
<Channel>System</Channel>
<Computer>WKS-WIN764BITB.shieldbase.local</Computer>
<Security UserID=""></Security>
</System>
<UserData><AutoBackup xmlns:auto-ns3="http://schemas.microsoft.com/win/2004/08/events" xmlns="http://manifests.microsoft.com/win/2004/08/windows/eventlog"><Channel>System</Channel>
<BackupPath>C:\\Windows\\System32\\Winevt\\Logs\\Archive-System-2012-03-14-04-17-39-932.evtx</BackupPath>
</AutoBackup>
</UserData>
</Event>
"""


def system_path():
    """
    fetch the file system path of the system.evtx test file.

    Returns:
      str: the file system path of the test file.
    """
    cd = os.path.dirname(__file__)
    datadir = os.path.join(cd, "evtx.d")
    systempath = os.path.join(datadir, "system.evtx")
    return systempath


def system():
    """
    yields the contents of the system.evtx test file.
    the returned value is a memory map of the contents,
     so it acts pretty much like a byte string.

    Returns:
      mmap.mmap: the contents of the test file.
    """
    p = system_path()
    with open(p, "rb") as f:
        return f.read()


def security_path():
    """
    fetch the file system path of the security.evtx test file.

    Returns:
      str: the file system path of the test file.
    """
    cd = os.path.dirname(__file__)
    datadir = os.path.join(cd, "evtx.d")
    secpath = os.path.join(datadir, "security.evtx")
    return secpath


def security():
    """
    yields the contents of the security.evtx test file.
    the returned value is a memory map of the contents,
     so it acts pretty much like a byte string.

    Returns:
      mmap.mmap: the contents of the test file.
    """
    p = security_path()
    with open(p, "rb") as f:
        return f.read()


def user_infinite_counter():
    start = 0
    while True:
        yield start
        start += 1


def get_input(case):
    if case == "case1":
        return system()
    else:
        return security()


def test_chunks(input_str):
    """
    regression test parsing some known fields in the file chunks.

    Args:
      system (bytes): the system.evtx test file contents. pytest fixture.
    """
    ### --- BLOCK BEGIN 352
    fh = FileHeader(input_str, 0x0)
    # collected empirically
    expecteds = expected_output1
    for i, chunk in enumerate(fh.chunks(False)):
    # collected empirically
        if i < 9:
            assert chunk.check_magic() is True
            assert chunk.magic() == "ElfChnk\x00"
            assert chunk.calculate_header_checksum() == chunk.header_checksum()
            assert chunk.calculate_data_checksum() == chunk.data_checksum()
            expected = expecteds[i]
            assert chunk.file_first_record_number() == expected["start_file"]
            assert chunk.file_last_record_number() == expected["end_file"]
            assert chunk.log_first_record_number() == expected["start_log"]
            assert chunk.log_last_record_number() == expected["end_log"]
        else:
            assert chunk.check_magic() is False
            assert chunk.magic() == EMPTY_MAGIC
    ### --- BLOCK END 352



def test_chunks2(input_str):
    """
    regression test parsing some known fields in the file chunks.

    Args:
      security (bytes): the security.evtx test file contents. pytest fixture.
    """
    ### --- BLOCK BEGIN 353
    fh = FileHeader(input_str, 0x0)
    # collected empirically
    expecteds = expected_output2
    for i, chunk in enumerate(fh.chunks(False)):
    # collected empirically
        if i < 26:
            assert chunk.check_magic() is True
            assert chunk.magic() == "ElfChnk\x00"
            assert chunk.calculate_header_checksum() == chunk.header_checksum()
            assert chunk.calculate_data_checksum() == chunk.data_checksum()
            expected = expecteds[i]
            assert chunk.file_first_record_number() == expected["start_file"]
            assert chunk.file_last_record_number() == expected["end_file"]
            assert chunk.log_first_record_number() == expected["start_log"]
            assert chunk.log_last_record_number() == expected["end_log"]
        else:
            assert chunk.check_magic() is False
            assert chunk.magic() == EMPTY_MAGIC
    ### --- BLOCK END 353



def test_file_header(input_str):
    """
    regression test parsing some known fields in the file header.

    Args:
      system (bytes): the system.evtx test file contents. pytest fixture.
    """
    ### --- BLOCK BEGIN 354
    fh = FileHeader(input_str, 0x0)
    # collected empirically
    assert fh.magic() == "ElfFile\x00"
    assert fh.major_version() == 0x3
    assert fh.minor_version() == 0x1
    assert fh.flags() == 0x1
    assert fh.is_dirty() is True
    assert fh.is_full() is False
    assert fh.current_chunk_number() == 0x8
    assert fh.chunk_count() == 0x9
    assert fh.oldest_chunk() == 0x0
    assert fh.next_record_number() == 0x34D8
    assert fh.checksum() == 0x41B4B1EC
    assert fh.calculate_checksum() == fh.checksum()
    ### --- BLOCK END 354



def test_file_header2(input_str):
    """
    regression test parsing some known fields in the file header.

    Args:
      security (bytes): the security.evtx test file contents. pytest fixture.
    """
    ### --- BLOCK BEGIN 355
    fh = FileHeader(input_str, 0x0)
    # collected empirically
    assert fh.magic() == "ElfFile\x00"
    assert fh.major_version() == 0x3
    assert fh.minor_version() == 0x1
    assert fh.flags() == 0x1
    assert fh.is_dirty() is True
    assert fh.is_full() is False
    assert fh.current_chunk_number() == 0x19
    assert fh.chunk_count() == 0x1A
    assert fh.oldest_chunk() == 0x0
    assert fh.next_record_number() == 0x8B2
    assert fh.checksum() == 0x3F6E33D5
    assert fh.calculate_checksum() == fh.checksum()
    ### --- BLOCK END 355



def one(iterable):
    """
    fetch a single element from the given iterable.

    Args:
      iterable (iterable): a sequence of things.

    Returns:
      object: the first thing in the sequence.
    """
    ### --- BLOCK BEGIN 356
    for i in iterable:
        return i
    ### --- BLOCK END 356



def extract_structure(node):
    """
    given an evtx bxml node, generate a tree of all the nodes.
    each node has:
      - str: node type
      - str: (optional) value
      - list: (optional) children

    Args:
      node (Node): the root node.

    Returns:
      list: the tree representing the bxml structure.
    """
    ### --- BLOCK BEGIN 357
    name = node._class_name.split(';')[0]
    if user_check_type(node, BXmlTypeNode):
        value = None
    elif user_check_type(node, VariantTypeNode):
        value = node.string()
    elif user_check_type(node, OpenStartElementNode):
        value = node.tag_name()
    elif user_check_type(node, AttributeNode):
        value = node.attribute_name().string()
    else:
        value = None
    children = []
    if user_check_type(node, BXmlTypeNode):
        children.append(extract_structure(node._root))
    elif user_check_type(node, TemplateInstanceNode) and node.is_resident_template():
        children.append(extract_structure(node.template()))
    children.extend(list(map(extract_structure, node.children())))
    if user_check_type(node, RootNode):
        substitutions = list(map(extract_structure, node.substitutions()))
        children.append(["Substitutions", None, substitutions])
    if children:
        return [name, value, children]
    elif value:
        return [name, value]
    else:
        return [name]
    ### --- BLOCK END 357



def test_parse_record(input_str):
    """
    regression test demonstrating binary xml nodes getting parsed.

    Args:
      system (bytes): the system.evtx test file contents. pytest fixture.
    """
    ### --- BLOCK BEGIN 358
    fh = FileHeader(input_str, 0x0)
    chunk = next(fh.chunks(False))
    record = next(chunk.records())
    # generated by hand, but matches the output of extract_structure.
    expected = expected_output3
    assert extract_structure(record.root()) == expected
    ### --- BLOCK END 358



def test_render_record(input_str):
    """
    regression test demonstrating formatting a record to xml.

    Args:
      system (bytes): the system.evtx test file contents. pytest fixture.
    """
    ### --- BLOCK BEGIN 359
    fh = FileHeader(input_str, 0x0)
    chunk = next(fh.chunks(False))
    record = next(chunk.records())
    xml = record.xml()
    assert xml == expected_output4
    ### --- BLOCK END 359



def test_parse_records(input_str):
    """
    regression test demonstrating that all record metadata can be parsed.

    Args:
      system (bytes): the system.evtx test file contents. pytest fixture.
    """
    ### --- BLOCK BEGIN 360
    fh = FileHeader(input_str, 0x0)
    for i, chunk in enumerate(fh.chunks(False)):
        for j, record in enumerate(chunk.records()):
            assert record.magic() == 0x2A2A
    ### --- BLOCK END 360



def test_parse_records2(input_str):
    """
    regression test demonstrating that all record metadata can be parsed.

    Args:
      security (bytes): the security.evtx test file contents. pytest fixture.
    """
    ### --- BLOCK BEGIN 361
    fh = FileHeader(input_str, 0x0)
    for i, chunk in enumerate(fh.chunks(False)):
        for j, record in enumerate(chunk.records()):
            assert record.magic() == 0x2A2A
    ### --- BLOCK END 361



def test_render_records(input_str):
    """
    regression test demonstrating formatting records to xml.

    Args:
      system (bytes): the system.evtx test file contents. pytest fixture.
    """
    ### --- BLOCK BEGIN 362
    fh = FileHeader(input_str, 0x0)
    for chunk in fh.chunks(False):
        for record in chunk.records():
            assert record.xml() is not None
    ### --- BLOCK END 362



def test_render_records2(input_str):
    """
    regression test demonstrating formatting records to xml.

    Args:
      security (bytes): the security.evtx test file contents. pytest fixture.
    """
    ### --- BLOCK BEGIN 363
    fh = FileHeader(input_str, 0x0)
    for chunk in fh.chunks(False):
        for record in chunk.records():
            assert record.xml() is not None
    ### --- BLOCK END 363



def test_render_records_lxml(input_str):
    """
    regression test demonstrating formatting records to xml.

    Args:
      system (bytes): the system.evtx test file contents. pytest fixture.
    """
    ### --- BLOCK BEGIN 364
    pass
    ### --- BLOCK END 364



def test_render_records_lxml2(input_str):
    """
    regression test demonstrating formatting records to xml.

    Args:
      security (bytes): the security.evtx test file contents. pytest fixture.
    """
    ### --- BLOCK BEGIN 365
    pass
    ### --- BLOCK END 365



### seperation test begin

def test_corrupt_ascii_example():
    """
    regression test demonstrating issue 37.

    Args:
      data_path (str): the file system path of the test directory.
    """
    # record number two contains a QNAME xml element
    # with an ASCII text value that is invalid ASCII:
    #
    #     000002E0:                                31 39 33 2E 31 2E            193.1.
    #     000002F0: 33 36 2E 31 32 31 30 2E  39 2E 31 35 2E 32 30 32  36.1210.9.15.202
    #     00000300: 01 62 2E 5F 64 6E 73 2D  73 64 2E 5F 75 64 70 2E  .b._dns-sd._udp.
    #     00000310: 40 A6 35 01 2E                                    @.5..
    #                  ^^ ^^ ^^
    #
    # with pytest.raises(UnicodeDecodeError):
    ### --- BLOCK BEGIN 366
    pass
    ### --- BLOCK END 366



def test_continue_parsing_after_corrupt_ascii():
    """
    regression test demonstrating issue 37.

    Args:
      data_path (str): the file system path of the test directory.
    """
    ### --- BLOCK BEGIN 367
    pass
    ### --- BLOCK END 367



def test():
    ### --- BLOCK BEGIN 368
    test_chunks(get_input("case1"))
    test_chunks2(get_input("case2"))
    test_file_header(get_input("case1"))
    test_file_header2(get_input("case2"))
    test_parse_record(get_input("case1"))
    test_parse_records(get_input("case1"))
    test_parse_records2(get_input("case2"))
    test_render_record(get_input("case1"))
    test_render_records(get_input("case1"))
    test_render_records2(get_input("case2"))
    print("All tests passed")
    ### --- BLOCK END 368



## Preprocessing:

# We remove 2 tests due to the lack of corresponding libraries ("mmap", "lxml") in JS.

# We adjust 1 test becuase the translation of `time.isoformat(" ")` in JS will lose the precision of the date.

# These two tests are not related to the main functionality of the program.

### Global Begin

### --- BLOCK BEGIN 0
EMPTY_MAGIC = "\x00" * 0x8

XML_HEADER = '<?xml version="1.1" encoding="utf-8" standalone="yes" ?>\n'

node_dispatch_table = [
    EndOfStreamNode,
    OpenStartElementNode,
    CloseStartElementNode,
    CloseEmptyElementNode,
    CloseElementNode,
    ValueNode,
    AttributeNode,
    CDataSectionNode,
    CharacterReferenceNode,
    EntityReferenceNode,
    ProcessingInstructionTargetNode,
    ProcessingInstructionDataNode,
    TemplateInstanceNode,
    NormalSubstitutionNode,
    ConditionalSubstitutionNode,
    StreamStartNode,
]

node_readable_tokens = [
    "End of Stream",
    "Open Start Element",
    "Close Start Element",
    "Close Empty Element",
    "Close Element",
    "Value",
    "Attribute",
    "unknown",
    "unknown",
    "unknown",
    "unknown",
    "unknown",
    "TemplateInstanceNode",
    "Normal Substitution",
    "Conditional Substitution",
    "Start of Stream",
]

test()

### --- BLOCK END 0
