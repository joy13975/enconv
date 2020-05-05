import argparse
import os
from time import sleep
import traceback

from .encoding_converter import EncodingConverter

exclude_files = ['.DS_Store']
include_extensions = ['txt']


def main(*args, **kwargs):
    ap = argparse.ArgumentParser(description='Guess and convert '
                                 'file encodings from source to '
                                 'destination folders')
    ap.add_argument('input_dir',
                    help='Input directory',
                    type=str)
    ap.add_argument('output_dir',
                    help='Output directory',
                    type=str)
    ap.add_argument('-ie', '--input_encoding',
                    help='Input enconding',
                    default='guess')
    ap.add_argument('-gl', '--guess_length',
                    help='Number of bytes to use for guessing. -1=all',
                    default=1024)
    ap.add_argument('-oe', '--output_encoding',
                    help='Output enconding',
                    default='utf-8')
    ap.add_argument('-ow', '--overwrite',
                    help='When set, won\'t confirm when attempting to '
                    'overwrite.',
                    action='store_true')
    ap.add_argument('-i', '--interval',
                    help='Loop interval in seconds.',
                    default=2)
    args = ap.parse_args()
    if not os.path.isdir(args.input_dir):
        print('Input directory is not a directory')
        exit(1)
    if not os.path.isdir(args.output_dir):
        print('Output directory is not a directory')
        exit(1)
    args_dict = vars(args)
    print(
        f'****************************************\n'
        f'*       Encoding Portal starting       *\n'
        f'****************************************\n'
        f'src: "{args.input_dir}" ({args.input_encoding})\n'
        f'                   |                    \n'
        f'                   V                    \n'
        f'dst: "{args.output_dir}" ({args.output_encoding})'
    )
    failure_mark = 'encodefailed.'
    try:
        print(f'Checking every {args.interval:.1f} seconds...')
        while True:
            sleep(args.interval)
            filenames = [f for f in os.listdir(args.input_dir)
                         if os.path.isfile(os.path.join(args.input_dir, f))]
            for filename in filenames:
                if filename.startswith(failure_mark) or filename in \
                        exclude_files:
                    continue
                if filename.split('.')[-1] not in include_extensions:
                    continue
                print(f'\nNew file: {filename}')
                ec_args = args_dict.copy()
                input_path = os.path.join(args.input_dir, filename)
                ec_args['input_file'] = input_path
                output_path = os.path.join(args.output_dir, filename)
                ec_args['output_file'] = output_path
                ec = EncodingConverter(**ec_args)
                if ec.input_encoding.lower() == 'guess':
                    guess_result = ec.guess()
                    print(f'Guess: {guess_result}')
                    ec.input_encoding = guess_result['encoding']
                try:
                    if ec.convert():
                        print(f'Wrote to {ec.output_file} in '
                              f'{ec.output_encoding}')
                        os.remove(input_path)
                    else:
                        raise Exception(f'Conversion failed.')
                except Exception as e:
                    print(e)
                    traceback.print_exc()
                    os.rename(input_path, os.path.join(
                        args.input_dir, f'{failure_mark}{filename}'))
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
