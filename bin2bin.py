import mbl
import pmb
import helper
import struct


def makeMbl(p_input, p_output_dir, out_mbl_flags):
    mbl_bin = p_input.read_bytes()
    exist = -1
    for mbl_name in mbl.mbl_dict_list:
        mbl_flags = mbl.mbl_dict[mbl_name]
        try:
            if mbl.checkMbl(p_input, mbl_flags) is True:
                mbl_tree = mbl.importMbl(mbl_bin, mbl_flags)
                mbl_tree = mbl.exportMblControlFlags(mbl_tree, out_mbl_flags)
                mbl_bin_out = mbl.exportMbl(mbl_tree, out_mbl_flags)
                if mbl_bin != mbl_bin_out:
                    p_output = helper.makeOutputDir(p_input, p_output_dir) / p_input.name
                    with p_output.open('wb') as outfile:
                        outfile.write(mbl_bin_out)
                    exist = 1
                else:
                    exist = 0
                break
        except (ValueError, struct.error, IndexError, helper.PointerError):
            pass
    if exist == 1:
        print('Success')
    elif exist == 0:
        print('No need to convert.')
    else:
        print('Failure')


def makeMblRecursive(p_input, p_output_dir, out_mbl_flags):
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
        makeMbl(p, p_o, out_mbl_flags)


def makePmb(p_input, p_output_dir, out_pmb_flags):
    pmb_bin = p_input.read_bytes()
    exist = -1
    for pmb_name in pmb.pmb_dict_list:
        pmb_flags = pmb.pmb_dict[pmb_name]
        try:
            if pmb.checkPmb(p_input, pmb_flags) is True:
                (pmb_tree, pimg) = pmb.importPmb(pmb_bin, pmb_flags)
                pmb_tree = pmb.exportPmbControlFlags(pmb_tree, out_pmb_flags)
                pmb_bin_out = pmb.exportPmb(pmb_tree, pimg, out_pmb_flags)

                if pmb_bin != pmb_bin_out:
                    p_output = helper.makeOutputDir(p_input, p_output_dir) / p_input.name
                    with p_output.open('wb') as outfile:
                        outfile.write(pmb_bin_out)
                    exist = 1
                else:
                    exist = 0
                break
        except (ValueError, struct.error, IndexError, helper.PointerError):
            pass
    if exist == 1:
        print('Success')
    elif exist == 0:
        print('No need to convert.')
    else:
        print('Failure')


def makePmbRecursive(p_input, p_output_dir, out_pmb_flags):
    p_output_dir = helper.makeOutputDir(p_input, p_output_dir)

    input_path_list = list(p_input.rglob('*.pmb'))
    for p in input_path_list:
        p_r = p.relative_to(p_input)
        p_o = p_output_dir / p_r.parents[0]
        if p_o.exists() is False:
            p_o.mkdir(parents=True, exist_ok=True)
        print(p_r.name + '\t', end='')
        makePmb(p, p_o, out_pmb_flags)
