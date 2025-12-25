import base64
import binascii
import datetime
import re
import os
import os.path
import struct
import xml.sax.saxutils
NAME_PATTERN = re.compile(r"[a-zA-Z_][a-zA-Z_\-]*")
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
def user_check_type(obj, _type):
    if "function" in str(_type):
        for i in obj._class_name.split(";"):
            if i == str(_type).split(" ")[1]:
                return True
        return False
def SkelClass(class_name):
    Clz = type(class_name, (), {'_class_name': class_name})
    return Clz()
def memoize(param_0, decorated_object=None):
    def __init__(func):
        class_var.func = func
    def __call__(*args):
        kw = {}
        obj = args[0]
        try:
            cache = obj.__cache
        except AttributeError:
            cache = obj.__cache = {}
        key = (class_var.func, args, frozenset(list(kw.items())))
        if key not in cache:
            cache[key] = class_var.func(*args)
        return cache[key]
    class_var = SkelClass('memoize')
    tmp_f = param_0
    def self_func(*args):
        return tmp_f(*args[1:])
    param_0 = self_func
    class_var.__init__ = __init__
    class_var.__call__ = __call__
    __init__(param_0)
    def self_call(*args):
        return __call__(decorated_object, *args)
    return self_call
def parse_filetime(qword):
    if qword == 0:
        return datetime.datetime.min
    try:
        return datetime.datetime.fromtimestamp(float(qword) * 1e-7 - 11644473600, datetime.timezone.utc)
    except (ValueError, OSError):
        return datetime.datetime.min
def BinaryParserException(param_0):
    def __init__(value):
        class_var._value = value
    class_var = Exception()
    class_var._class_name = 'BinaryParserException;' + class_var._class_name
    class_var.__init__ = __init__
    __init__(param_0)
    return class_var
def ParseException(param_0):
    def __init__(value):
        pass
    class_var = BinaryParserException(param_0)
    class_var._class_name = 'ParseException;' + class_var._class_name
    class_var.__init__ = __init__
    __init__(param_0)
    return class_var
def OverrunBufferException(param_0, param_1):
    def __init__(readOffs, bufLen):
        tvalue = "read: {}, buffer length: {}".format(hex(readOffs), hex(bufLen))
    class_var = ParseException('Error: Type not support')
    class_var._class_name = 'OverrunBufferException;' + class_var._class_name
    class_var.__init__ = __init__
    __init__(param_0, param_1)
    return class_var
def Block(param_0, param_1):
    def __init__(buf, offset):
        class_var._buf = buf
        class_var._offset = offset
        class_var._implicit_offset = 0
    def declare_field(type, name, offset=None, length=None):
        def no_length_handler():
            f = getattr(class_var, "unpack_" + type)
            return f(offset)
        def explicit_length_handler():
            f = getattr(class_var, "unpack_" + type)
            return f(offset, length)
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
    def current_field_offset():
        return class_var._implicit_offset
    def unpack_byte(offset):
        o = class_var._offset + offset
        try:
            return struct.unpack_from("<B", class_var._buf, o)[0]
        except struct.error:
            raise OverrunBufferException(o, len(class_var._buf))
    def unpack_word(offset):
        o = class_var._offset + offset
        try:
            return struct.unpack_from("<H", class_var._buf, o)[0]
        except struct.error:
            raise OverrunBufferException(o, len(class_var._buf))
    def unpack_word_be(offset):
        o = class_var._offset + offset
        try:
            return struct.unpack_from(">H", class_var._buf, o)[0]
        except struct.error:
            raise OverrunBufferException(o, len(class_var._buf))
    def unpack_dword(offset):
        o = class_var._offset + offset
        try:
            return struct.unpack_from("<I", class_var._buf, o)[0]
        except struct.error:
            raise OverrunBufferException(o, len(class_var._buf))
    def unpack_dword_be(offset):
        o = class_var._offset + offset
        try:
            return struct.unpack_from(">I", class_var._buf, o)[0]
        except struct.error:
            raise OverrunBufferException(o, len(class_var._buf))
    def unpack_int32(offset):
        o = class_var._offset + offset
        try:
            return struct.unpack_from("<i", class_var._buf, o)[0]
        except struct.error:
            raise OverrunBufferException(o, len(class_var._buf))
    def unpack_qword(offset):
        o = class_var._offset + offset
        try:
            return struct.unpack_from("<Q", class_var._buf, o)[0]
        except struct.error:
            raise OverrunBufferException(o, len(class_var._buf))
    def unpack_binary(offset, length):
        if not length:
            return ("".encode("ascii"))
        o = class_var._offset + offset
        try:
            return (struct.unpack_from("<{}s".format(length), class_var._buf, o)[0])
        except struct.error:
            raise OverrunBufferException(o, len(class_var._buf))
    def unpack_string(offset, length):
        return class_var.unpack_binary(offset, length).decode("ascii")
    def unpack_wstring(offset, length):
        start = class_var._offset + offset
        end = class_var._offset + offset + 2 * length
        try:
            return bytes(class_var._buf[start:end]).decode("utf16")
        except AttributeError:
            return bytes(class_var._buf[start:end]).decode("utf16")
    def unpack_filetime(offset):
        return parse_filetime(class_var.unpack_qword(offset))
    def unpack_guid(offset):
        o = class_var._offset + offset
        try:
            _bin = bytes(class_var._buf[o:o + 16])
        except IndexError:
            raise OverrunBufferException(o, len(class_var._buf))
        h = [_bin[i] for i in range(len(_bin))]
        return """{:02x}{:02x}{:02x}{:02x}-{:02x}{:02x}-{:02x}{:02x}-{:02x}{:02x}-{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}""".format(h[3], h[2], h[1], h[0], h[5], h[4], h[7], h[6], h[8], h[9], h[10], h[11], h[12], h[13], h[14], h[15])
    def offset():
        return class_var._offset
    class_var = SkelClass('Block')
    class_var.__init__ = __init__
    class_var.declare_field = declare_field
    class_var.current_field_offset = current_field_offset
    class_var.unpack_byte = unpack_byte
    class_var.unpack_word = unpack_word
    class_var.unpack_word_be = unpack_word_be
    class_var.unpack_dword = unpack_dword
    class_var.unpack_dword_be = unpack_dword_be
    class_var.unpack_int32 = unpack_int32
    class_var.unpack_qword = unpack_qword
    class_var.unpack_binary = unpack_binary
    class_var.unpack_string = unpack_string
    class_var.unpack_wstring = unpack_wstring
    class_var.unpack_filetime = unpack_filetime
    class_var.unpack_guid = unpack_guid
    class_var.offset = offset
    __init__(param_0, param_1)
    return class_var
def BXmlNode(param_0, param_1, param_2, param_3):
    def __init__(buf, offset, chunk, parent):
        class_var._chunk = chunk
        class_var._parent = parent
    def _children(max_children, end_tokens):
        ret = []
        ofs = class_var.tag_length()
        if max_children:
            gen = list(range(max_children))
        else:
            gen = user_infinite_counter()
        for _ in gen:
            token = class_var.unpack_byte(ofs) & 0x0F
            try:
                HandlerNodeClass = node_dispatch_table[token]
                child = HandlerNodeClass(class_var._buf, class_var.offset() + ofs, class_var._chunk, class_var)
            except IndexError:
                raise ParseException("Unexpected token {:02X} at {}".format(token, class_var.offset() + ofs))
            ret.append(child)
            ofs += child.length()
            if token in end_tokens:
                break
            if child.find_end_of_stream():
                break
        return ret
    def children():
        return class_var._children(None, [EndOfStreamToken])
    def length():
        ret = class_var.tag_length()
        for child in class_var.children():
            ret += child.length()
        return ret
    def find_end_of_stream():
        for child in class_var.children():
            if user_check_type(child, EndOfStreamNode):
                return child
            ret = child.find_end_of_stream()
            if ret:
                return ret
        return None
    class_var = Block(param_0, param_1)
    class_var._class_name = 'BXmlNode;' + class_var._class_name
    children = memoize(children, class_var)
    length = memoize(length, class_var)
    find_end_of_stream = memoize(find_end_of_stream, class_var)
    class_var.__init__ = __init__
    class_var._children = _children
    class_var.children = children
    class_var.length = length
    class_var.find_end_of_stream = find_end_of_stream
    __init__(param_0, param_1, param_2, param_3)
    return class_var
def NameStringNode(param_0, param_1, param_2, param_3):
    def __init__(buf, offset, chunk, parent):
        class_var.declare_field("dword", "next_offset", 0x0, None)
        class_var.declare_field("word", "hash", None, None)
        class_var.declare_field("word", "string_length", None, None)
        class_var.declare_field("wstring", "string", length=class_var.string_length())
    def tag_length():
        return (class_var.string_length() * 2) + 8
    def length():
        return class_var.tag_length() + 2
    class_var = BXmlNode(param_0, param_1, param_2, param_3)
    class_var._class_name = 'NameStringNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.tag_length = tag_length
    class_var.length = length
    __init__(param_0, param_1, param_2, param_3)
    return class_var
def TemplateNode(param_0, param_1, param_2, param_3):
    def __init__(buf, offset, chunk, parent):
        class_var.declare_field("dword", "next_offset", 0x0, None)
        class_var.declare_field("dword", "template_id", None, None)
        class_var.declare_field("guid", "guid", 0x04, None)
        class_var.declare_field("dword", "data_length", None, None)
    def tag_length():
        return 0x18
    def length():
        return class_var.tag_length() + class_var.data_length()
    class_var = BXmlNode(param_0, param_1, param_2, param_3)
    class_var._class_name = 'TemplateNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.tag_length = tag_length
    class_var.length = length
    __init__(param_0, param_1, param_2, param_3)
    return class_var
def EndOfStreamNode(param_0, param_1, param_2, param_3):
    def __init__(buf, offset, chunk, parent):
        pass
    def length():
        return 1
    def children():
        return []
    class_var = BXmlNode(param_0, param_1, param_2, param_3)
    class_var._class_name = 'EndOfStreamNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.length = length
    class_var.children = children
    __init__(param_0, param_1, param_2, param_3)
    return class_var
def OpenStartElementNode(param_0, param_1, param_2, param_3):
    def __init__(buf, offset, chunk, parent):
        class_var.declare_field("byte", "token", 0x0, None)
        class_var.declare_field("word", "unknown0", None, None)
        class_var.declare_field("dword", "size", None, None)
        class_var.declare_field("dword", "string_offset", None, None)
        class_var._tag_length = 11
        class_var._element_type = 0
        if class_var.flags() & 0x04:
            class_var._tag_length += 4
        if class_var.string_offset() > class_var.offset() - class_var._chunk._offset:
            new_string = class_var._chunk.add_string(class_var.string_offset(), parent=class_var)
            class_var._tag_length += new_string.length()
    def flags():
        return class_var.token() >> 4
    def tag_name():
        return class_var._chunk.strings()[class_var.string_offset()].string()
    def tag_length():
        return class_var._tag_length
    def children():
        return class_var._children(None, [CloseElementToken, CloseEmptyElementToken])
    class_var = BXmlNode(param_0, param_1, param_2, param_3)
    class_var._class_name = 'OpenStartElementNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.flags = flags
    class_var.tag_name = memoize(tag_name, class_var)
    class_var.tag_length = tag_length
    class_var.children = memoize(children, class_var)
    __init__(param_0, param_1, param_2, param_3)
    return class_var
def CloseStartElementNode(param_0, param_1, param_2, param_3):
    def __init__(buf, offset, chunk, parent):
        class_var.declare_field("byte", "token", 0x0, None)
    def length():
        return 1
    def children():
        return []
    class_var = BXmlNode(param_0, param_1, param_2, param_3)
    class_var._class_name = 'CloseStartElementNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.length = length
    class_var.children = children
    __init__(param_0, param_1, param_2, param_3)
    return class_var
def CloseEmptyElementNode(param_0, param_1, param_2, param_3):
    def __init__(buf, offset, chunk, parent):
        class_var.declare_field("byte", "token", 0x0, None)
    def length():
        return 1
    def children():
        return []
    class_var = BXmlNode(param_0, param_1, param_2, param_3)
    class_var._class_name = 'CloseEmptyElementNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.length = length
    class_var.children = children
    __init__(param_0, param_1, param_2, param_3)
    return class_var
def CloseElementNode(param_0, param_1, param_2, param_3):
    def __init__(buf, offset, chunk, parent):
        class_var.declare_field("byte", "token", 0x0, None)
    def length():
        return 1
    def children():
        return []
    class_var = BXmlNode(param_0, param_1, param_2, param_3)
    class_var._class_name = 'CloseElementNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.length = length
    class_var.children = children
    __init__(param_0, param_1, param_2, param_3)
    return class_var
def get_variant_value(buf, offset, chunk, parent, type_, length=None):
    TypeClass = {NULL: NullTypeNode, WSTRING: WstringTypeNode, UNSIGNED_BYTE: UnsignedByteTypeNode, UNSIGNED_WORD: UnsignedWordTypeNode, UNSIGNED_DWORD: UnsignedDwordTypeNode, UNSIGNED_QWORD: UnsignedQwordTypeNode, FLOAT: FloatTypeNode, DOUBLE: DoubleTypeNode, BOOLEAN: BooleanTypeNode, BINARY: BinaryTypeNode, GUID: GuidTypeNode, SIZE: SizeTypeNode, FILETIME: FiletimeTypeNode, SYSTEMTIME: SystemtimeTypeNode, SID: SIDTypeNode, HEX32: Hex32TypeNode, HEX64: Hex64TypeNode, BXML: BXmlTypeNode, WSTRINGARRAY: WstringArrayTypeNode}[type_]
    return TypeClass(buf, offset, chunk, parent, length)
def ValueNode(param_0, param_1, param_2, param_3):
    def __init__(buf, offset, chunk, parent):
        class_var.declare_field("byte", "token", 0x0, None)
        class_var.declare_field("byte", "type", None, None)
    def tag_length():
        return 2
    def children():
        child = get_variant_value(class_var._buf, class_var.offset() + class_var.tag_length(), class_var._chunk, class_var, class_var.type())
        return [child]
    class_var = BXmlNode(param_0, param_1, param_2, param_3)
    class_var._class_name = 'ValueNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.tag_length = tag_length
    class_var.children = children
    __init__(param_0, param_1, param_2, param_3)
    return class_var
def AttributeNode(param_0, param_1, param_2, param_3):
    def __init__(buf, offset, chunk, parent):
        class_var.declare_field("byte", "token", 0x0, None)
        class_var.declare_field("dword", "string_offset", None, None)
        class_var._name_string_length = 0
        if class_var.string_offset() > class_var.offset() - class_var._chunk._offset:
            new_string = class_var._chunk.add_string(class_var.string_offset(), parent=class_var)
            class_var._name_string_length += new_string.length()
    def attribute_name():
        return class_var._chunk.strings()[class_var.string_offset()]
    def attribute_value():
        return class_var.children()[0]
    def tag_length():
        return 5 + class_var._name_string_length
    def children():
        return class_var._children(1, [EndOfStreamToken])
    class_var = BXmlNode(param_0, param_1, param_2, param_3)
    class_var._class_name = 'AttributeNode;' + class_var._class_name
    children = memoize(children, class_var)
    class_var.__init__ = __init__
    class_var.attribute_name = attribute_name
    class_var.attribute_value = attribute_value
    class_var.tag_length = tag_length
    class_var.children = children
    __init__(param_0, param_1, param_2, param_3)
    return class_var
def CharacterReferenceNode(param_0, param_1, param_2, param_3):
    def __init__(buf, offset, chunk, parent):
        class_var.declare_field("byte", "token", 0x0)
        class_var.declare_field("word", "entity")
        class_var._tag_length = 3
    def entity_reference():
        return "&#x%04x;" % (class_var.entity())
    def flags():
        return class_var.token() >> 4
    def tag_length():
        return class_var._tag_length
    def children():
        return []
    class_var = BXmlNode(param_0, param_1, param_2, param_3)
    class_var._class_name = 'CharacterReferenceNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.entity_reference = entity_reference
    class_var.flags = flags
    class_var.tag_length = tag_length
    class_var.children = children
    __init__(param_0, param_1, param_2, param_3)
    return class_var
def EntityReferenceNode(param_0, param_1, param_2, param_3):
    def __init__(buf, offset, chunk, parent):
        class_var.declare_field("byte", "token", 0x0)
        class_var.declare_field("dword", "string_offset")
        class_var._tag_length = 5
        if class_var.string_offset() > class_var.offset() - class_var._chunk.offset():
            new_string = class_var._chunk.add_string(class_var.string_offset(), parent=class_var)
            class_var._tag_length += new_string.length()
    def entity_reference():
        return "&{};".format(class_var._chunk.strings()[class_var.string_offset()].string())
    def flags():
        return class_var.token() >> 4
    def tag_length():
        return class_var._tag_length
    def children():
        return []
    class_var = BXmlNode(param_0, param_1, param_2, param_3)
    class_var._class_name = 'EntityReferenceNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.entity_reference = entity_reference
    class_var.flags = flags
    class_var.tag_length = tag_length
    class_var.children = children
    __init__(param_0, param_1, param_2, param_3)
    return class_var
def TemplateInstanceNode(param_0, param_1, param_2, param_3):
    def __init__(buf, offset, chunk, parent):
        class_var.declare_field("byte", "token", 0x0, None)
        class_var.declare_field("byte", "unknown0", None, None)
        class_var.declare_field("dword", "template_id", None, None)
        class_var.declare_field("dword", "template_offset", None, None)
        class_var._data_length = 0
        if class_var.is_resident_template():
            new_template = class_var._chunk.add_template(class_var.template_offset(), parent=class_var)
            class_var._data_length += new_template.length()
    def is_resident_template():
        return class_var.template_offset() > class_var.offset() - class_var._chunk._offset
    def tag_length():
        return 10
    def length():
        return class_var.tag_length() + class_var._data_length
    def template():
        return class_var._chunk.templates()[class_var.template_offset()]
    def children():
        return []
    def find_end_of_stream():
        return class_var.template().find_end_of_stream()
    class_var = BXmlNode(param_0, param_1, param_2, param_3)
    class_var._class_name = 'TemplateInstanceNode;' + class_var._class_name
    find_end_of_stream = memoize(find_end_of_stream, class_var)
    class_var.__init__ = __init__
    class_var.is_resident_template = is_resident_template
    class_var.tag_length = tag_length
    class_var.length = length
    class_var.template = template
    class_var.children = children
    class_var.find_end_of_stream = find_end_of_stream
    __init__(param_0, param_1, param_2, param_3)
    return class_var
def NormalSubstitutionNode(param_0, param_1, param_2, param_3):
    def __init__(buf, offset, chunk, parent):
        class_var.declare_field("byte", "token", 0x0, None)
        class_var.declare_field("word", "index", None, None)
        class_var.declare_field("byte", "type", None, None)
    def tag_length():
        return 0x4
    def length():
        return class_var.tag_length()
    def children():
        return []
    class_var = BXmlNode(param_0, param_1, param_2, param_3)
    class_var._class_name = 'NormalSubstitutionNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.tag_length = tag_length
    class_var.length = length
    class_var.children = children
    __init__(param_0, param_1, param_2, param_3)
    return class_var
def ConditionalSubstitutionNode(param_0, param_1, param_2, param_3):
    def __init__(buf, offset, chunk, parent):
        class_var.declare_field("byte", "token", 0x0, None)
        class_var.declare_field("word", "index", None, None)
        class_var.declare_field("byte", "type", None, None)
    def tag_length():
        return 0x4
    def length():
        return class_var.tag_length()
    def children():
        return []
    class_var = BXmlNode(param_0, param_1, param_2, param_3)
    class_var._class_name = 'ConditionalSubstitutionNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.tag_length = tag_length
    class_var.length = length
    class_var.children = children
    __init__(param_0, param_1, param_2, param_3)
    return class_var
def StreamStartNode(param_0, param_1, param_2, param_3):
    def __init__(buf, offset, chunk, parent):
        class_var.declare_field("byte", "token", 0x0, None)
        class_var.declare_field("byte", "unknown0", None, None)
        class_var.declare_field("word", "unknown1", None, None)
    def tag_length():
        return 4
    def length():
        return class_var.tag_length() + 0
    def children():
        return []
    class_var = BXmlNode(param_0, param_1, param_2, param_3)
    class_var._class_name = 'StreamStartNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.tag_length = tag_length
    class_var.length = length
    class_var.children = children
    __init__(param_0, param_1, param_2, param_3)
    return class_var
def RootNode(param_0, param_1, param_2, param_3):
    def __init__(buf, offset, chunk, parent):
        pass
    def tag_length():
        return 0
    def children():
        return class_var._children(None, (EndOfStreamToken,))
    def tag_and_children_length():
        children_length = 0
        for child in class_var.children():
            children_length += child.length()
        return class_var.tag_length() + children_length
    def template_instance():
        ofs = class_var.offset()
        if class_var.unpack_byte(0x0) & 0x0F == 0xF:
            ofs += 4
        return TemplateInstanceNode(class_var._buf, ofs, class_var._chunk, class_var)
    def template():
        instance = class_var.template_instance()
        offset = class_var._chunk.offset() + instance.template_offset()
        node = TemplateNode(class_var._buf, offset, class_var._chunk, instance)
        return node
    def substitutions():
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
                raise ParseException("Invalid substitution value size")
            sub_def.append(val)
            ofs += size
        return sub_def
    class_var = BXmlNode(param_0, param_1, param_2, param_3)
    class_var._class_name = 'RootNode;' + class_var._class_name
    children = memoize(children, class_var)
    substitutions = memoize(substitutions, class_var)
    class_var.__init__ = __init__
    class_var.tag_length = tag_length
    class_var.children = children
    class_var.tag_and_children_length = tag_and_children_length
    class_var.template_instance = template_instance
    class_var.template = template
    class_var.substitutions = substitutions
    __init__(param_0, param_1, param_2, param_3)
    return class_var
def VariantTypeNode(param_0, param_1, param_2, param_3, param_4):
    def __init__(buf, offset, chunk, parent, length):
        class_var._length = length
    def length():
        return class_var.tag_length()
    def children():
        return []
    class_var = BXmlNode(param_0, param_1, param_2, param_3)
    class_var._class_name = 'VariantTypeNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.length = length
    class_var.children = children
    __init__(param_0, param_1, param_2, param_3, param_4)
    return class_var
def NullTypeNode(param_0, param_1, param_2, param_3, param_4):
    def __init__(buf, offset, chunk, parent, length):
        class_var._offset = offset
        class_var._length = length
    def string():
        return ""
    def length():
        return class_var._length or 0
    def children():
        return []
    class_var = SkelClass('NullTypeNode')
    class_var.__init__ = __init__
    class_var.string = string
    class_var.length = length
    class_var.children = children
    __init__(param_0, param_1, param_2, param_3, param_4)
    return class_var
def WstringTypeNode(param_0, param_1, param_2, param_3, param_4):
    def __init__(buf, offset, chunk, parent, length):
        if class_var._length is None:
            class_var.declare_field("word", "string_length", 0x0, None)
            class_var.declare_field("wstring", "_string", length=(class_var.string_length()))
        else:
            class_var.declare_field("wstring", "_string", 0x0, (class_var._length // 2))
    def tag_length():
        if class_var._length is None:
            return 2 + (class_var.string_length() * 2)
        return class_var._length
    def string():
        return class_var._string().rstrip("\x00")
    class_var = VariantTypeNode(param_0, param_1, param_2, param_3, param_4)
    class_var._class_name = 'WstringTypeNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.tag_length = tag_length
    class_var.string = string
    __init__(param_0, param_1, param_2, param_3, param_4)
    return class_var
def UnsignedByteTypeNode(param_0, param_1, param_2, param_3, param_4):
    def __init__(buf, offset, chunk, parent, length):
        class_var.declare_field("byte", "byte", 0x0, None)
    def tag_length():
        return 1
    def string():
        return str(class_var.byte())
    class_var = VariantTypeNode(param_0, param_1, param_2, param_3, param_4)
    class_var._class_name = 'UnsignedByteTypeNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.tag_length = tag_length
    class_var.string = string
    __init__(param_0, param_1, param_2, param_3, param_4)
    return class_var
def UnsignedWordTypeNode(param_0, param_1, param_2, param_3, param_4):
    def __init__(buf, offset, chunk, parent, length):
        class_var.declare_field("word", "word", 0x0, None)
    def tag_length():
        return 2
    def string():
        return str(class_var.word())
    class_var = VariantTypeNode(param_0, param_1, param_2, param_3, param_4)
    class_var._class_name = 'UnsignedWordTypeNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.tag_length = tag_length
    class_var.string = string
    __init__(param_0, param_1, param_2, param_3, param_4)
    return class_var
def UnsignedDwordTypeNode(param_0, param_1, param_2, param_3, param_4):
    def __init__(buf, offset, chunk, parent, length):
        class_var.declare_field("dword", "dword", 0x0, None)
    def tag_length():
        return 4
    def string():
        return str(class_var.dword())
    class_var = VariantTypeNode(param_0, param_1, param_2, param_3, param_4)
    class_var._class_name = 'UnsignedDwordTypeNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.tag_length = tag_length
    class_var.string = string
    __init__(param_0, param_1, param_2, param_3, param_4)
    return class_var
def UnsignedQwordTypeNode(param_0, param_1, param_2, param_3, param_4):
    def __init__(buf, offset, chunk, parent, length):
        class_var.declare_field("qword", "qword", 0x0, None)
    def tag_length():
        return 8
    def string():
        return str(class_var.qword())
    class_var = VariantTypeNode(param_0, param_1, param_2, param_3, param_4)
    class_var._class_name = 'UnsignedQwordTypeNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.tag_length = tag_length
    class_var.string = string
    __init__(param_0, param_1, param_2, param_3, param_4)
    return class_var
def FloatTypeNode(param_0, param_1, param_2, param_3, param_4):
    def __init__(buf, offset, chunk, parent, length):
        class_var.declare_field("float", "float", 0x0)
    def tag_length():
        return 4
    def string():
        return str(class_var.float())
    class_var = VariantTypeNode(param_0, param_1, param_2, param_3, param_4)
    class_var._class_name = 'FloatTypeNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.tag_length = tag_length
    class_var.string = string
    __init__(param_0, param_1, param_2, param_3, param_4)
    return class_var
def DoubleTypeNode(param_0, param_1, param_2, param_3, param_4):
    def __init__(buf, offset, chunk, parent, length):
        class_var.declare_field("double", "double", 0x0)
    def tag_length():
        return 8
    def string():
        return str(class_var.double())
    class_var = VariantTypeNode(param_0, param_1, param_2, param_3, param_4)
    class_var._class_name = 'DoubleTypeNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.tag_length = tag_length
    class_var.string = string
    __init__(param_0, param_1, param_2, param_3, param_4)
    return class_var
def BooleanTypeNode(param_0, param_1, param_2, param_3, param_4):
    def __init__(buf, offset, chunk, parent, length):
        class_var.declare_field("int32", "int32", 0x0, None)
    def tag_length():
        return 4
    def string():
        if class_var.int32() > 0:
            return "True"
        return "False"
    class_var = VariantTypeNode(param_0, param_1, param_2, param_3, param_4)
    class_var._class_name = 'BooleanTypeNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.tag_length = tag_length
    class_var.string = string
    __init__(param_0, param_1, param_2, param_3, param_4)
    return class_var
def BinaryTypeNode(param_0, param_1, param_2, param_3, param_4):
    def __init__(buf, offset, chunk, parent, length):
        if class_var._length is None:
            class_var.declare_field("dword", "size", 0x0)
            class_var.declare_field("binary", "binary", length=class_var.size())
        else:
            class_var.declare_field("binary", "binary", 0x0, class_var._length)
    def tag_length():
        if class_var._length is None:
            return 4 + class_var.size()
        return class_var._length
    def string():
        return base64.b64encode(class_var.binary()).decode("ascii")
    class_var = VariantTypeNode(param_0, param_1, param_2, param_3, param_4)
    class_var._class_name = 'BinaryTypeNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.tag_length = tag_length
    class_var.string = string
    __init__(param_0, param_1, param_2, param_3, param_4)
    return class_var
def GuidTypeNode(param_0, param_1, param_2, param_3, param_4):
    def __init__(buf, offset, chunk, parent, length):
        class_var.declare_field("guid", "guid", 0x0, None)
    def tag_length():
        return 16
    def string():
        return "{" + class_var.guid() + "}"
    class_var = VariantTypeNode(param_0, param_1, param_2, param_3, param_4)
    class_var._class_name = 'GuidTypeNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.tag_length = tag_length
    class_var.string = string
    __init__(param_0, param_1, param_2, param_3, param_4)
    return class_var
def SizeTypeNode(param_0, param_1, param_2, param_3, param_4):
    def __init__(buf, offset, chunk, parent, length):
        if class_var._length == 0x4:
            class_var.declare_field("dword", "num", 0x0)
        elif class_var._length == 0x8:
            class_var.declare_field("qword", "num", 0x0)
        else:
            class_var.declare_field("qword", "num", 0x0)
    def tag_length():
        if class_var._length is None:
            return 8
        return class_var._length
    def string():
        return str(class_var.num())
    class_var = VariantTypeNode(param_0, param_1, param_2, param_3, param_4)
    class_var._class_name = 'SizeTypeNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.tag_length = tag_length
    class_var.string = string
    __init__(param_0, param_1, param_2, param_3, param_4)
    return class_var
def FiletimeTypeNode(param_0, param_1, param_2, param_3, param_4):
    def __init__(buf, offset, chunk, parent, length):
        class_var.declare_field("filetime", "filetime", 0x0, None)
    def string():
        t = class_var.filetime().isoformat(" ")
        return "time not supported"
    def tag_length():
        return 8
    class_var = VariantTypeNode(param_0, param_1, param_2, param_3, param_4)
    class_var._class_name = 'FiletimeTypeNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.string = string
    class_var.tag_length = tag_length
    __init__(param_0, param_1, param_2, param_3, param_4)
    return class_var
def SystemtimeTypeNode(param_0, param_1, param_2, param_3, param_4):
    def __init__(buf, offset, chunk, parent, length):
        class_var.declare_field("systemtime", "systemtime", 0x0)
    def tag_length():
        return 16
    def string():
        t = class_var.systemtime().isoformat(" ")
        return "time not supported"
    class_var = VariantTypeNode(param_0, param_1, param_2, param_3, param_4)
    class_var._class_name = 'SystemtimeTypeNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.tag_length = tag_length
    class_var.string = string
    __init__(param_0, param_1, param_2, param_3, param_4)
    return class_var
def SIDTypeNode(param_0, param_1, param_2, param_3, param_4):
    def __init__(buf, offset, chunk, parent, length):
        class_var.declare_field("byte", "version", 0x0, None)
        class_var.declare_field("byte", "num_elements", None, None)
        class_var.declare_field("dword_be", "id_high", None, None)
        class_var.declare_field("word_be", "id_low", None, None)
    def elements():
        ret = []
        _tmp = class_var.num_elements()
        for i in range(_tmp):
            ret.append(class_var.unpack_dword(class_var.current_field_offset() + 4 * i))
        return ret
    def id():
        ret = "S-{}-{}".format(class_var.version(), (class_var.id_high() << 16) ^ class_var.id_low())
        for elem in class_var.elements():
            ret += "-{}".format(elem)
        return ret
    def tag_length():
        return 8 + 4 * class_var.num_elements()
    def string():
        return class_var.id()
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
    def __init__(buf, offset, chunk, parent, length):
        class_var.declare_field("binary", "hex", 0x0, 0x4)
    def tag_length():
        return 4
    def string():
        ret = "0x"
        b = class_var.hex()[::-1]
        for i in range(len(b)):
            ret += "{:02x}".format(b[i])
        return ret
    class_var = VariantTypeNode(param_0, param_1, param_2, param_3, param_4)
    class_var._class_name = 'Hex32TypeNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.tag_length = tag_length
    class_var.string = string
    __init__(param_0, param_1, param_2, param_3, param_4)
    return class_var
def Hex64TypeNode(param_0, param_1, param_2, param_3, param_4):
    def __init__(buf, offset, chunk, parent, length):
        class_var.declare_field("binary", "hex", 0x0, 0x8)
    def tag_length():
        return 8
    def string():
        ret = "0x"
        b = class_var.hex()[::-1]
        for i in range(len(b)):
            ret += "{:02x}".format(b[i])
        return ret
    class_var = VariantTypeNode(param_0, param_1, param_2, param_3, param_4)
    class_var._class_name = 'Hex64TypeNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.tag_length = tag_length
    class_var.string = string
    __init__(param_0, param_1, param_2, param_3, param_4)
    return class_var
def BXmlTypeNode(param_0, param_1, param_2, param_3, param_4):
    def __init__(buf, offset, chunk, parent, length):
        class_var._root = RootNode(buf, offset, chunk, class_var)
    def tag_length():
        return class_var._length or class_var._root.length()
    def string():
        return ""
    def root():
        return class_var._root
    class_var = VariantTypeNode(param_0, param_1, param_2, param_3, param_4)
    class_var._class_name = 'BXmlTypeNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.tag_length = tag_length
    class_var.string = string
    class_var.root = root
    __init__(param_0, param_1, param_2, param_3, param_4)
    return class_var
def WstringArrayTypeNode(param_0, param_1, param_2, param_3, param_4):
    def __init__(buf, offset, chunk, parent, length):
        if class_var._length is None:
            class_var.declare_field("word", "binary_length", 0x0)
            class_var.declare_field("binary", "binary", length=(class_var.binary_length()))
        else:
            class_var.declare_field("binary", "binary", 0x0, (class_var._length))
    def tag_length():
        if class_var._length is None:
            return 2 + class_var.binary_length()
        return class_var._length
    def string():
        binary = class_var.binary()
        acc = []
        while len(binary) > 0:
            match = re.search(b"((?:[^\x00].)+)", binary)
            if match:
                frag = match.group()
                acc.append("<string>")
                acc.append(frag.decode("utf16"))
                acc.append("</string>\n")
                binary = binary[len(frag) + 2:]
                if len(binary) == 0:
                    break
            frag = re.search(b"(\x00*)", binary).group()
            if len(frag) % 2 == 0:
                for _ in range(len(frag) // 2):
                    acc.append("<string></string>\n")
            else:
                raise ParseException("Error parsing uneven substring of NULLs")
            binary = binary[len(frag):]
        return "".join(acc)
    class_var = VariantTypeNode(param_0, param_1, param_2, param_3, param_4)
    class_var._class_name = 'WstringArrayTypeNode;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.tag_length = tag_length
    class_var.string = string
    __init__(param_0, param_1, param_2, param_3, param_4)
    return class_var
def UnexpectedElementException(param_0):
    def __init__(msg):
        pass
    class_var = Exception(param_0)
    class_var._class_name = 'UnexpectedElementException;' + class_var._class_name
    class_var.__init__ = __init__
    __init__(param_0)
    return class_var
def escape_attr(s):
    RESTRICTED_CHARS = re.compile('[\x01-\x08\x0B\x0C\x0E-\x1F\x7F-\x84\x86-\x9F]')
    esc = xml.sax.saxutils.quoteattr(s)
    esc = esc.encode('ascii', 'xmlcharrefreplace').decode('ascii')
    esc = RESTRICTED_CHARS.sub('', esc)
    return esc
def escape_value(s):
    RESTRICTED_CHARS = re.compile('[\x01-\x08\x0B\x0C\x0E-\x1F\x7F-\x84\x86-\x9F]')
    esc = xml.sax.saxutils.escape(s)
    esc = esc.encode('ascii', 'xmlcharrefreplace').decode('ascii')
    esc = RESTRICTED_CHARS.sub('', esc)
    return esc
def validate_name(s):
    if not NAME_PATTERN.match(s):
        raise RuntimeError("invalid xml name: %s" % (s))
    return s
def render_root_node_with_subs(root_node, subs):
    def rec(node, acc):
        if user_check_type(node, EndOfStreamNode):
            pass
        elif user_check_type(node, OpenStartElementNode):
            acc.append("<")
            acc.append(node.tag_name())
            for child in node.children():
                if user_check_type(child, AttributeNode):
                    acc.append(" ")
                    acc.append(validate_name(child.attribute_name().string()))
                    acc.append('="')
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
        elif user_check_type(node, CloseEmptyElementNode):
            pass
        elif user_check_type(node, CloseElementNode):
            pass
        elif user_check_type(node, ValueNode):
            acc.append(escape_value(node.children()[0].string()))
        elif user_check_type(node, AttributeNode):
            pass
        elif user_check_type(node, EntityReferenceNode):
            acc.append(escape_value(node.entity_reference()))
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
    acc = []
    for c in root_node.template().children():
        rec(c, acc)
    return "".join(acc)
def render_root_node(root_node):
    subs = []
    for sub in root_node.substitutions():
        if isinstance(sub, str):
            raise RuntimeError("string sub?")
        if sub is None:
            raise RuntimeError("null sub?")
        subs.append(sub)
    return render_root_node_with_subs(root_node, subs)
def evtx_record_xml_view(record, cache):
    return render_root_node(record.root())
def InvalidRecordException():
    def __init__():
        pass
    class_var = ParseException("Invalid record structure")
    class_var._class_name = 'InvalidRecordException;' + class_var._class_name
    class_var.__init__ = __init__
    __init__()
    return class_var
def FileHeader(param_0, param_1):
    def __init__(buf, offset):
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
    def check_magic():
        return class_var.magic() == "ElfFile\x00"
    def calculate_checksum():
        return binascii.crc32(class_var.unpack_binary(0, 0x78)) & 0xFFFFFFFF
    def verify():
        return (class_var.check_magic() and class_var.major_version() == 0x3 and class_var.minor_version() == 0x1 and class_var.header_chunk_size() == 0x1000 and class_var.checksum() == class_var.calculate_checksum())
    def is_dirty():
        return class_var.flags() & 0x1 == 0x1
    def is_full():
        return class_var.flags() & 0x2 == 0x2
    def first_chunk():
        ofs = class_var._offset + class_var.header_chunk_size()
        return ChunkHeader(class_var._buf, ofs)
    def current_chunk():
        ofs = class_var._offset + class_var.header_chunk_size()
        ofs += class_var.current_chunk_number() * 0x10000
        return ChunkHeader(class_var._buf, ofs)
    def chunks(include_inactive):
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
    def get_record(record_num):
        for chunk in class_var.chunks():
            first_record = chunk.log_first_record_number()
            last_record = chunk.log_last_record_number()
            if not (first_record <= record_num <= last_record):
                continue
            for record in chunk.records():
                if record.record_num() == record_num:
                    return record
        return None
    class_var = Block(param_0, param_1)
    class_var._class_name = 'FileHeader;' + class_var._class_name
    class_var.__init__ = __init__
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
        class_var._template_node = template_node
        class_var._xml = None
    def _load_xml():
        if class_var._xml is not None:
            return
        matcher = r"\[(?:Normal|Conditional) Substitution\(index=(\d+), type=\d+\)\]"
        class_var._xml = re.sub(matcher, "{\\1:}", class_var._template_node.template_format().replace("{", "{{").replace("}", "}}"))
    def make_substitutions(substitutions):
        class_var._load_xml()
        return class_var._xml.format(*[n.xml() for n in substitutions])
    def node():
        return class_var._template_node
    class_var = SkelClass('Template')
    class_var.__init__ = __init__
    class_var._load_xml = _load_xml
    class_var.make_substitutions = make_substitutions
    class_var.node = node
    __init__(param_0)
    return class_var
def ChunkHeader(param_0, param_1):
    def __init__(buf, offset):
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
    def check_magic():
        return class_var.magic() == "ElfChnk\x00"
    def calculate_header_checksum():
        data = class_var.unpack_binary(0x0, 0x78)
        data += class_var.unpack_binary(0x80, 0x180)
        return binascii.crc32(data) & 0xFFFFFFFF
    def calculate_data_checksum():
        data = class_var.unpack_binary(0x200, class_var.next_record_offset() - 0x200)
        return binascii.crc32(data) & 0xFFFFFFFF
    def verify():
        return (class_var.check_magic() and class_var.calculate_header_checksum() == class_var.header_checksum() and class_var.calculate_data_checksum() == class_var.data_checksum())
    def _load_strings():
        if class_var._strings is None:
            class_var._strings = {}
        for i in range(64):
            ofs = class_var.unpack_dword(0x80 + (i * 4))
            while ofs > 0:
                string_node = class_var.add_string(ofs, None)
                ofs = string_node.next_offset()
    def strings():
        if not class_var._strings:
            class_var._load_strings()
        return class_var._strings
    def add_string(offset, parent):
        if class_var._strings is None:
            class_var._load_strings()
        string_node = NameStringNode(class_var._buf, class_var._offset + offset, class_var, parent or class_var)
        class_var._strings[offset] = string_node
        return string_node
    def _load_templates():
        if class_var._templates is None:
            class_var._templates = {}
        for i in range(32):
            ofs = class_var.unpack_dword(0x180 + (i * 4))
            while ofs > 0:
                token = class_var.unpack_byte(ofs - 10)
                pointer = class_var.unpack_dword(ofs - 4)
                if token != 0x0C or pointer != ofs:
                    ofs = 0
                    continue
                template = class_var.add_template(ofs, None)
                ofs = template.next_offset()
    def add_template(offset, parent):
        if class_var._templates is None:
            class_var._load_templates()
        node = TemplateNode(class_var._buf, class_var._offset + offset, class_var, parent or class_var)
        class_var._templates[offset] = node
        return node
    def templates():
        if not class_var._templates:
            class_var._load_templates()
        return class_var._templates
    def first_record():
        return Record(class_var._buf, class_var._offset + 0x200, class_var)
    def records():
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
    class_var = Block(param_0, param_1)
    class_var._class_name = 'ChunkHeader;' + class_var._class_name
    class_var.__init__ = __init__
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
        class_var._chunk = chunk
        class_var.declare_field("dword", "magic", 0x0, None)
        class_var.declare_field("dword", "size", None, None)
        class_var.declare_field("qword", "record_num", None, None)
        class_var.declare_field("filetime", "timestamp", None, None)
        if class_var.size() > 0x10000:
            return None
        class_var.declare_field("dword", "size2", class_var.size() - 4, None)
    def root():
        return RootNode(class_var._buf, class_var._offset + 0x18, class_var._chunk, class_var)
    def length():
        return class_var.size()
    def verify():
        return class_var.size() == class_var.size2()
    def data():
        return class_var._buf[class_var.offset():class_var.offset() + class_var.size()]
    def xml():
        return evtx_record_xml_view(class_var, None)
    class_var = Block(param_0, param_1)
    class_var._class_name = 'Record;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.root = root
    class_var.length = length
    class_var.verify = verify
    class_var.data = data
    class_var.xml = xml
    __init__(param_0, param_1, param_2)
    return class_var
expected_output1 = [{"start_file": 1, "end_file": 153, "start_log": 12049, "end_log": 12201}, {"start_file": 154, "end_file": 336, "start_log": 12202, "end_log": 12384}, {"start_file": 337, "end_file": 526, "start_log": 12385, "end_log": 12574}, {"start_file": 527, "end_file": 708, "start_log": 12575, "end_log": 12756}, {"start_file": 709, "end_file": 882, "start_log": 12757, "end_log": 12930}, {"start_file": 883, "end_file": 1059, "start_log": 12931, "end_log": 13107}, {"start_file": 1060, "end_file": 1241, "start_log": 13108, "end_log": 13289}, {"start_file": 1242, "end_file": 1424, "start_log": 13290, "end_log": 13472}, {"start_file": 1425, "end_file": 1601, "start_log": 13473, "end_log": 13649}]
expected_output2 = [{"start_file": 1, "end_file": 91, "start_log": 1, "end_log": 91}, {"start_file": 92, "end_file": 177, "start_log": 92, "end_log": 177}, {"start_file": 178, "end_file": 260, "start_log": 178, "end_log": 260}, {"start_file": 261, "end_file": 349, "start_log": 261, "end_log": 349}, {"start_file": 350, "end_file": 441, "start_log": 350, "end_log": 441}, {"start_file": 442, "end_file": 530, "start_log": 442, "end_log": 530}, {"start_file": 531, "end_file": 622, "start_log": 531, "end_log": 622}, {"start_file": 623, "end_file": 711, "start_log": 623, "end_log": 711}, {"start_file": 712, "end_file": 802, "start_log": 712, "end_log": 802}, {"start_file": 803, "end_file": 888, "start_log": 803, "end_log": 888}, {"start_file": 889, "end_file": 976, "start_log": 889, "end_log": 976}, {"start_file": 977, "end_file": 1063, "start_log": 977, "end_log": 1063}, {"start_file": 1064, "end_file": 1148, "start_log": 1064, "end_log": 1148}, {"start_file": 1149, "end_file": 1239, "start_log": 1149, "end_log": 1239}, {"start_file": 1240, "end_file": 1327, "start_log": 1240, "end_log": 1327}, {"start_file": 1328, "end_file": 1414, "start_log": 1328, "end_log": 1414}, {"start_file": 1415, "end_file": 1501, "start_log": 1415, "end_log": 1501}, {"start_file": 1502, "end_file": 1587, "start_log": 1502, "end_log": 1587}, {"start_file": 1588, "end_file": 1682, "start_log": 1588, "end_log": 1682}, {"start_file": 1683, "end_file": 1766, "start_log": 1683, "end_log": 1766}, {"start_file": 1767, "end_file": 1847, "start_log": 1767, "end_log": 1847}, {"start_file": 1848, "end_file": 1942, "start_log": 1848, "end_log": 1942}, {"start_file": 1943, "end_file": 2027, "start_log": 1943, "end_log": 2027}, {"start_file": 2028, "end_file": 2109, "start_log": 2028, "end_log": 2109}, {"start_file": 2110, "end_file": 2201, "start_log": 2110, "end_log": 2201}, {"start_file": 2202, "end_file": 2261, "start_log": 2202, "end_log": 2261}]
expected_output3 = ["RootNode", None, [["StreamStartNode"], ["TemplateInstanceNode", None, [["TemplateNode", None, [["StreamStartNode"], ["OpenStartElementNode", "Event", [["AttributeNode", "xmlns", [["ValueNode", None, [["WstringTypeNode", "http://schemas.microsoft.com/win/2004/08/events/event"]]]]], ["CloseStartElementNode"], ["OpenStartElementNode", "System", [["CloseStartElementNode"], ["OpenStartElementNode", "Provider", [["AttributeNode", "Name", [["ValueNode", None, [["WstringTypeNode", "Microsoft-Windows-Eventlog"]]]]], ["AttributeNode", "Guid", [["ValueNode", None, [["WstringTypeNode", "{fc65ddd8-d6ef-4962-83d5-6e5cfe9ce148}"]]]]], ["CloseEmptyElementNode"]]], ["OpenStartElementNode", "EventID", [["AttributeNode", "Qualifiers", [["ConditionalSubstitutionNode"]]], ["CloseStartElementNode"], ["ConditionalSubstitutionNode"], ["CloseElementNode"]]], ["OpenStartElementNode", "Version", [["CloseStartElementNode"], ["ConditionalSubstitutionNode"], ["CloseElementNode"]]], ["OpenStartElementNode", "Level", [["CloseStartElementNode"], ["ConditionalSubstitutionNode"], ["CloseElementNode"]]], ["OpenStartElementNode", "Task", [["CloseStartElementNode"], ["ConditionalSubstitutionNode"], ["CloseElementNode"]]], ["OpenStartElementNode", "Opcode", [["CloseStartElementNode"], ["ConditionalSubstitutionNode"], ["CloseElementNode"]]], ["OpenStartElementNode", "Keywords", [["CloseStartElementNode"], ["ConditionalSubstitutionNode"], ["CloseElementNode"]]], ["OpenStartElementNode", "TimeCreated", [["AttributeNode", "SystemTime", [["ConditionalSubstitutionNode"]]], ["CloseEmptyElementNode"]]], ["OpenStartElementNode", "EventRecordID", [["CloseStartElementNode"], ["ConditionalSubstitutionNode"], ["CloseElementNode"]]], ["OpenStartElementNode", "Correlation", [["AttributeNode", "ActivityID", [["ConditionalSubstitutionNode"]]], ["AttributeNode", "RelatedActivityID", [["ConditionalSubstitutionNode"]]], ["CloseEmptyElementNode"]]], ["OpenStartElementNode", "Execution", [["AttributeNode", "ProcessID", [["ConditionalSubstitutionNode"]]], ["AttributeNode", "ThreadID", [["ConditionalSubstitutionNode"]]], ["CloseEmptyElementNode"]]], ["OpenStartElementNode", "Channel", [["CloseStartElementNode"], ["ValueNode", None, [["WstringTypeNode", "System"]]], ["CloseElementNode"]]], ["OpenStartElementNode", "Computer", [["CloseStartElementNode"], ["ValueNode", None, [["WstringTypeNode", "WKS-WIN764BITB.shieldbase.local"]]], ["CloseElementNode"]]], ["OpenStartElementNode", "Security", [["AttributeNode", "UserID", [["ConditionalSubstitutionNode"]]], ["CloseEmptyElementNode"]]], ["CloseElementNode"]]], ["OpenStartElementNode", "UserData", [["CloseStartElementNode"], ["ConditionalSubstitutionNode"], ["CloseElementNode"]]], ["CloseElementNode"]]], ["EndOfStreamNode"]]]]], ["Substitutions", None, [["UnsignedByteTypeNode", "4"], ["UnsignedByteTypeNode", "0"], ["UnsignedWordTypeNode", "105"], ["UnsignedWordTypeNode", "105"], ["NullTypeNode"], ["Hex64TypeNode", "0x8000000000000000"], ["FiletimeTypeNode", "time not supported"], ["NullTypeNode"], ["UnsignedDwordTypeNode", "820"], ["UnsignedDwordTypeNode", "2868"], ["UnsignedQwordTypeNode", "12049"], ["UnsignedByteTypeNode", "0"], ["NullTypeNode"], ["NullTypeNode"], ["NullTypeNode"], ["NullTypeNode"], ["NullTypeNode"], ["NullTypeNode"], ["NullTypeNode"], ["BXmlTypeNode", None, [["RootNode", None, [["StreamStartNode"], ["TemplateInstanceNode", None, [["TemplateNode", None, [["StreamStartNode"], ["OpenStartElementNode", "AutoBackup", [["AttributeNode", "xmlns:auto-ns3", [["ValueNode", None, [["WstringTypeNode", "http://schemas.microsoft.com/win/2004/08/events"]]]]], ["AttributeNode", "xmlns", [["ValueNode", None, [["WstringTypeNode", "http://manifests.microsoft.com/win/2004/08/windows/eventlog"]]]]], ["CloseStartElementNode"], ["OpenStartElementNode", "Channel", [["CloseStartElementNode"], ["NormalSubstitutionNode"], ["CloseElementNode"]]], ["OpenStartElementNode", "BackupPath", [["CloseStartElementNode"], ["NormalSubstitutionNode"], ["CloseElementNode"]]], ["CloseElementNode"]]], ["EndOfStreamNode"]]]]], ["Substitutions", None, [["WstringTypeNode", "System"], ["WstringTypeNode", r"C:\Windows\System32\Winevt\Logs\Archive-System-2012-03-14-04-17-39-932.evtx"]]]]]]]]]]]
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
    cd = os.path.dirname(__file__)
    datadir = os.path.join(cd, "evtx.d")
    systempath = os.path.join(datadir, "system.evtx")
    return systempath
def system():
    p = system_path()
    with open(p, "rb") as f:
        return f.read()
def security_path():
    cd = os.path.dirname(__file__)
    datadir = os.path.join(cd, "evtx.d")
    secpath = os.path.join(datadir, "security.evtx")
    return secpath
def security():
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
    fh = FileHeader(input_str, 0x0)
    expecteds = expected_output1
    for i, chunk in enumerate(fh.chunks(False)):
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
def test_chunks2(input_str):
    fh = FileHeader(input_str, 0x0)
    expecteds = expected_output2
    for i, chunk in enumerate(fh.chunks(False)):
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
def test_file_header(input_str):
    fh = FileHeader(input_str, 0x0)
    assert fh.magic() == "ElfFile\x00"
    assert fh.major_version() == 0x3
    assert fh.minor_version() == 0x1
    assert fh.flags() == 0x1
    assert fh.is_dirty() is True
    assert fh.is_full() is False
    assert fh.current_chunk_number() == 0x0
    assert fh.chunk_count() == 0x1
    assert fh.oldest_chunk() == 0x0
    assert fh.next_record_number() == 0x34D8
    assert fh.checksum() == 0xA49E1EA8
    assert fh.calculate_checksum() == fh.checksum()
def test_file_header2(input_str):
    fh = FileHeader(input_str, 0x0)
    assert fh.magic() == "ElfFile\x00"
    assert fh.major_version() == 0x3
    assert fh.minor_version() == 0x1
    assert fh.flags() == 0x1
    assert fh.is_dirty() is True
    assert fh.is_full() is False
    assert fh.current_chunk_number() == 0x0
    assert fh.chunk_count() == 0x1
    assert fh.oldest_chunk() == 0x0
    assert fh.next_record_number() == 0x8B2
    assert fh.checksum() == 0x1A4A389B
    assert fh.calculate_checksum() == fh.checksum()
def extract_structure(node):
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
def test_parse_record(input_str):
    fh = FileHeader(input_str, 0x0)
    chunk = next(fh.chunks(False))
    record = next(chunk.records())
    expected = expected_output3
    assert extract_structure(record.root()) == expected
def test_render_record(input_str):
    fh = FileHeader(input_str, 0x0)
    chunk = next(fh.chunks(False))
    record = next(chunk.records())
    xml = record.xml()
    assert xml == expected_output4
def test_parse_records(input_str):
    fh = FileHeader(input_str, 0x0)
    for i, chunk in enumerate(fh.chunks(False)):
        for j, record in enumerate(chunk.records()):
            assert record.magic() == 0x2A2A
def test_parse_records2(input_str):
    fh = FileHeader(input_str, 0x0)
    for i, chunk in enumerate(fh.chunks(False)):
        for j, record in enumerate(chunk.records()):
            assert record.magic() == 0x2A2A
def test_render_records(input_str):
    fh = FileHeader(input_str, 0x0)
    for chunk in fh.chunks(False):
        for record in chunk.records():
            assert record.xml() is not None
def test_render_records2(input_str):
    fh = FileHeader(input_str, 0x0)
    for chunk in fh.chunks(False):
        for record in chunk.records():
            assert record.xml() is not None
def test():
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
EMPTY_MAGIC = "\x00" * 0x8
XML_HEADER = '<?xml version="1.1" encoding="utf-8" standalone="yes" ?>\n'
node_dispatch_table = [EndOfStreamNode, OpenStartElementNode, CloseStartElementNode, CloseEmptyElementNode, CloseElementNode, ValueNode, AttributeNode, None, CharacterReferenceNode, EntityReferenceNode, None, None, TemplateInstanceNode, NormalSubstitutionNode, ConditionalSubstitutionNode, StreamStartNode]
node_readable_tokens = ["End of Stream", "Open Start Element", "Close Start Element", "Close Empty Element", "Close Element", "Value", "Attribute", "unknown", "unknown", "unknown", "unknown", "unknown", "TemplateInstanceNode", "Normal Substitution", "Conditional Substitution", "Start of Stream"]
test()