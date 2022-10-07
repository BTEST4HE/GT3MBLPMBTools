import argparse
import pathlib
import pmbbin


parser = argparse.ArgumentParser(prog='pmbbintools', description='This is a script to unpack and repack PMBBIN files '
                                                                 '(xxx.pmb.bin) output by the -e (--textexport) option '
                                                                 'of pmbtools. When unpacked, the output is in '
                                                                 'img,gz format.If -u(--unpack) or -e(repack) option '
                                                                 'is not specified, it means that -u option '
                                                                 'is specified.')
parser.add_argument('input', type=pathlib.Path, help='input file path or directory')
parser.add_argument('output_dir', type=pathlib.Path, nargs='?', default=None, help='output directory(optional)')
parser.add_argument('-u', '--unpack', help='unpack PMBBIN into img,gz files',
                    action="store_true")
parser.add_argument('-e', '--repack', help='repack the PMBBIN file in the directory where the img,gz file is stored',
                    action="store_true")
parser.add_argument('-r', '--recursive', help='reads "input" as a directory and recursively retrieves files '
                                              'in the directory', action="store_true")
parser.add_argument('-g', '--ungzip', help='extract gzip file in PMBBIN to img file and output (unpack only)',
                    action="store_true")
args = parser.parse_args()

# Print Arguments
print('input:{}'.format(repr(args.input)))
if args.output_dir:
    print('output:{}'.format(repr(args.output_dir)))


if args.repack:
    if args.recursive:
        if args.input.is_dir():
            pmbbin.repackPIMGRecursive(args.input, args.output_dir)
        else:
            print('Error: When using the "-r" option, "input" must be a directory.')
    elif args.input.is_dir():
        pmbbin.repackPIMG(args.input, args.output_dir)
    else:
        print('Error: In this case, "input" must be a directory.')

else:
    is_ungzip = True if args.ungzip else False
    if args.recursive:
        if args.input.is_dir():
            pmbbin.unpackPIMGRecursive(args.input, args.output_dir, is_ungzip)
        else:
            print('Error: When using the "-r" option, "input" must be a directory.')
    elif args.input.is_file():
        pmbbin.unpackPIMG(args.input, args.output_dir, is_ungzip)
    else:
        print('Error: In this case, "input" must be a file.')
