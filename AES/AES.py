import random
import numpy as np


class AES:
    # AES S-box
    # s_box is simply an affine transformation(i.e. matrix mulitplication followed by a vector addition)
    # of the inverse of the input byte. Possible to do that instead of using a lookup table.
    s_box = [
        # 0    1    2    3    4    5    6    7    8    9    A    B    C    D    E    F
        0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76, # 0
        0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0, # 1
        0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15, # 2
        0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75, # 3
        0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84, # 4
        0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf, # 5
        0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8, # 6
        0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2, # 7
        0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73, # 8
        0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb, # 9
        0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79, # A
        0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08, # B
        0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a, # C
        0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e, # D
        0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf, # E
        0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16  # F
    ]

    # AES inverse S-box to be moved for inverse
    inv_s_box = [
        # 0    1    2    3    4    5    6    7    8    9    A    B    C    D    E    F
        0x52,0x09,0x6a,0xd5,0x30,0x36,0xa5,0x38,0xbf,0x40,0xa3,0x9e,0x81,0xf3,0xd7,0xfb, # 0
        0x7c,0xe3,0x39,0x82,0x9b,0x2f,0xff,0x87,0x34,0x8e,0x43,0x44,0xc4,0xde,0xe9,0xcb, # 1
        0x54,0x7b,0x94,0x32,0xa6,0xc2,0x23,0x3d,0xee,0x4c,0x95,0x0b,0x42,0xfa,0xc3,0x4e, # 2
        0x08,0x2e,0xa1,0x66,0x28,0xd9,0x24,0xb2,0x76,0x5b,0xa2,0x49,0x6d,0x8b,0xd1,0x25, # 3
        0x72,0xf8,0xf6,0x64,0x86,0x68,0x98,0x16,0xd4,0xa4,0x5c,0xcc,0x5d,0x65,0xb6,0x92, # 4
        0x6c,0x70,0x48,0x50,0xfd,0xed,0xb9,0xda,0x5e,0x15,0x46,0x57,0xa7,0x8d,0x9d,0x84, # 5
        0x90,0xd8,0xab,0x00,0x8c,0xbc,0xd3,0x0a,0xf7,0xe4,0x58,0x05,0xb8,0xb3,0x45,0x06, # 6
        0xd0,0x2c,0x1e,0x8f,0xca,0x3f,0x0f,0x02,0xc1,0xaf,0xbd,0x03,0x01,0x13,0x8a,0x6b, # 7
        0x3a,0x91,0x11,0x41,0x4f,0x67,0xdc,0xea,0x97,0xf2,0xcf,0xce,0xf0,0xb4,0xe6,0x73, # 8
        0x96,0xac,0x74,0x22,0xe7,0xad,0x35,0x85,0xe2,0xf9,0x37,0xe8,0x1c,0x75,0xdf,0x6e, # 9
        0x47,0xf1,0x1a,0x71,0x1d,0x29,0xc5,0x89,0x6f,0xb7,0x62,0x0e,0xaa,0x18,0xbe,0x1b, # A
        0xfc,0x56,0x3e,0x4b,0xc6,0xd2,0x79,0x20,0x9a,0xdb,0xc0,0xfe,0x78,0xcd,0x5a,0xf4, # B
        0x1f,0xdd,0xa8,0x33,0x88,0x07,0xc7,0x31,0xb1,0x12,0x10,0x59,0x27,0x80,0xec,0x5f, # C
        0x60,0x51,0x7f,0xa9,0x19,0xb5,0x4a,0x0d,0x2d,0xe5,0x7a,0x9f,0x93,0xc9,0x9c,0xef, # D
        0xa0,0xe0,0x3b,0x4d,0xae,0x2a,0xf5,0xb0,0xc8,0xeb,0xbb,0x3c,0x83,0x53,0x99,0x61, # E
        0x17,0x2b,0x04,0x7e,0xba,0x77,0xd6,0x26,0xe1,0x69,0x14,0x63,0x55,0x21,0x0c,0x7d  # F
    ]
    def __init__(self, plaintext, key) -> None:
        # number of rounds
        self.Nr = 10
        # number of columns in state(or words in key)
        self.Nk = 4
        # create state
        self.create_state(plaintext)

        # create keys for each round, requires the s_box
        self.create_keys(key)

    def print(self) -> None:
        for i in range(4):
            for j in range(4):
                print(hex(self.state[j][i]), end=' ')
            print()

        print()

    def print_keys(self) -> None:
        for i in range(11):
            print(f"Round {i} key")
            for j in range(4):
                for k in range(4):
                    print(hex(self.key[i][k][j]), end=' ')
                print()
            print()

    def create_state(self, plaintext) -> None:
        if plaintext:
            # create numpy matrix
            self.state = np.array([[plaintext[i + j] for j in range(4)] for i in range(0, 16, 4)])
        else:
            self.state = np.array([[0 for _ in range(4)] for _ in range(4)])


    # The next 3 functions are used for key creation.
    def sub_word(self, word) -> None:
        for i in range(len(word)):
            word[i] = AES.s_box[word[i]]
        return word

    def rot_word(self, word) -> None:
        word = np.roll(word, -1)
        return word

    def create_keys(self, key) -> None:
        # Create a numpy matrix from the 16-byte key, not tranposed
        # self.key = [np.array([[key[4*i + j] for j in range(4)] for i in range(4)], dtype=np.uint8)]
        self.key = np.zeros((self.Nr + 1, 4, 4), dtype=int)

        # rcon array
        rcon = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]

        # intialize with given key
        for i in range(4):
            for j in range(4):
                self.key[0][i][j] = key[4*i + j]

        # generate round keys
        for i in range(1, self.Nr + 1):
            for j in range(4):
                if j == 0:
                    prev = self.key[i - 1][3].copy()
                    prev = self.rot_word(prev)
                    prev = self.sub_word(prev)
                    prev[0] ^= rcon[i - 1]
                else:
                    prev = self.key[i][j - 1]
                for k in range(4):
                    self.key[i][j][k] = self.key[i - 1][j][k] ^ prev[k]

        # transpose keys, using this for now since I am not sure how to fix this
        # in the original code you wrote.
        # for i in range(self.Nr + 1):
        #     self.key[i] = self.key[i]


    def sub_bytes(self, state) -> None:
        for i in range(4):
            for j in range(4):
                state[i][j] = AES.s_box[state[i][j]]

    def inv_sub_bytes(self, state) -> None:
        for i in range(4):
            for j in range(4):
                state[i][j] = AES.inv_s_box[state[i][j]]

    def shift_rows(self, state) -> None:
        # this shifts the rows by i
        for i in range(4):
            state[:,i] = np.roll(state[:,i], -i)

    def inv_shift_rows(self, state) -> None:
        for i in range(4):
            state[i] = state[i][-i:] + state[i][:-i]

    # multiplying by 2 in GF(2^8)
    # used in mix_columns
    def xtimes(self, x):
        # if MSB is 1, then it will overflow
        if x & 0x80:
            return ((x << 1) ^ 0x11B)
            # (x << 1) ^ 0x1B) & 0xFF also does the same thing
        return x << 1


    def mix_columns(self, state) -> None:
        for i in range(4):
            a = state[i][0]
            b = state[i][1]
            c = state[i][2]
            d = state[i][3]

            state[i][0] = aes.xtimes(a) ^ b ^ aes.xtimes(b) ^ c ^ d
            state[i][1] = a ^ aes.xtimes(b) ^ aes.xtimes(c) ^ c ^ d
            state[i][2] = a ^ b ^ aes.xtimes(c) ^ aes.xtimes(d) ^ d
            state[i][3] = aes.xtimes(a) ^ a ^ b ^ c ^ aes.xtimes(d)
            # [1 3 2 1]
            # [1 2 3 1]
            # [1 1 2 3]
            # [3 1 1 2]

    # Multiply by 0x09 in GF(2^8)
    def mul9(x):
        return aes.xtimes(aes.xtimes(aes.xtimes(x))) ^ x

    # Multiply by 0x0B in GF(2^8)
    def mul11(x):
        return aes.xtimes(aes.xtimes(aes.xtimes(x))) ^ aes.xtimes(x) ^ x

    # Multiply by 0x0D in GF(2^8)
    def mul13(x):
        return aes.xtimes(aes.xtimes(aes.xtimes(x))) ^ aes.xtimes(aes.xtimes(x)) ^ x

    # Multiply by 0x0E in GF(2^8)
    def mul14(x):
        return aes.xtimes(aes.xtimes(aes.xtimes(x))) ^ aes.xtimes(aes.xtimes(x)) ^ aes.xtimes(x)

    # Perform Inverse MixColumn on a single column
    def inv_mix_column(column):
        a = column[0]
        b = column[1]
        c = column[2]
        d = column[3]

        return [
            aes.mul14(a) ^ aes.mul11(b) ^ aes.mul13(c) ^ aes.mul9(d),
            aes.mul9(a) ^ aes.mul14(b) ^ aes.mul11(c) ^ aes.mul13(d),
            aes.mul13(a) ^ aes.mul9(b) ^ aes.mul14(c) ^ aes.mul11(d),
            aes.mul11(a) ^ aes.mul13(b) ^ aes.mul9(c) ^ aes.mul14(d)
        ]

    # Apply Inverse MixColumn to the whole state
    def inv_mix_columns(state):
        for i in range(4):
            # Extract column i
            column = [state[j][i] for j in range(4)]
            # Apply Inverse MixColumn to this column
            column = aes.inv_mix_column(column)
            # Put the result back into the state
            for j in range(4):
                state[j][i] = column[j]

    def add_round_key(self, state, round) -> None:
        # xor hex values
        for i in range(4):
            for j in range(4):
                state[i][j] ^= self.key[round][i][j]

    def state_to_text(self, state) -> str:
        # concatenate state
        text = ""
        for i in range(4):
            for j in range(4):
                # add hex value to text without the 0x
                text += hex(state[i][j])[2:]

        return text

    def main(self) -> None:
        # print("Starting state:")
        # self.print()

        # xor with key for round 0
        # print("Add round 0 key:")
        self.add_round_key(self.state, 0)
        # self.print()

        for i in range(1, 10):
            # print("---------")

            # print("Sub bytes:")
            self.sub_bytes(self.state)
            # self.print()

            # print("Shift rows:")
            self.shift_rows(self.state)
            # self.print()

            # print("Mix columns:")
            self.mix_columns(self.state)
            # self.print()

            # print(f"Round {i}")
            self.add_round_key(self.state, i)
            # self.print()

        # print("Sub bytes:")
        self.sub_bytes(self.state)
        # self.print()

        # print("Shift rows:")
        self.shift_rows(self.state)
        # self.print()

        # print("Add round key:")
        self.add_round_key(self.state, 10)
        # self.print()

        print("Cipher text:")
        print(self.state_to_text(self.state))



# Run main
if __name__ == "__main__":
    # prompt user for plaintext
    plaintext = input("Enter plaintext: ")
    key = input("Enter key: ")

    # example use cases, just press enter to use.
    # https://www.simplilearn.com/tutorials/cryptography-tutorial/aes-encryption
    if plaintext == "":
        plaintext = "Two One Nine Two"

    if key == "":
        key = "Thats my Kung Fu"

    print("Plaintext: ", plaintext)
    print("Key: ", key)

    # convert plaintext and key to bytes
    text_bytes = plaintext.encode('utf-8')
    key_bytes = key.encode('utf-8')

    text_array = []

    while (len(text_bytes) > 16):
        text_array.append(text_bytes[:16])
        text_bytes = text_bytes[16:]

    if len(text_bytes) <= 16:
        while len(text_bytes) < 16:
            text_bytes += b'\0'

        text_array.append(text_bytes)


    if len(key_bytes) != 16:
        print("Key must be 128 bits / 16 bytes")
        exit()


    for text in text_array:
        aes = AES(text, key_bytes)
        aes.main()
