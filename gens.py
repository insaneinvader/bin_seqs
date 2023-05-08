MLS_TAPS = [
    0, # Dummy
    0b1, # 1
    0b11, # 2
    0b011, # 3
    0b0011, # 4
    0b00101, # 5
    0b000011, # 6
    0b0000011, # 7
    0b01100011, # 8
    0b000010001, # 9
    0b0000001001, # 10
    0b00000000101, # 11
    0b000010011001, # 12
    0b0000000011011, # 13
    0b01100000000011, # 14
    0b000000000000011, # 15
    0b0000000000101101, # 16
    0b00000000000001001, # 17
    0b000000000010000001, # 18
    0b0000000000001100011, # 19
    0b00000000000000001001, # 20
    0b000000000000000000101, # 21
    0b0000000000000000000011, # 22
    0b00000000000000000100001, # 23
    0b000000000000000000011011, # 24
]
"""
Source: W. Stahnke, Primitive binary polynomials,
Mathematics of Computation, 27:977-980, 1973.
"""

class BaseGen(object):
    """
    Parent class for all generators.
    """

    def __init__(self, word_len:int, word_num:int, gen_bits:bool=False):
        if word_len <= 0:
            raise ValueError()
        self.word_len = word_len
        self.word_num = word_num
        if gen_bits:
            self.gen = self.bits_gen
            self.len = word_num * word_len
        else:
            self.gen = self.words_gen
            self.len = word_num

    def __len__(self):
        return self.len

    def __iter__(self):
        return self.gen()

    def bits_gen(self):
        for word in self.words_gen():
            for shift in range(self.word_len):
                lsb = (word >> shift) & 1
                yield lsb

    def words_gen(self):
        raise NotImplementedError()

class BinaryGen(BaseGen):
    """
    Binary code generator.
    """

    def __init__(self, word_len:int, gen_bits:bool=False):
        super().__init__(word_len, 2 ** word_len, gen_bits)

    def words_gen(self):
        for bin_word in range(self.word_num):
            yield bin_word

class GrayGen(BaseGen):
    """
    Gray code generator. Algorithm source:
    https://en.wikipedia.org/wiki/Gray_code#Converting_to_and_from_Gray_code
    """

    def __init__(self, word_len:int, gen_bits:bool=False):
        super().__init__(word_len, 2 ** word_len, gen_bits)

    def words_gen(self):
        for bin_word in range(self.word_num):
            gray_word = bin_word ^ (bin_word >> 1)
            yield gray_word

class MLSGen(BaseGen):
    """
    Maximum length sequence generator. Algorithm explanation:
    http://www.kempacoustics.com/thesis/node83.html
    """

    def __init__(self, word_len:int, gen_bits:bool=False, taps:int=None):
        if taps is None:
            if word_len >= len(MLS_TAPS):
                raise ValueError()
            self.taps = MLS_TAPS[word_len]
        else:
            self.taps = taps
        super().__init__(word_len, 2 ** word_len - 1, gen_bits) # Exclude word=0

    def words_gen(self):
        mls_word = self.word_num # Set all bits
        yield mls_word
        msb_mask = (self.word_num >> 1) + 1
        for _ in range(self.word_num - 1):
            for _ in range(self.word_len):
                new_msb = (mls_word & self.taps).bit_count() & 1
                mls_word = (mls_word >> 1) | (new_msb * msb_mask)
            yield mls_word
