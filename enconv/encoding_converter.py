import chardet
import os

class EncodingConverter:
    def __init__(self, *args, **kwargs):
        """Constructor

        :attribute str input_file: mandatory input file path
        :attribute str input_encoding: optional input encoding
        :attribute int guess_length: number of bytes to use for guessing
        :attribute str output_encoding: optional output encoding
        :attribute str output_file: optional output file path
        :attribute bool overwrite: won't confirm overwrite when True
        """
        for k, v in kwargs.items():
            setattr(self, k, v)
        assert getattr(self, 'input_file') is not None
        self.filebytes = self._read()
        assert getattr(self, 'input_encoding') is not None
        assert getattr(self, 'guess_length') is not None
        assert getattr(self, 'output_encoding') is not None
        assert getattr(self, 'output_file') is not None
        assert getattr(self, 'overwrite') is not None
        self.converted_str = None

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
        return chardet.detect(self.filebytes[:self.guess_length])

    def convert(self):
        try:
            # Confirm overwrite
            if os.path.exists(self.output_file) and not self.overwrite:
                overwrite_ok = input('Output file exists. Overwrite?\n(y/n): ')
                if overwrite_ok.lower() != 'y':
                    print('Abort writting.')
                    return False
            decoded_str = self.filebytes.decode(self.input_encoding, errors='ignore')
            with open(self.output_file, 'w', encoding=self.output_encoding) as file:
                file.write(decoded_str)
            return True
        except Exception as e:
            raise Exception(f'Failed to write to file {self.output_file}. ') from e


    def _read(self):
        try:
            with open(self.input_file, 'rb') as file:
                filebytes = b''
                for line in file.readlines():
                    filebytes += line
                return filebytes
        except Exception as e:
            raise Exception(f'Failed to read file {self.input_file}. ') from e