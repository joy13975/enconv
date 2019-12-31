import argparse
import os
from time import sleep

from .encoding_converter import EncodingConverter

exclude_files = ['.DS_Store']
include_extensions = ['txt']

def main(*args, **kwargs):
    ap = argparse.ArgumentParser(description='Guess text encoding of files in folder')
    ap.add_argument('input_dir',
                    help='Input directory',
                    type=str)
    ap.add_argument('-gl', '--guess_length',
                    help='Number of bytes to use for guessing. -1=all',
                    default=1024)
    args = ap.parse_args()
    if not os.path.isdir(args.input_dir):
        print('Input directory is not a directory')
        exit(1)
    args_dict = vars(args)
    filenames = [f for f in os.listdir(args.input_dir)
                if os.path.isfile(os.path.join(args.input_dir, f))]
    for filename in filenames:
        if filename in exclude_files or filename.split('.')[-1] not in include_extensions:
            continue
        ec_args = args_dict.copy()
        input_path = os.path.join(args.input_dir, filename)
        ec_args['input_file'] = input_path
        ec = EncodingConverter(**ec_args)
        if ec.input_encoding.lower() == 'guess':
            guess_result = ec.guess()
            print(f'Guess for {filename}:\n{guess_result}')
            ec.input_encoding = guess_result['encoding']

if __name__  == '__main__':
    main()