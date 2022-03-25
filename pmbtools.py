import pmb
import argparse
import bin2bin as b2b
import bin2text as b2t
import text2bin as t2b
import pathlib
import time

t1 = time.time()

parser = argparse.ArgumentParser(prog='pmbtools', description='Scripts to convert PMB files for playback '
                                                              'in the production version of GT3, export and import '
                                                              'in text and PMB.BIN (image data) formats, etc.')
parser.add_argument('input', type=pathlib.Path, help='input file path or directory')
parser.add_argument('output_dir', type=pathlib.Path, nargs='?', default=None, help='output directory(optional)')
parser.add_argument('-s', '--storedemo', help='output PMB files that can be played back in '
                                              'GT3 Store Demo Vol.2', action="store_true")
parser.add_argument('-p', '--product', help='output PMB files that can be played back in '
                                            'the production version of GT3', action="store_true")
parser.add_argument('-r', '--recursive', help='reads "input" as a directory and recursively retrieves files '
                                              'in the directory', action="store_true")
parser.add_argument('-e', '--textexport', help='export from PMB file to text format and PMBBIN(image data) files'
                    , action="store_true")
parser.add_argument('-i', '--textimport', help='import from text format PMB and PMBBIN(image data) files'
                                               ' to binary format PNB'
                    , action="store_true")
args = parser.parse_args()

print(repr(args.input))
if args.output_dir:
    print(repr(args.output_dir))

if args.textexport:
    if args.recursive:
        if args.input.is_dir():
            b2t.makePmbTextRecursive(args.input, args.output_dir)
        else:
            print('Error: When using the "-r" option, "input" must be a directory.')
    elif args.input.is_file():
        b2t.makePmbText(args.input, args.output_dir)
    else:
        print('Error: In this case, "input" must be a file.')

elif args.textimport:
    if args.storedemo:
        pmb_flags = pmb.pmb_dict['pmb20']
    elif args.product:
        pmb_flags = pmb.pmb_dict['pmb40']
    else:
        pmb_flags = None
    if args.recursive:
        if args.input.is_dir():
            t2b.makePmbFromTextBinRecursive(args.input, args.output_dir, pmb_flags)
        else:
            print('Error: When using the "-r" option, "input" must be a directory.')
    elif args.input.is_file():
        t2b.makePmbFromTextBin(args.input, args.output_dir, pmb_flags)
    else:
        print('Error: In this case, "input" must be a file.')

else:
    print()
    if args.storedemo:
        pmb_flags = pmb.pmb_dict['pmb20']
    else:
        pmb_flags = pmb.pmb_dict['pmb40']

    if args.recursive:
        if args.input.is_dir():
            b2b.makePmbRecursive(args.input, args.output_dir, pmb_flags)
        else:
            print('Error: When using the "-r" option, "input" must be a directory.')
    elif args.input.is_file():
        b2b.makePmb(args.input, args.output_dir, pmb_flags)
    else:
        print('Error: In this case, "input" must be a file.')

t2 = time.time()
elapsed_time = t2-t1
print(f"経過時間：{elapsed_time}")
