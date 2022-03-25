import helper

mbl_dict = {
    'mbl10': 0x0,
    'mbl20': 0x19,
    'mbl21': 0x1D,
    'mbl40': 0x1E,
}

"""
0x01: chr_size = 0x20
0x02: chr_size = 0x40
0x04: Presence of variable "m_function_label
0x08: Presence or absence of variable "m_common_label
0x10: Presence of variable "s_function_label
"""

mbl_dict_list = list(mbl_dict.keys())

mbl_control_flags_list = [[['mbl21', 'mbl40'], [0x10, 0x40]],
                          [['mbl21', 'mbl40'], [0x20, 0x100]],
                          [['mbl20', 'mbl21'], [0x0, 0x20]],
                          [['mbl20', 'mbl40'], [0x0, 0x100]],
                          [['mbl10', 'mbl21'], [0x0, 0x20]],
                          [['mbl10', 'mbl40'], [0x0, 0x100]],
                          [['mbl40', 'mbl21'], [0x40, 0x10]],
                          [['mbl40', 'mbl21'], [0x100, 0x20]],
                          [['mbl21', 'mbl20'], [0x20, 0x0]],
                          [['mbl40', 'mbl20'], [0x100, 0x0]],
                          [['mbl21', 'mbl10'], [0x20, 0x0]],
                          [['mbl40', 'mbl10'], [0x100, 0x0]]
                          ]


def importMbl(source, mbl_flags):
    if (mbl_flags & 0x1) != 0:
        chr_size = 0x20
    elif (mbl_flags & 0x2) != 0:
        chr_size = 0x40
    else:
        chr_size = 0x10
    r_size = helper.unpackOneFormat("L", source, 0x00, 0)
    r_offset = helper.unpackOneFormat("L", source, 0x04, 0)
    mbl_tree = ["ROOT", [k for k, v in mbl_dict.items() if v == mbl_flags][0], []]
    pointer = 0x8
    helper.checkPointer(r_offset, pointer)
    (MAIN_offset_list, pointer) = helper.getOffsetAddress(source, r_size, pointer)
    (mbl_tree[2], pointer) = importMblMAIN(source, mbl_tree[2], chr_size, mbl_flags, MAIN_offset_list, pointer)
    return mbl_tree


def importMblMAIN(source, mbl_tree, chr_size, mbl_flags, offset_list, pointer):
    for i in range(len(offset_list)):
        m_pointer = 0
        m_label = helper.getName(source, offset_list[i], 'euc_jp', 0)  # ラベル
        m_pointer += chr_size
        m_pmb_id = helper.unpackOneFormat("H", source, offset_list[i] + m_pointer, 0)
        m_pointer += 2
        m_button_flag = helper.unpackOneFormat("H", source, offset_list[i] + m_pointer, 0)
        m_pointer += 2
        if (mbl_flags & 0x8) != 0:
            m_common_label = helper.getName(source, offset_list[i] + m_pointer, 'euc_jp', 0)
            m_pointer += chr_size
        else:
            m_common_label = ""
        m_return_label = helper.getName(source, offset_list[i] + m_pointer, 'euc_jp', 0)
        m_pointer += chr_size
        if (mbl_flags & 0x4) != 0:
            m_function_label = helper.getName(source, offset_list[i] + m_pointer, 'euc_jp', 0)
            m_pointer += chr_size
        else:
            m_function_label = ""
        m_sub_size = helper.unpackOneFormat("L", source, offset_list[i] + m_pointer, 0)
        m_pointer += 4
        m_sub_offset = helper.unpackOneFormat("L", source, offset_list[i] + m_pointer, 0)
        m_pointer += 4

        mbl_tree.append([['MAIN', m_label, m_pmb_id, m_button_flag,
                          m_common_label, m_return_label, m_function_label], []])

        pointer += m_pointer
        helper.checkPointer(m_sub_offset, pointer)
        (s_offset_list, pointer) = helper.getOffsetAddress(source, m_sub_size, pointer)
        (mbl_tree[i][1], pointer) = importMblSUB(source, mbl_tree[i][1], chr_size, mbl_flags, s_offset_list, pointer)
    return mbl_tree, pointer


def importMblSUB(source, mbl_tree, chr_size, mbl_flags, offset_list, pointer):
    for i in range(len(offset_list)):
        s_pointer = 0
        s_label = helper.getName(source, offset_list[i], 'euc_jp', 0)
        s_pointer += chr_size
        s_layer_label1 = helper.getName(source, offset_list[i] + s_pointer, 'euc_jp', 0)
        s_pointer += chr_size
        s_layer_label2 = helper.getName(source, offset_list[i] + s_pointer, 'euc_jp', 0)
        s_pointer += chr_size
        if (mbl_flags & 0x10) != 0:
            s_function_label = helper.getName(source, offset_list[i] + s_pointer, 'euc_jp', 0)
            s_pointer += chr_size
        else:
            s_function_label = ""
        s_return_label = helper.getName(source, offset_list[i] + s_pointer, 'euc_jp', 0)
        s_pointer += chr_size
        s_pmb_id = helper.unpackOneFormat("H", source, offset_list[i] + s_pointer, 0)
        s_pointer += 2
        s_button_flag = helper.unpackOneFormat("H", source, offset_list[i] + s_pointer, 0)
        s_pointer += 2
        ss_size = helper.unpackOneFormat("L", source, offset_list[i] + s_pointer, 0)
        s_pointer += 4
        ss_offset = helper.unpackOneFormat("L", source, offset_list[i] + s_pointer, 0)
        s_pointer += 4

        mbl_tree.append([['SUB', s_label, s_layer_label1, s_layer_label2, s_function_label,
                          s_return_label, s_pmb_id, s_button_flag], []])

        pointer += s_pointer
        helper.checkPointer(ss_offset, pointer)
        (ss_offset_list, pointer) = helper.getOffsetAddress(source, ss_size, pointer)
        (mbl_tree[i][1], pointer) = importMblSUB(source, mbl_tree[i][1], chr_size, mbl_flags, ss_offset_list, pointer)
    return mbl_tree, pointer


def exportMbl(mbl_tree, mbl_flags):
    if (mbl_flags & 0x1) != 0:
        chr_size = 0x20
    elif (mbl_flags & 0x2) != 0:
        chr_size = 0x40
    else:
        chr_size = 0x10

    m_size = len(mbl_tree[2])
    b_r = m_size.to_bytes(4, byteorder='little')
    pointer = 0x8
    b_r += pointer.to_bytes(4, byteorder='little')

    b_m = b""
    b_m_offset = b""
    m_offset_list = []
    pointer += 0x4 * m_size
    for i in range(m_size):
        m_offset_list.append(pointer.to_bytes(4, byteorder='little'))
        (b, pointer) = exportMblMAIN(mbl_tree[2][i], chr_size, mbl_flags, pointer)
        b_m += b
    for i in range(m_size):
        b_m_offset += m_offset_list[i]
    b_r += b_m_offset + b_m
    return b_r


def exportMblMAIN(mbl_tree, chr_size, mbl_flags, pointer):
    b_m = b""
    m_pointer = 0
    b_m += helper.setZeroPaddingForLabel(mbl_tree[0][1], chr_size, 'euc_jp')
    m_pointer += chr_size
    b_m += mbl_tree[0][2].to_bytes(2, byteorder='little')
    m_pointer += 2
    b_m += mbl_tree[0][3].to_bytes(2, byteorder='little')
    m_pointer += 2
    if (mbl_flags & 0x8) != 0:
        b_m += helper.setZeroPaddingForLabel(mbl_tree[0][4], chr_size, 'euc_jp')
        m_pointer += chr_size
    b_m += helper.setZeroPaddingForLabel(mbl_tree[0][5], chr_size, 'euc_jp')
    m_pointer += chr_size
    if (mbl_flags & 0x4) != 0:
        b_m += helper.setZeroPaddingForLabel(mbl_tree[0][6], chr_size, 'euc_jp')
        m_pointer += chr_size
    s_size = len(mbl_tree[1])
    b_m += s_size.to_bytes(4, byteorder='little')
    m_pointer += 4 + 4
    pointer += m_pointer
    b_m += pointer.to_bytes(4, byteorder='little')
    b_s = b""
    b_s_offset = b""
    s_offset_list = []
    pointer += 0x4 * s_size
    for i in range(s_size):
        s_offset_list.append(pointer.to_bytes(4, byteorder='little'))
        (b, pointer) = exportMblSUB(mbl_tree[1][i], chr_size, mbl_flags, pointer)
        b_s += b
    for i in range(s_size):
        b_s_offset += s_offset_list[i]
    b_m += b_s_offset + b_s
    return b_m, pointer


def exportMblSUB(mbl_tree, chr_size, mbl_flags, pointer):
    b_s = b""
    s_pointer = 0
    b_s += helper.setZeroPaddingForLabel(mbl_tree[0][1], chr_size, 'euc_jp')
    s_pointer += chr_size
    b_s += helper.setZeroPaddingForLabel(mbl_tree[0][2], chr_size, 'euc_jp')
    s_pointer += chr_size
    b_s += helper.setZeroPaddingForLabel(mbl_tree[0][3], chr_size, 'euc_jp')
    s_pointer += chr_size
    if (mbl_flags & 0x10) != 0:
        b_s += helper.setZeroPaddingForLabel(mbl_tree[0][4], chr_size, 'euc_jp')
        s_pointer += chr_size
    b_s += helper.setZeroPaddingForLabel(mbl_tree[0][5], chr_size, 'euc_jp')
    s_pointer += chr_size
    b_s += mbl_tree[0][6].to_bytes(2, byteorder='little')
    s_pointer += 2
    b_s += mbl_tree[0][7].to_bytes(2, byteorder='little')
    s_pointer += 2
    ss_size = len(mbl_tree[1])
    b_s += ss_size.to_bytes(4, byteorder='little')
    s_pointer += 4 + 4
    pointer += s_pointer
    b_s += pointer.to_bytes(4, byteorder='little')

    b_ss = b""
    b_ss_offset = b""
    ss_offset_list = []
    pointer += 0x4 * ss_size
    for i in range(ss_size):
        ss_offset_list.append(pointer.to_bytes(4, byteorder='little'))
        (b, pointer) = exportMblSUB(mbl_tree[1][i], chr_size, mbl_flags, pointer)
        b_ss += b
    for i in range(ss_size):
        b_ss_offset += ss_offset_list[i]
    b_s += b_ss_offset + b_ss
    return b_s, pointer


def exportMblControlFlags(mbl_tree, output_pmb_flags):
    input_name = mbl_tree[1]
    output_name = [k for k, v in mbl_dict.items() if v == output_pmb_flags][0]
    for i in range(len(mbl_control_flags_list)):
        if mbl_control_flags_list[i][0] == [input_name, output_name]:
            mbl_tree = exportMblControlFlagsMAIN(mbl_tree, mbl_control_flags_list[i][1])
    return mbl_tree


def exportMblControlFlagsMAIN(mbl_tree, mcf_list):
    for i in range(len(mbl_tree[2])):
        mbl_control_flags = mbl_tree[2][i][0][3]
        if mbl_control_flags & mcf_list[0] == mcf_list[0] and mbl_control_flags & mcf_list[1] == 0:
            mbl_tree[2][i][0][3] = mbl_control_flags - mcf_list[0] + mcf_list[1]
    return mbl_tree


def checkMbl(path, mbl_flags):
    mbl_source = path.read_bytes()
    # Import MBL
    mbl_tree = importMbl(mbl_source, mbl_flags)
    # Export MBL
    mbl_out = exportMbl(mbl_tree, mbl_flags)

    # Check for correct data
    if mbl_out == mbl_source:
        return True
    else:
        return False
