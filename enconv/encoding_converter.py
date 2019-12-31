import chardet
import os

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

    def convert(self):
        try:
            # Confirm overwrite
            if os.path.exists(self.output_file) and not self.overwrite:
                overwrite_ok = input('Output file exists. Overwrite?\n(y/n): ')
                if overwrite_ok.lower() != 'y':
                    print('Abort writting.')
                    return False
            filebytes = self._read()
            decoded_str = filebytes.decode(self.input_encoding, errors='ignore')
            with open(self.output_file, 'w', encoding=self.output_encoding) as file:
                file.write(decoded_str)
            return True
        except Exception as e:
            raise Exception(f'Failed to write to file {self.output_file}. ') from e


    def _read(self, length=-1):
        try:
            with open(self.input_file, 'rb') as file:
                filebytes = b''
                for line in file.readlines():
                    filebytes += line
                    if length > -1 and len(filebytes) >= length:
                        break
                return filebytes[:length]
        except Exception as e:
            raise Exception(f'Failed to read file {self.input_file}. ') from e