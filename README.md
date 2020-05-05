# Enconv
A light wrapper around chardet to conveniently convert text files.

# Install

Optionally create virtual env

```
~$ pip install enconv
```

# Usage

### enconv: Guess and convert between encodings
```bash
usage: enconv [-h] [-ie INPUT_ENCODING] [-gl GUESS_LENGTH]
                 [-oe OUTPUT_ENCODING] [-of OUTPUT_FILE] [-ow]
                 input_file
```

### enportal: Guess and convert file encodings from source to destination folders
```bash
usage: enportal [-h] [-ie INPUT_ENCODING] [-gl GUESS_LENGTH]
                [-oe OUTPUT_ENCODING] [-ow] [-i INTERVAL]
                input_dir output_dir
```

### encheck: Guess text encoding of files in folder
```bash
usage: encheck [-h] [-gl GUESS_LENGTH] input_dir
```

# Example

```bash
~$ enconv /Users/me/Downloads/chinese.txt
Guess: {'encoding': 'GB2312', 'confidence': 0.99, 'language': 'Chinese'}
Wrote to /Users/me/Downloads/chinese.txt.utf-8 in utf-8
```
