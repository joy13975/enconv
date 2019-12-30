# Enconv
A light wrapper around chardet to conveniently convert text files.

# Install

Optionally create virtual env

```
~$ pip install enconv
```

# Usage

```bash
~$ enconv
usage: enconv.py [-h] [-ie INPUT_ENCODING] [-gl GUESS_LENGTH]
                 [-oe OUTPUT_ENCODING] [-of OUTPUT_FILE] [-ow]
                 input_file
```

# Example

```bash
~$ enconv /Users/me/Downloads/chinese.txt
Guess: {'encoding': 'GB2312', 'confidence': 0.99, 'language': 'Chinese'}
Wrote to /Users/me/Downloads/chinese.txt.utf-8 in utf-8
```