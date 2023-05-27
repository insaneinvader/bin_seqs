# Binary sequences

## Goals

The purpose of this project is to:
1. Show the waveform and FFT of [binary](https://en.wikipedia.org/wiki/Binary_number), [Gray](https://en.wikipedia.org/wiki/Gray_code) and [MLS](https://en.wikipedia.org/wiki/Maximum_length_sequence) sequences.
2. Help to understand why an [absolute encoder](https://en.wikipedia.org/wiki/Rotary_encoder) uses an [MLS track](https://williamsprecher.com/pseudo-random-code-disc).
3. Demonstrate that an MLS is a type of [pseudorandom sequence](https://en.wikipedia.org/wiki/Pseudorandom_binary_sequence).

## Examples

### Prerequisites

* Use your local Python installation:  
  `python3 -m pip -r requirements.txt`  
  Note: the results will be shown in the *GUI window*.
* Or use Docker to keep your host clean:  
  `docker build -t binseqs .`  
  Note: the results will appear in the *seqs.pdf file*.

### Asking for help

* `python3 app.py -h`
* `docker run --rm -v .:/app binseqs -h`

### Specifying word length

* `python3 app.py --word-len 8`
* `docker run --rm -v .:/app binseqs --word-len 8`

![Result](pics/example_8bit_wrdseq.png)

### Using sequences of bits instead of words

* `python3 app.py --word-len 5 --gen-bits`
* `docker run --rm -v .:/app binseqs --word-len 5 --gen-bits`

![Result](pics/example_5bit_bitseq.png)
