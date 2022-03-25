import struct
import escape_dict as escd


class PointerError(Exception):
    """Exception class to inform that pointer and offset do not match"""


def checkPointer(offset, pointer):
    if offset != pointer:
        raise PointerError


def getOffsetAddress(source, size, pointer):
    address_list = []
    for i in range(size):
        address_list.append(unpackOneFormat("L", source, pointer, 0))
        pointer += 0x4
    return address_list, pointer


def setZeroPaddingForLabel(label, num, enc):
    b = b""
    i = 0
    while i < len(label):
        if label[i] == '〇':
            key = label[i:i + 7]
            i += 6
        else:
            key = label[i]
        value = escd.escape_dict.get(key)
        if value is not None:
            b_chr = value[0]
        else:
            b_chr = label[i].encode(encoding=enc)
        b += b_chr
        i += 1
    zero = (0).to_bytes(num - (len(b)), byteorder='little')
    return b + zero


def getName(data, name_adr, enc, print_flag):
    adr = name_adr
    while data[adr] != 0:
        adr += 1
    if enc == 'euc_jp':
        name = getNameWithEscapeCharacter(data, name_adr, enc)
    else:
        name = data[name_adr:adr].decode(enc)
    if print_flag == 1:
        print("ADDRESS:{0:08X},name:{1}".format(name_adr, name))
    return name


# Escape character processing
def getNameWithEscapeCharacter(data, name_adr, enc):
    adr = name_adr
    name = ""
    while data[adr] != 0:
        if (data[adr:adr + 2] in escd.escape_dict_keys) is True:
            key = [k for k, v in escd.escape_dict.items() if v[0] == data[adr:adr + 2]][0]
            name += key
            adr += 2
        elif (data[adr] in range(0xA1, 0xFF)) and (data[adr + 1] in range(0xA1, 0xFF)):
            name += data[adr:adr + 2].decode(enc)
            adr += 2
        else:
            name += data[adr:adr + 1].decode(enc)
            adr += 1
    return name


def unpackOneFormat(fmt, buffer, offset, print_flag):
    data = struct.unpack_from(fmt, buffer, offset)
    if print_flag == 1:
        print("ADDRESS:{0:08X},value:{1:X}".format(offset, data[0]))
    return data[0]


def getLen(label, enc):
    label_bin = label.encode(encoding=enc)
    label_len = len(label_bin)
    i = 0
    while i < len(label):
        if label[i] == '〇':
            key = label[i:i + 7]
            i += 6
        else:
            key = label[i]
        value = escd.escape_dict.get(key)
        if value is not None:
            label_len -= value[1]
        i += 1
    # padding
    padding = 4 - (label_len % 4)
    if padding == 0:
        padding = 4
    return label_len + padding


def makeOutputDir(p_input, p_output_dir):
    if p_output_dir is None or p_input == p_output_dir:
        p_output_dir = p_input / 'out' if p_input.is_dir() else p_input.parent / 'out'
        if p_output_dir.is_dir() is False:
            p_output_dir.mkdir()
    return p_output_dir
