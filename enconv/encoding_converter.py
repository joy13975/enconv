import chardet
import os
from shutil import copyfile

class EncodingConverter:
    def __init__(self,
                 *args,
                 input_file=None,
                 input_encoding='guess',
                 guess_length=1024,
                 output_encoding='utf-8',
                 output_file=None,
                 overwrite=False,
                 **kwargs):
        self.input_file = input_file
        self.input_encoding = input_encoding
        self.guess_length = guess_length
        self.output_encoding = output_encoding
        self.output_file = output_file
        self.overwrite = overwrite
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def output_file(self):
        file_path = self._output_file
        # Create output file path if not specified
        if file_path == '':
            file_path = f'{self.input_file}.{self.output_encoding}'
        # Create output file path if output is specified as directory
        if os.path.isdir(file_path):
            input_file_name = os.path.basename(self.input_file)
            file_path = os.path.join(file_path, input_file_name)
        return file_path

    @output_file.setter
    def output_file(self, value):
        self._output_file = value

    def guess(self):
        sample = self._read(length=self.guess_length)
        return chardet.detect(sample)

    def convert(self, silent=False):
        try:
            # Confirm overwrite
            if os.path.exists(self.output_file) and not self.overwrite:
                overwrite_ok = input('Output file exists. Overwrite?\n(y/n): ')
                if overwrite_ok.lower() != 'y':
                    if not silent:
                        print('Abort writting.')
                    return False
            if not silent:
                self._print_file_size()
            if self.guess()['encoding'].lower() == 'utf-8':
                # No need to convert; just copy
                copyfile(self.input_file, self.output_file)
                return True
            print('Reading...')
            filebytes = self._read()
            print('Decoding...')
            decoded_str = filebytes.decode(
                self.input_encoding, errors='ignore')
            print('Encoding and writing...')
            with open(self.output_file, 'w', encoding=self.output_encoding) \
                    as file:
                file.write(decoded_str)
            return True
        except Exception as e:
            raise Exception(
                f'Failed to write to file {self.output_file}. ') from e

    def _print_file_size(self):
        filesize = os.stat(self.input_file).st_size
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        unit_idx = 0
        while filesize >= 1024:
            unit_idx += 1
            filesize /= 1024
        print(f'File size: {filesize:.1f} {units[unit_idx]}')

    def _read(self, length=-1):
        try:
            # Blocked reading is a lot faster than taking a potentially very
            # large file into RAM
            block_size = 8192
            byte_lines = []
            rough_len = 0
            with open(self.input_file, 'rb') as file:
                while True:
                    block = file.readlines(block_size)
                    if not block:
                        break
                    byte_lines.extend(block)
                    rough_len += block_size
                    if length > -1 and rough_len >= length:
                        break
                filebytes = b''.join(byte_lines)
                return filebytes[:length]
        except Exception as e:
            raise Exception(f'Failed to read file {self.input_file}. ') from e