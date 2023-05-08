#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from numpy.typing import ArrayLike
from argparse import ArgumentParser
from gens import BinaryGen, GrayGen, MLSGen

def get_fft_mags(signal_vals:ArrayLike):
    fft_data = np.fft.rfft(signal_vals)
    signal_mags = np.abs(fft_data)
    signal_mags *= 2 / len(signal_vals)
    signal_mags[0] /= 2
    return signal_mags

def any_int_fmt(string:str):
    return int(string, 0)

parser = ArgumentParser(
        description=
        "the program shows the waveform and FFT of various binary sequences")
parser.add_argument(
        "-b", "--gen-bits", action="store_true", help=
        "use sequences of bits instead of words")
parser.add_argument(
        "-l", "--word-len", metavar="L", type=int, default=8, help=
        "word length (number of bits in each word)")
parser.add_argument(
        "-t", "--mls-taps", metavar="T", default=None, type=any_int_fmt, help=
        "taps for LFSR used to generate MLS sequence")
args = parser.parse_args()

if args.gen_bits:
    DTYPE = np.bool8
elif args.word_len <= 8:
    DTYPE = np.uint8
elif args.word_len <= 16:
    DTYPE = np.uint16
elif args.word_len <= 32:
    DTYPE = np.uint32
else:
    raise ValueError()

MAX_DATA_NUM = 2 ** args.word_len
if args.gen_bits:
    MAX_DATA_NUM *= args.word_len

seqs = (
    (BinaryGen(args.word_len, args.gen_bits), "r", "Binary"),
    (GrayGen(args.word_len, args.gen_bits), "g", "Gray"),
    (MLSGen(args.word_len, args.gen_bits, args.mls_taps), "b", "MLS"),
)

fig, ax = plt.subplots(len(seqs) + 1, 1, constrained_layout=True,
        gridspec_kw={"height_ratios": [1] * len(seqs) + [len(seqs)]})
one_pix = 72.0 / fig.dpi
seq_axs = ax[0:-1]
fft_ax = ax[-1]

prev_seq_ax = None
seq_axs[0].set_title("Sequence")
seq_axs[-1].set_xlabel("Bit" if args.gen_bits else "Word")
for seq_ax, (seq, color, label) in zip(seq_axs, seqs):
    # Draw signal values (words or bits)
    x = np.arange(len(seq))
    y = np.fromiter(seq, DTYPE, len(seq))
    seq_ax.step(x, y, f"-{color}", where="mid", label=label, linewidth=one_pix)
    # Group bits into words
    if args.gen_bits:
        for x_div in range(0, MAX_DATA_NUM + 1, args.word_len):
            seq_ax.axvline(x_div - 0.5, color="k", linewidth=one_pix)
    # Axis config
    seq_ax.set_ylabel("Value")
    seq_ax.set_xlim(0, MAX_DATA_NUM - 1)
    seq_ax.legend(loc="upper right")
    if prev_seq_ax:
        prev_seq_ax.sharex(seq_ax)
        prev_seq_ax.label_outer()
    prev_seq_ax = seq_ax
    # Draw signal harmonics
    mags = get_fft_mags(y - y.mean()) # Remove offset
    fft_ax.plot(mags, color, label=label, linewidth=one_pix)

fft_ax.set_title("FFT")
fft_ax.set_ylabel("Amplitude (offset removed)")
fft_ax.set_xlabel("Harmonic")
fft_ax.legend(loc="upper right")
fft_ax.grid(which="major", color="#DDDDDD")
fft_ax.grid(which="minor", color="#EEEEEE")
fft_ax.minorticks_on()

plt.show()
