import mbl
import pmb
import helper


def makeMblFromTextBin(p_input, p_output_dir, out_mbl_flags):
    print(p_input.name + '\t', end='')
    with p_input.open('r', encoding='utf-8') as infile:
        mbl_text = infile.read()
    mbl_tree = eval(mbl_text)
    out_mbl_flags = mbl.mbl_dict[mbl_tree[1]] if out_mbl_flags is None else out_mbl_flags

    mbl_tree = mbl.exportMblControlFlags(mbl_tree, out_mbl_flags)
    mbl_bin_out = mbl.exportMbl(mbl_tree, out_mbl_flags)

    mbl_filename = p_input.stem[:-4] if p_input.stem[-4:] == '.mbl' else p_input.stem
    p_output = helper.makeOutputDir(p_input, p_output_dir) / (mbl_filename + '.mbl')
    with p_output.open('wb') as outfile:
        outfile.write(mbl_bin_out)
    print('Success')


def makeMblFromTextBinRecursive(p_input, p_output_dir, out_mbl_flags):
    p_output_dir = helper.makeOutputDir(p_input, p_output_dir)

    input_path_list = list(p_input.rglob('*.txt'))
    for p in input_path_list:
        p_r = p.relative_to(p_input)
        p_o = p_output_dir / p_r.parents[0]
        if p_o.exists() is False:
            p_o.mkdir(parents=True, exist_ok=True)
        makeMblFromTextBin(p, p_o, out_mbl_flags)


def makePmbFromTextBin(p_input, p_output_dir, out_pmb_flags):
    print(p_input.name + '\t', end='')
    p_input_parent = p_input.parent
    with p_input.open('r', encoding='utf-8') as infile:
        pmb_text = infile.read()
    pmb_tree = eval(pmb_text)
    out_pmb_flags = pmb.pmb_dict[pmb_tree[1]] if out_pmb_flags is None else out_pmb_flags

    p_input_pimg = p_input_parent / (p_input.stem + '.bin')
    if p_input_pimg.exists():
        with p_input_pimg.open('rb') as infile:
            pimg = infile.read()
    else:
        pimg = None

    pmb_tree = pmb.exportPmbControlFlags(pmb_tree, out_pmb_flags)
    pmb_bin_out = pmb.exportPmb(pmb_tree, pimg, out_pmb_flags)

    pmb_filename = p_input.stem[:-4] if p_input.stem[-4:] == '.pmb' else p_input.stem
    p_output = helper.makeOutputDir(p_input, p_output_dir) / (pmb_filename + '.pmb')
    with p_output.open('wb') as outfile:
        outfile.write(pmb_bin_out)
    print('Success')


def makePmbFromTextBinRecursive(p_input, p_output_dir, out_pmb_flags):
    p_output_dir = helper.makeOutputDir(p_input, p_output_dir)

    input_path_list = list(p_input.rglob('*.txt'))
    for p in input_path_list:
        p_r = p.relative_to(p_input)
        p_o = p_output_dir / p_r.parents[0]
        if p_o.exists() is False:
            p_o.mkdir(parents=True, exist_ok=True)
        makePmbFromTextBin(p, p_o, out_pmb_flags)
