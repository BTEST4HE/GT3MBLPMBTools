import mbl
import pmb
import helper
import struct
import pprint


def makeMblText(p_input, p_output_dir):
    mbl_bin = p_input.read_bytes()
    exist = -1
    for mbl_name in mbl.mbl_dict_list:
        mbl_flags = mbl.mbl_dict[mbl_name]
        try:
            if mbl.checkMbl(p_input, mbl_flags) is True:
                mbl_tree = mbl.importMbl(mbl_bin, mbl_flags)
                mbl_text = pprint.pformat(mbl_tree, width=180)
                p_output = helper.makeOutputDir(p_input, p_output_dir) / (p_input.name + '.txt')
                with p_output.open('w', encoding='utf-8') as outfile:
                    outfile.write(mbl_text)
                exist = 1
                break
        except (ValueError, struct.error, IndexError, helper.PointerError):
            pass
    if exist == 1:
        print('Success')
    else:
        print('Failure')


def makeMblTextRecursive(p_input, p_output_dir):
    p_output_dir = helper.makeOutputDir(p_input, p_output_dir)

    input_path_list = list(p_input.rglob('*.mbl'))
    for p in input_path_list:
        p_r = p.relative_to(p_input)
        dir_difference = len(p_r.parents) - 1
        p_o = p_output_dir
        for i in reversed(range(dir_difference)):
            p_o = p_o / p_r.parents[i]
        if p_o.is_dir() is False:
            p_o.mkdir(parents=True)
        print(p_r.name + '\t', end='')
        makeMblText(p, p_o)


def makePmbText(p_input, p_output_dir):
    pmb_bin = p_input.read_bytes()
    exist = -1
    for pmb_name in pmb.pmb_dict_list:
        pmb_flags = pmb.pmb_dict[pmb_name]
        try:
            if pmb.checkPmb(p_input, pmb_flags) is True:
                (pmb_tree, pimg) = pmb.importPmb(pmb_bin, pmb_flags)
                pmb_tree = pprint.pformat(pmb_tree, width=180)
                p_output_text = helper.makeOutputDir(p_input, p_output_dir) / (p_input.name + '.txt')
                with p_output_text.open('w', encoding='utf-8') as outfile:
                    outfile.write(pmb_tree)
                if pimg is not None:
                    p_output_pimg = helper.makeOutputDir(p_input, p_output_dir) / (p_input.name + '.bin')
                    with p_output_pimg.open('wb') as outfile:
                        outfile.write(pimg)
                exist = 1
                break
        except (ValueError, struct.error, IndexError, helper.PointerError):
            pass
    if exist == 1:
        print('Success')
    else:
        print('Failure')


def makePmbTextRecursive(p_input, p_output_dir):
    p_output_dir = helper.makeOutputDir(p_input, p_output_dir)

    input_path_list = list(p_input.rglob('*.pmb'))
    for p in input_path_list:
        p_r = p.relative_to(p_input)
        p_o = p_output_dir / p_r.parents[0]
        if p_o.exists() is False:
            p_o.mkdir(parents=True, exist_ok=True)
        print(p_r.name + '\t', end='')
        makePmbText(p, p_o)
