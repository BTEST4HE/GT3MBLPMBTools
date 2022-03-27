import argparse
import pathlib
import mbl
import bin2bin as b2b
import bin2text as b2t
import text2bin as t2b


parser = argparse.ArgumentParser(prog='mbltools', description='Scripts to convert MBL files for playback '
                                                              'in the production version of GT3, export and import '
                                                              'in text format, etc. '
                                                              'When converting from MBL to MBL, if the file before '
                                                              'conversion and the file after conversion are the same, '
                                                              'there is a specification that the converted file '
                                                              'is not output.')
parser.add_argument('input', type=pathlib.Path, help='input file path or directory')
parser.add_argument('output_dir', type=pathlib.Path, nargs='?', default=None, help='output directory(optional)')
parser.add_argument('-s', '--storedemo', help='output MBL files that can be played back in '
                                              'GT3 Store Demo Vol.2', action="store_true")
parser.add_argument('-p', '--product', help='output MBL files that can be played back in '
                                            'the production version of GT3', action="store_true")
parser.add_argument('-r', '--recursive', help='reads "input" as a directory and recursively retrieves files '
                                              'in the directory', action="store_true")
parser.add_argument('-e', '--textexport', help='export MBL files to text format',
                    action="store_true")
parser.add_argument('-i', '--textimport', help='import from text format MBL to binary format MBL',
                    action="store_true")
args = parser.parse_args()

print('input:{}'.format(repr(args.input)))
if args.output_dir:
    print('output:{}'.format(repr(args.output_dir)))

if args.textexport:
    if args.recursive:
        if args.input.is_dir():
            b2t.makeMblTextRecursive(args.input, args.output_dir)
        else:
            print('Error: When using the "-r" option, "input" must be a directory.')
    elif args.input.is_file():
        b2t.makeMblText(args.input, args.output_dir)
    else:
        print('Error: In this case, "input" must be a file.')

elif args.textimport:
    if args.storedemo:
        mbl_flags = mbl.mbl_dict['mbl21']
    elif args.product:
        mbl_flags = mbl.mbl_dict['mbl40']
    else:
        mbl_flags = None
    if args.recursive:
        if args.input.is_dir():
            t2b.makeMblFromTextBinRecursive(args.input, args.output_dir, mbl_flags)
        else:
            print('Error: When using the "-r" option, "input" must be a directory.')
    elif args.input.is_file():
        t2b.makeMblFromTextBin(args.input, args.output_dir, mbl_flags)
    else:
        print('Error: In this case, "input" must be a file.')

else:
    if args.storedemo:
        mbl_flags = mbl.mbl_dict['mbl21']
    else:
        mbl_flags = mbl.mbl_dict['mbl40']

    if args.recursive:
        if args.input.is_dir():
            b2b.makeMblRecursive(args.input, args.output_dir, mbl_flags)
        else:
            print('Error: When using the "-r" option, "input" must be a directory.')
    elif args.input.is_file():
        b2b.makeMbl(args.input, args.output_dir, mbl_flags)
    else:
        print('Error: In this case, "input" must be a file.')
