import helper
import gzip
import io
import re


def unpackPIMG(p_input, p_output_dir, is_ungzip):
    print(p_input.name + '\t', end='')
    with p_input.open('rb') as infile:
        pmbbin = infile.read()

    # Create directory
    p_output_dir = helper.makeOutputDir(p_input, p_output_dir) / p_input.stem
    if p_output_dir.is_dir() is False:
        p_output_dir.mkdir()

    # Define Variables
    header = pmbbin[0:4]
    if header != b'PBIN':
        print('May not be PMBBIN data.')
    img_count = helper.unpackOneFormat("L", pmbbin, 0x8, 0)
    pimg_offset = helper.unpackOneFormat("L", pmbbin, 0xC, 0)
    img_size_list = []
    img_offset_list = []

    # Unpack PMBBIN
    ptr = pimg_offset
    for i in range(img_count):
        img_size = helper.unpackOneFormat("L", pmbbin, ptr, 0)
        img_offset = helper.unpackOneFormat("L", pmbbin, ptr + 0x4, 0)

        img_size_list.append(img_size)
        img_offset_list.append(img_offset)
        ptr += 0x8
    for i in range(img_count):
        if i != img_count - 1:
            img_data = pmbbin[img_offset_list[i]:img_offset_list[i + 1]]
        else:
            img_data = pmbbin[img_offset_list[i]:]

        # Check if data is img or gz
        img_header = img_data[0:4]
        if img_header[:2] == b'\x1f\x8b':
            extension = 'gz'
            with io.BytesIO(gzip.decompress(img_data)) as gzip_file:
                img_raw = gzip_file.read()
            if is_ungzip is True:  # check ungzip flag
                img_data = img_raw
                extension = 'img'
        elif img_header == b'Tex1':
            extension = 'img'
            img_raw = img_data
        else:
            raise ValueError('Incorrect image data exists. Count:{}'.format(i))

        # File length check and output file definition
        outfile_name = '{0:04}.{1}'.format(i, extension)
        if len(img_raw) != img_size_list[i]:
            print('The size of the image data does not match the size '
                             'written in the corresponding PMBBIN data. FileName:{}'.format(outfile_name))

        # Output gz,img files
        p_output_pimg = p_output_dir / outfile_name
        with p_output_pimg.open('wb') as outfile:
            outfile.write(img_data)
    print('Success')


def unpackPIMGRecursive(p_input, p_output_dir, is_ungzip):
    p_output_dir = helper.makeOutputDir(p_input, p_output_dir)

    input_path_list = list(p_input.rglob('*.bin'))
    for p in input_path_list:
        p_r = p.relative_to(p_input)
        p_o = p_output_dir / p_r.parents[0]
        if p_o.exists() is False:
            p_o.mkdir(parents=True, exist_ok=True)
        unpackPIMG(p, p_o, is_ungzip)


def repackPIMG(p_input_dir, p_output_dir):
    print(p_input_dir.name + '\t', end='')
    # List img,gz files from input directory
    img_file_list = [p for p in p_input_dir.glob('*') if re.search('(?<!\d)\d{4}(?!\d)\.(img|gz)', str(p))]

    # Variable Definitions
    ptr = 0x10
    b_img_header = b'PBIN'
    b_img_header += (0).to_bytes(4, byteorder="little")
    b_img_header += len(img_file_list).to_bytes(4, byteorder='little')
    b_img_header += ptr.to_bytes(4, byteorder="little")
    b_img_offsets = b''
    b_img_data = b''
    ptr += len(img_file_list) * 8

    # Create a list for PMBBIN file creation
    img_raw_size_list = []
    img_offset_list = []
    for p_img in img_file_list:
        with p_img.open('rb') as infile:
            img = infile.read()

        img_header = img[0:4]
        img_size = len(img)
        extension = p_img.suffix[1:]
        if img_header[0:2] == b'\x1f\x8b' and extension == 'gz':
            with io.BytesIO(gzip.decompress(img)) as gzip_file:
                img_raw_size = len(gzip_file.read())
        elif img_header == b'Tex1' and extension == 'img':
            img_raw_size = img_size
        else:
            raise ValueError('Incorrect image data exists. Count:{}'.format(p_img.name))
        img_raw_size_list.append(img_raw_size)
        img_offset_list.append(ptr)
        b_img_data += img
        ptr += img_size

    # Convert list to binary file
    for i in range(len(img_raw_size_list)):
        b_img_offsets += img_raw_size_list[i].to_bytes(4, byteorder="little")
        b_img_offsets += img_offset_list[i].to_bytes(4, byteorder="little")

    # PMBBIN Binary Creation
    b_img = b_img_header + b_img_offsets + b_img_data
    pmbbin_name = p_input_dir.name + '.bin'
    p_output_pmbbin =helper.makeOutputDir(p_input_dir, p_output_dir) / pmbbin_name
    with p_output_pmbbin.open('wb') as outfile:
        outfile.write(b_img)
    print('Success')


def repackPIMGRecursive(p_input_dir, p_output_dir):
    # Create path list of directory containing gz,img files
    input_path_list = []
    p_dir_list = [p for p in p_input_dir.glob('**/*') if p.is_dir()]
    for p_dir in p_dir_list:
        if len([p for p in p_dir.glob('*') if re.search('(?<!\d)\d{4}(?!\d)\.(img|gz)', str(p))]) != 0:
            input_path_list.append(p_dir)

    p_output_dir = helper.makeOutputDir(p_input_dir, p_output_dir)

    for p in input_path_list:
        p_r = p.relative_to(p_input_dir)
        p_o = p_output_dir / p_r.parents[0]
        if p_o.exists() is False:
            p_o.mkdir(parents=True, exist_ok=True)
        repackPIMG(p, p_o)
