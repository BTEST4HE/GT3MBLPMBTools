import helper

pmb_dict = {
    'pmb10': 0x20,
    'pmb20': 0x39,
    'pmb21': 0x7D,
    'pmb40': 0x7E,
    'pmb40s': 0x5E
}
"""
pmb_dict
0x01 : chr_size = 0x20
0x02 : chr_size = 0x40
0x04 : FUNC data availability
0x08 : Availability of recursive data for SUB
0x10 : Presence of variable "text_unk_3" in TEXT data
0x20 : euc_jp when ON, sjis when OFF
0x40 : PMBBIN with or without some padding
"""

pmb_dict_list = list(pmb_dict.keys())

pmb_control_flags_list = [[['pmb10', 'pmb21'], [0x10000, 0]],
                          [['pmb10', 'pmb40'], [0x10000, 0]],
                          [['pmb10', 'pmb40s'], [0x10000, 0]],
                          [['pmb20', 'pmb21'], [0x10000, 0]],
                          [['pmb20', 'pmb40'], [0x10000, 0]],
                          [['pmb20', 'pmb40s'], [0x10000, 0]],
                          [['pmb10', 'pmb20'], [0x8, 0]],
                          [['pmb10', 'pmb21'], [0x8, 0]],
                          [['pmb10', 'pmb40'], [0x8, 0]],
                          [['pmb10', 'pmb40s'], [0x8, 0]]
                          ]


def importPmb(source, pmb_flags):
    if (pmb_flags & 0x1) != 0:
        chr_size = 0x20
    elif (pmb_flags & 0x2) != 0:
        chr_size = 0x40
    else:
        chr_size = 0x10
    # FileHeader
    r_m_size = helper.unpackOneFormat("L", source, 0x00, 0)
    r_offset = helper.unpackOneFormat("L", source, 0x04, 0)
    r_img_size = helper.unpackOneFormat("L", source, 0x08, 0)
    r_img_offset = helper.unpackOneFormat("L", source, 0x0C, 0)
    pmb_tree = ["ROOT", [k for k, v in pmb_dict.items() if v == pmb_flags][0], [], []]

    pointer = 0x10
    # SUB
    helper.checkPointer(r_offset, pointer)
    (m_offset_list, pointer) = helper.getOffsetAddress(source, r_m_size, pointer)
    (pmb_tree[2], pointer) = importPmbMAIN(source, pmb_tree[2], chr_size, pmb_flags, m_offset_list, pointer)
    # IMG
    helper.checkPointer(r_img_offset, pointer)
    img_bin = None
    if r_img_size > 0:
        img_bin = importPmbPBIN(source, pmb_flags, r_img_size, pointer)
    return pmb_tree, img_bin


def importPmbMAIN(source, pmb_tree, chr_size, pmb_flags, offset_list, pointer):
    enc = 'euc_jp'
    for i in range(len(offset_list)):
        m_pointer = 0
        m_label = helper.getName(source, offset_list[i], enc, 0)  # ラベル
        m_pointer += chr_size
        m_s_size = helper.unpackOneFormat("L", source, offset_list[i] + m_pointer, 0)  # 次のアドレスの数
        m_pointer += 4
        m_s_offset = helper.unpackOneFormat("L", source, offset_list[i] + m_pointer, 0)  # 次のアドレス
        m_pointer += 4
        m_layer_size = helper.unpackOneFormat("L", source, offset_list[i] + m_pointer, 0)  # 次のアドレスの数
        m_pointer += 4
        m_layer_offset = helper.unpackOneFormat("L", source, offset_list[i] + m_pointer, 0)  # 次のアドレス
        m_pointer += 4

        pmb_tree.append([['MAIN', m_label], [], []])

        pointer += m_pointer

        helper.checkPointer(m_s_offset, pointer)
        (s_offset_list, pointer) = helper.getOffsetAddress(source, m_s_size, pointer)
        (pmb_tree[i][1], pointer) = importPmbSUB(source, pmb_tree[i][1], chr_size, pmb_flags, s_offset_list, pointer)

        helper.checkPointer(m_layer_offset, pointer)
        (layer_offset_list, pointer) = helper.getOffsetAddress(source, m_layer_size, pointer)
        (pmb_tree[i][2], pointer) = importPmbLAYER(source, pmb_tree[i][2], chr_size, pmb_flags, layer_offset_list,
                                                   pointer)
    return pmb_tree, pointer


def importPmbSUB(source, pmb_tree, chr_size, pmb_flags, offset_list, pointer):
    enc = 'euc_jp'
    for i in range(len(offset_list)):
        s_pointer = 0
        s_label_1 = helper.getName(source, offset_list[i], enc, 0)
        s_pointer += chr_size
        s_flags = helper.unpackOneFormat("L", source, offset_list[i] + s_pointer, 0)
        s_pointer += 4
        s_unk_1 = helper.unpackOneFormat("L", source, offset_list[i] + s_pointer, 0)
        s_pointer += 4
        s_unk_2 = helper.unpackOneFormat("L", source, offset_list[i] + s_pointer, 0)
        s_pointer += 4
        s_unk_3 = helper.unpackOneFormat("L", source, offset_list[i] + s_pointer, 0)
        s_pointer += 4
        s_unk_4 = helper.unpackOneFormat("L", source, offset_list[i] + s_pointer, 0)
        s_pointer += 4
        s_unk_5 = helper.unpackOneFormat("L", source, offset_list[i] + s_pointer, 0)
        s_pointer += 4
        if (pmb_flags & 0x4) != 0:
            s_func_offset = helper.unpackOneFormat("L", source, offset_list[i] + s_pointer, 0)
            s_pointer += 4
        else:
            s_func_offset = 0
        if (pmb_flags & 0x8) != 0:
            ss_offset = helper.unpackOneFormat("L", source, offset_list[i] + s_pointer, 0)
            s_pointer += 4
        else:
            ss_offset = 0
        s_image_offset = helper.unpackOneFormat("L", source, offset_list[i] + s_pointer, 0)
        s_pointer += 4
        s_box_offset = helper.unpackOneFormat("L", source, offset_list[i] + s_pointer, 0)
        s_pointer += 4
        s_text_offset = helper.unpackOneFormat("L", source, offset_list[i] + s_pointer, 0)
        s_pointer += 4

        pmb_tree.append([['SUB', s_label_1, s_flags, s_unk_1, s_unk_2, s_unk_3, s_unk_4, s_unk_5],
                         [], [], [], [], []])
        pointer += s_pointer
        if (s_flags & 0x30000) == 0x10000 and (pmb_flags & 0x4) != 0:
            helper.checkPointer(s_func_offset, pointer)
            (pmb_tree[i][1], pointer) = importPmbFUNC(source, pmb_flags, pointer)
        if (s_flags & 8) != 0 and (pmb_flags & 0x8) != 0:
            helper.checkPointer(ss_offset, pointer)
            (pmb_tree[i][2], pointer) = importPmbSUB(source, pmb_tree[i][2], chr_size, pmb_flags, [pointer], pointer)
        if (s_flags & 1) != 0:
            helper.checkPointer(s_image_offset, pointer)
            (pmb_tree[i][3], pointer) = importPmbIMAGE(source, pointer)
        if (s_flags & 2) != 0:
            helper.checkPointer(s_box_offset, pointer)
            (pmb_tree[i][4], pointer) = importPmbBOX(source, pointer)
        if (s_flags & 4) != 0:
            helper.checkPointer(s_text_offset, pointer)
            (pmb_tree[i][5], pointer) = importPmbTEXT(source, pmb_flags, pointer)
    return pmb_tree, pointer


def importPmbFUNC(source, pmb_flags, pointer):
    enc = checkEncodingFromPmbFlags(pmb_flags)
    func_label_offset = helper.unpackOneFormat("L", source, pointer, 0)
    func_label = helper.getName(source, func_label_offset, enc, 0)
    pmb_tree = ['FUNC', func_label]
    pointer += 0x4 + helper.getLen(func_label, enc)
    return pmb_tree, pointer


def importPmbIMAGE(source, pointer):
    i_image_id = helper.unpackOneFormat("L", source, pointer, 0)
    i_unk_2 = helper.unpackOneFormat("L", source, pointer + 0x4, 0)
    i_unk_3 = helper.unpackOneFormat("L", source, pointer + 0x8, 0)
    i_unk_4 = helper.unpackOneFormat("L", source, pointer + 0xC, 0)
    i_unk_5 = helper.unpackOneFormat("L", source, pointer + 0x10, 0)
    i_unk_6 = helper.unpackOneFormat("L", source, pointer + 0x14, 0)
    i_unk_7 = helper.unpackOneFormat("L", source, pointer + 0x18, 0)
    i_unk_8 = helper.unpackOneFormat("L", source, pointer + 0x1C, 0)
    i_unk_9 = helper.unpackOneFormat("L", source, pointer + 0x20, 0)
    pmb_tree = ['IMAGE', i_image_id, i_unk_2, i_unk_3, i_unk_4, i_unk_5,
                i_unk_6, i_unk_7, i_unk_8, i_unk_9]
    pointer += 0x24
    return pmb_tree, pointer


def importPmbBOX(source, pointer):
    box_unk_1 = helper.unpackOneFormat("L", source, pointer, 0)
    box_unk_2 = helper.unpackOneFormat("L", source, pointer + 0x4, 0)
    box_unk_3 = helper.unpackOneFormat("L", source, pointer + 0x8, 0)
    box_unk_4 = helper.unpackOneFormat("L", source, pointer + 0xC, 0)
    pmb_tree = ['BOX', box_unk_1, box_unk_2, box_unk_3, box_unk_4]
    pointer += 0x10
    return pmb_tree, pointer


def importPmbTEXT(source, pmb_flags, pointer):
    enc = checkEncodingFromPmbFlags(pmb_flags)
    text_pointer = 0
    text_unk_1 = helper.unpackOneFormat("B", source, pointer, 0)
    text_pointer += 2
    text_unk_2 = helper.unpackOneFormat("B", source, pointer + text_pointer, 0)
    text_pointer += 2
    if (pmb_flags & 0x10) != 0:
        text_unk_3 = helper.unpackOneFormat("L", source, pointer + text_pointer, 0)
        text_pointer += 4
    else:
        text_unk_3 = 0
    text_label1_offset = helper.unpackOneFormat("L", source, pointer + text_pointer, 0)
    text_pointer += 4
    text_label2_offset = helper.unpackOneFormat("L", source, pointer + text_pointer, 0)
    text_pointer += 4

    text_label1 = helper.getName(source, text_label1_offset, enc, 0)
    text_label2 = helper.getName(source, text_label2_offset, enc, 0)
    pmb_tree = ['TEXT1', text_unk_1, text_unk_2, text_unk_3, text_label1, text_label2]
    pointer += text_pointer + helper.getLen(text_label1, enc) + helper.getLen(text_label2, enc)
    return pmb_tree, pointer


def importPmbLAYER(source, pmb_tree, chr_size, pmb_flags, offset_list, pointer):
    enc = 'euc_jp'
    for i in range(len(offset_list)):
        layer_pointer = 0
        layer_label = helper.getName(source, offset_list[i], enc, 0)
        layer_pointer += chr_size
        layer_s1_size = helper.unpackOneFormat("L", source, offset_list[i] + layer_pointer, 0)
        layer_pointer += 4
        layer_s1_offset = helper.unpackOneFormat("L", source, offset_list[i] + layer_pointer, 0)
        layer_pointer += 4
        layer_s2_size = helper.unpackOneFormat("L", source, offset_list[i] + layer_pointer, 0)
        layer_pointer += 4
        layer_s2_offset = helper.unpackOneFormat("L", source, offset_list[i] + layer_pointer, 0)
        layer_pointer += 4

        pmb_tree.append([['LAYER', layer_label], [], []])

        pointer += layer_pointer

        helper.checkPointer(layer_s1_offset, pointer)
        (s1_offset_list, pointer) = helper.getOffsetAddress(source, layer_s1_size, pointer)
        (pmb_tree[i][1], pointer) = importPmbSUB(source, pmb_tree[i][1], chr_size, pmb_flags, s1_offset_list, pointer)

        helper.checkPointer(layer_s2_offset, pointer)
        (s2_offset_list, pointer) = helper.getOffsetAddress(source, layer_s2_size, pointer)
        (pmb_tree[i][2], pointer) = importPmbSUB(source, pmb_tree[i][2], chr_size, pmb_flags, s2_offset_list, pointer)

    return pmb_tree, pointer


def importPmbPBIN(pmb, pmb_flags, img_count, pointer):
    b_i_h = helper.setZeroPaddingForLabel("PBIN", 4, "euc_jp")
    b_i_l = b''
    b_i_m = b''
    b_i_h += (0).to_bytes(4, byteorder="little")
    b_i_h += img_count.to_bytes(4, byteorder="little")
    b_i_h += (0x10).to_bytes(4, byteorder="little")

    # Defining IMG list and offset
    img_size_list = []
    img_offset_list = []
    base_ofs = pointer - 0x10
    for i in range(img_count):
        img_size = helper.unpackOneFormat("L", pmb, pointer, 0)
        img_offset = helper.unpackOneFormat("L", pmb, pointer + 0x4, 0)

        # Creating a list of IMG
        img_size_list.append(img_size)
        img_offset_list.append(img_offset)
        pointer += 0x8

    # Creating an offset list for PBIN files
    img_out_offset_list = [n - base_ofs for n in img_offset_list]

    # Create binary data for PBIN file
    padding = 0  # count of padding data at the end of gz file.
    for i in range(img_count):
        # Set padding
        img_header = pmb[img_offset_list[i]:img_offset_list[i] + 4]
        # gz or img
        if img_header[:2] == b'\x1f\x8b':
            if pointer % 4 != 0:
                padding += 4 - (pointer % 4)
                pointer += 4 - (pointer % 4)
        elif img_header == b'Tex1':
            if pointer % 0x10 != 0:
                padding += 0x10 - (pointer % 0x10)
                pointer += 0x10 - (pointer % 0x10)
        else:
            raise ValueError("error!")
        # Create binary data for IMG list
        b_i_l += img_size_list[i].to_bytes(4, byteorder="little")
        b_i_l += (img_out_offset_list[i] - padding).to_bytes(4, byteorder="little")

        # Acquisition of img file (if statement is processed when i+1 is out of range)
        if i + 1 != img_count:
            img = pmb[img_offset_list[i]:img_offset_list[i + 1]]
        else:
            img = pmb[img_offset_list[i]:]

        # gz or img
        if img[:2] == b'\x1f\x8b':
            check_padding = helper.unpackOneFormat("L", img[-4:], 0, 0)
            while check_padding != img_size_list[i]:
                img = img[:-1]
                check_padding = helper.unpackOneFormat("L", img[-4:], 0, 0)
                padding += 1
                pointer += 1
        elif img[:4] == b'Tex1':
            pass
        else:
            raise ValueError("error!")

        pointer += len(img)

        if i + 1 == img_count and pointer % 4 != 0 and (pmb_flags & 0x40) != 0:
            check_padding = 4 - (pointer % 4)
            pointer -= check_padding
            img = img[:pointer]
        # Add img to binary
        b_i_m += img

    # Add all binary elements.
    b_i = b_i_h + b_i_l + b_i_m
    return b_i


def setPmbGetAddress(pmb, offset, size, pointer):
    l_address = []
    for i in range(size):
        l_address.append(helper.unpackOneFormat("L", pmb, offset, 0))
        offset += 0x04
        pointer += 0x04
    return l_address, pointer


def checkEncodingFromPmbFlags(pmb_flags):
    if (pmb_flags & 0x20) != 0:
        return "euc_jp"
    else:
        return "shift_jis"


def exportPmb(pmb_tree, img_bin, pmb_flags):
    if (pmb_flags & 0x1) != 0:
        chr_size = 0x20
    elif (pmb_flags & 0x2) != 0:
        chr_size = 0x40
    else:
        chr_size = 0x10
    m_size = len(pmb_tree[2])
    b_r = m_size.to_bytes(4, byteorder='little')
    pointer = 0x10
    b_r += pointer.to_bytes(4, byteorder='little')

    b_m = b""
    b_m_offset = b""
    m_offset_list = []
    pointer += 0x4 * m_size
    for i in range(m_size):
        m_offset_list.append(pointer.to_bytes(4, byteorder='little'))
        (b, pointer) = exportPmbMAIN(pmb_tree[2][i], chr_size, pmb_flags, pointer)
        b_m += b

    img_size = 0
    img_offset = 0
    if img_bin is not None:
        img_pointer = 0x8
        img_size = helper.unpackOneFormat("L", img_bin, img_pointer, 0)
        img_pointer += 0x4
        img_offset = helper.unpackOneFormat("L", img_bin, img_pointer, 0)
        img_pointer += (img_offset - 0x10) + 0x4

    b_r += img_size.to_bytes(4, byteorder='little')
    b_r += pointer.to_bytes(4, byteorder='little')
    b_img = b""
    if img_bin is not None:
        b_img = exportPmbPBIN(img_bin, pmb_flags, img_size, img_offset, pointer)
    for i in range(m_size):
        b_m_offset += m_offset_list[i]
    b_r += b_m_offset + b_m + b_img
    return b_r


def exportPmbMAIN(pmb_tree, chr_size, pmb_flags, pointer):
    enc = 'euc_jp'
    b_m = b""
    b_m += helper.setZeroPaddingForLabel(pmb_tree[0][1], chr_size, enc)  # MAIN_label
    s_size = len(pmb_tree[1])
    b_m += s_size.to_bytes(4, byteorder='little')  # MAIN_SUB_size
    pointer += chr_size + (0x4 * 4)
    b_m += pointer.to_bytes(4, byteorder='little')  # MAIN_SUB_offset

    b_s = b""
    b_s_offset = b""
    s_offset_list = []
    pointer += 0x4 * s_size
    for i in range(s_size):
        s_offset_list.append(pointer.to_bytes(4, byteorder='little'))
        (b, pointer) = exportPmbSUB(pmb_tree[1][i], chr_size, pmb_flags, pointer)
        b_s += b
    for i in range(s_size):
        b_s_offset += s_offset_list[i]

    layer_size = len(pmb_tree[2])
    b_m += layer_size.to_bytes(4, byteorder='little')  # MAIN_LAYER_size
    b_m += pointer.to_bytes(4, byteorder='little')  # MAIN_LAYER_offset

    b_layer = b""
    b_layer_offset = b""
    layer_offset_list = []
    pointer += 0x4 * layer_size
    for i in range(layer_size):
        layer_offset_list.append(pointer.to_bytes(4, byteorder='little'))
        (b, pointer) = exportPmbLAYER(pmb_tree[2][i], chr_size, pmb_flags, pointer)
        b_layer += b
    for i in range(layer_size):
        b_layer_offset += layer_offset_list[i]
    b_m += b_s_offset + b_s + b_layer_offset + b_layer
    return b_m, pointer


def exportPmbSUB(pmb_tree, chr_size, pmb_flags, pointer):
    enc = 'euc_jp'
    b_s = b""
    b_s_func = b""
    b_ss = b""
    b_s_image = b""
    b_s_box = b""
    b_s_text = b""
    b_s += helper.setZeroPaddingForLabel(pmb_tree[0][1], chr_size, enc)
    s_flags = pmb_tree[0][2]
    b_s += s_flags.to_bytes(4, byteorder='little')
    b_s += pmb_tree[0][3].to_bytes(4, byteorder='little')
    b_s += pmb_tree[0][4].to_bytes(4, byteorder='little')
    b_s += pmb_tree[0][5].to_bytes(4, byteorder='little')
    b_s += pmb_tree[0][6].to_bytes(4, byteorder='little')
    b_s += pmb_tree[0][7].to_bytes(4, byteorder='little')
    if (pmb_flags & 0x8) != 0:
        pointer += 0x4
    if (pmb_flags & 0x4) != 0:
        pointer += 0x4
    pointer += chr_size + 0x24

    if (pmb_flags & 0x4) != 0:
        if (s_flags & 0x30000) == 0x10000:
            b_s += pointer.to_bytes(4, byteorder='little')
            (b_s_func, pointer) = exportPmbFUNC(pmb_tree[1], pmb_flags, pointer)
        else:
            b_s += (0).to_bytes(4, byteorder='little')
    if (pmb_flags & 0x8) != 0:
        if (s_flags & 8) != 0:
            b_s += pointer.to_bytes(4, byteorder='little')
            (b_ss, pointer) = exportPmbSUB(pmb_tree[2][0], chr_size, pmb_flags, pointer)
        else:
            b_s += (0).to_bytes(4, byteorder='little')
    if (s_flags & 1) != 0:
        b_s += pointer.to_bytes(4, byteorder='little')
        (b_s_image, pointer) = exportPmbIMAGE(pmb_tree[3], pointer)
    else:
        b_s += (0).to_bytes(4, byteorder='little')
    if (s_flags & 2) != 0:
        b_s += pointer.to_bytes(4, byteorder='little')
        (b_s_box, pointer) = exportPmbBOX(pmb_tree[4], pointer)
    else:
        b_s += (0).to_bytes(4, byteorder='little')
    if (s_flags & 4) != 0:
        b_s += pointer.to_bytes(4, byteorder='little')
        (b_s_text, pointer) = exportPmbTEXT(pmb_tree[5], pmb_flags, pointer)
    else:
        b_s += (0).to_bytes(4, byteorder='little')

    b_s += b_s_func + b_ss + b_s_image + b_s_box + b_s_text
    return b_s, pointer


def exportPmbFUNC(pmb_tree, pmb_flags, pointer):
    enc = checkEncodingFromPmbFlags(pmb_flags)
    pointer += 0x4
    b_func = pointer.to_bytes(4, byteorder='little')  # FUNC_label_offset
    func_label = pmb_tree[1]  # FUNC_label
    b_func += helper.setZeroPaddingForLabel(func_label, helper.getLen(func_label, enc), enc)
    pointer += helper.getLen(func_label, enc)
    return b_func, pointer


def exportPmbIMAGE(pmb_tree, pointer):
    b_image = pmb_tree[1].to_bytes(4, byteorder='little')
    b_image += pmb_tree[2].to_bytes(4, byteorder='little')
    b_image += pmb_tree[3].to_bytes(4, byteorder='little')
    b_image += pmb_tree[4].to_bytes(4, byteorder='little')
    b_image += pmb_tree[5].to_bytes(4, byteorder='little')
    b_image += pmb_tree[6].to_bytes(4, byteorder='little')
    b_image += pmb_tree[7].to_bytes(4, byteorder='little')
    b_image += pmb_tree[8].to_bytes(4, byteorder='little')
    b_image += pmb_tree[9].to_bytes(4, byteorder='little')
    pointer += 0x24
    return b_image, pointer


def exportPmbBOX(pmb_tree, pointer):
    b_box = pmb_tree[1].to_bytes(4, byteorder='little')
    b_box += pmb_tree[2].to_bytes(4, byteorder='little')
    b_box += pmb_tree[3].to_bytes(4, byteorder='little')
    b_box += pmb_tree[4].to_bytes(4, byteorder='little')
    pointer += 0x10
    return b_box, pointer


def exportPmbTEXT(pmb_tree, pmb_flags, pointer):
    enc = checkEncodingFromPmbFlags(pmb_flags)
    b_text = pmb_tree[1].to_bytes(2, byteorder='little')
    b_text += pmb_tree[2].to_bytes(2, byteorder='little')
    if (pmb_flags & 0x10) != 0:
        b_text += pmb_tree[3].to_bytes(4, byteorder='little')
        pointer += 0x4
    pointer += 0xC
    text_label1 = pmb_tree[4]
    text_label2 = pmb_tree[5]

    b_text += pointer.to_bytes(4, byteorder='little')
    pointer += helper.getLen(text_label1, enc)
    b_text += pointer.to_bytes(4, byteorder='little')

    b_text += helper.setZeroPaddingForLabel(text_label1, helper.getLen(text_label1, enc), enc)
    b_text += helper.setZeroPaddingForLabel(text_label2, helper.getLen(text_label2, enc), enc)

    pointer += helper.getLen(text_label2, enc)
    return b_text, pointer


def exportPmbLAYER(pmb_tree, chr_size, pmb_flags, pointer):
    enc = 'euc_jp'
    b_layer = b""
    b_layer += helper.setZeroPaddingForLabel(pmb_tree[0][1], chr_size, enc)  # LAYER_label

    s1_size = len(pmb_tree[1])
    b_layer += s1_size.to_bytes(4, byteorder='little')  # LAYER_SUB1_size
    pointer += chr_size + 0x10
    b_layer += pointer.to_bytes(4, byteorder='little')  # LAYER_SUB1_offset

    b_s1 = b""
    b_s1_offset = b""
    s1_offset_list = []
    pointer += 0x4 * s1_size
    for i in range(s1_size):
        s1_offset_list.append(pointer.to_bytes(4, byteorder='little'))
        (b, pointer) = exportPmbSUB(pmb_tree[1][i], chr_size, pmb_flags, pointer)
        b_s1 += b
    for i in range(s1_size):
        b_s1_offset += s1_offset_list[i]

    s2_size = len(pmb_tree[2])
    b_layer += s2_size.to_bytes(4, byteorder='little')  # LAYER_SUB2_size
    b_layer += pointer.to_bytes(4, byteorder='little')  # LAYER_SUB2_offset

    b_s2 = b""
    b_s2_offset = b""
    s2_offset_list = []
    pointer += 0x4 * s2_size
    for i in range(s2_size):
        s2_offset_list.append(pointer.to_bytes(4, byteorder='little'))
        (b, pointer) = exportPmbSUB(pmb_tree[2][i], chr_size, pmb_flags, pointer)
        b_s2 += b
    for i in range(s2_size):
        b_s2_offset += s2_offset_list[i]
    b_layer += b_s1_offset + b_s1 + b_s2_offset + b_s2
    return b_layer, pointer


def exportPmbPBIN(pbin, pmb_flags, nuber_of_img, pbin_offset, pointer):
    pbin_pointer = pbin_offset

    # Init binary data
    b_i_l = b''
    b_i_m = b''

    img_size_list = []
    img_offset_list = []
    img_out_offset_list = []
    for i in range(nuber_of_img):
        img_size = helper.unpackOneFormat("L", pbin, pbin_pointer, 0)
        img_offset = helper.unpackOneFormat("L", pbin, pbin_pointer + 0x4, 0)

        img_size_list.append(img_size)
        img_offset_list.append(img_offset)
        img_out_offset_list.append(img_offset + pointer - pbin_offset)
        pbin_pointer += 0x8

    padding = 0
    pointer += pbin_pointer - pbin_offset

    first_img_header = pbin[img_offset_list[0]:img_offset_list[0] + 4]
    if first_img_header[:2] == b'\x1f\x8b':
        (b_i_m, padding, pointer) = setPBINPadding(b_i_m, padding, pointer, 4)
    elif first_img_header == b'Tex1':
        (b_i_m, padding, pointer) = setPBINPadding(b_i_m, padding, pointer, 0x10)
    else:
        raise ValueError("error!")

    for i in range(nuber_of_img):
        # Create binary data for IMG list
        b_i_l += img_size_list[i].to_bytes(4, byteorder="little")
        b_i_l += (img_out_offset_list[i] + padding).to_bytes(4, byteorder="little")

        # Acquisition of img file (if statement is processed when i+1 is out of range)
        if i + 1 == nuber_of_img:
            img = pbin[img_offset_list[i]:]
        else:
            img = pbin[img_offset_list[i]:img_offset_list[i + 1]]

        pointer += len(img)
        # gz or img
        if i + 1 != nuber_of_img:
            next_img_header = pbin[img_offset_list[i + 1]:img_offset_list[i + 1] + 4]
            if next_img_header[:2] == b'\x1f\x8b':
                (img, padding, pointer) = setPBINPadding(img, padding, pointer, 4)
            elif next_img_header == b'Tex1':
                (img, padding, pointer) = setPBINPadding(img, padding, pointer, 0x10)
            else:
                raise ValueError("error!")
        elif (pmb_flags & 0x40) != 0:
            (img, padding, pointer) = setPBINPadding(img, padding, pointer, 4)
        # Add img to binary
        b_i_m += img
    # Add all binary elements.
    b_img = b_i_l + b_i_m
    return b_img


def setPBINPadding(img, padding, pointer, num):
    if pointer % num != 0:
        p = num - (pointer % num)
        img += b'\x50' * p
        padding += p
        pointer += p
    return img, padding, pointer


def exportPmbControlFlags(pmb_tree, output_pmb_flags):
    input_name = pmb_tree[1]
    output_name = [k for k, v in pmb_dict.items() if v == output_pmb_flags][0]
    for i in range(len(pmb_control_flags_list)):
        if pmb_control_flags_list[i][0] == [input_name, output_name]:
            pmb_tree = exportPmbControlFlagsMAIN(pmb_tree, pmb_control_flags_list[i][1])
    return pmb_tree


def exportPmbControlFlagsMAIN(pmb_tree, pcf_list):
    for i in range(len(pmb_tree[2])):
        pmb_tree[2][i][1] = exportPmbControlFlagsSUB(pmb_tree[2][i][1], pcf_list)
        for j in range(len(pmb_tree[2][i][2])):
            pmb_tree[2][i][2][j][1] = exportPmbControlFlagsSUB(pmb_tree[2][i][2][j][1], pcf_list)
            pmb_tree[2][i][2][j][2] = exportPmbControlFlagsSUB(pmb_tree[2][i][2][j][2], pcf_list)
    return pmb_tree


def exportPmbControlFlagsSUB(pmb_tree, pcf_list):
    for i in range(len(pmb_tree)):
        pmb_control_flags = pmb_tree[i][0][2]
        if pmb_control_flags & pcf_list[0] == pcf_list[0] and pmb_control_flags & pcf_list[1] == 0:
            pmb_tree[i][0][2] = pmb_control_flags - pcf_list[0] + pcf_list[1]
        if len(pmb_tree[i][2]) != 0:
            pmb_tree[i][2] = exportPmbControlFlagsSUB(pmb_tree[i][2], pcf_list)
    return pmb_tree


def checkPmb(path, pmb_flags):
    pmb_source = path.read_bytes()
    # Import PMB
    (pmb_tree, pbin) = importPmb(pmb_source, pmb_flags)
    # Export PMB
    pmb_out = exportPmb(pmb_tree, pbin, pmb_flags)

    # Check for correct data
    if pmb_out == pmb_source:
        return True
    else:
        return False
