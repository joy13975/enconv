import argparse

from .encoding_converter import EncodingConverter

def main(*args, **kwargs):
    ap = argparse.ArgumentParser(description='Guess and convert between encodings')
    ap.add_argument('input_file',
                    help='Input file path',
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
    ap.add_argument('-of', '--output_file',
                    help='Output file path',
                    default='')
    ap.add_argument('-ow', '--overwrite', 
                    help='When set, won\'t confirm when attempting to overwrite.',
                    action='store_true')
    args = ap.parse_args()
    ec = EncodingConverter(**vars(args))
    if ec.input_encoding.lower() == 'guess':
        guess_result = ec.guess()
        print(f'Guess: {guess_result}')
        ec.input_encoding = guess_result['encoding']
    if ec.convert():
        print(f'Wrote to {ec.output_file} in {ec.output_encoding}')
    else:
        print(f'Conversion failed.')


if __name__  == '__main__':
    main()