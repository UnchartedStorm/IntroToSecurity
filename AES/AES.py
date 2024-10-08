"""
This file is an implementation of the AES encryption algorithm.
The algorithm can be run by simply running the file and following the prompts.
The prompts can be left blank to run the example use case:
    Plaintext: Two One Nine Two
    Key: Thats my Kung Fu
Which should output the following ciphertext:
    29c3505f571420f6402299b31a02d73a

The key should be 128 bits / 16 bytes long.
The plaintext can be any length, but will be padded with null bytes to 16 bytes.

Group: ¯\_(ツ)_/¯
Bruno Sprenger  StudentID: 13084151
Ray Zhang       StudentID: 15772829
"""

import numpy as np

class AES:
    # AES Rijndael S-box.
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

    def __init__(self, plaintext, key) -> None:
        # The number of rounds.
        self.Nr = 10
        # The number of columns in state(or words in key).
        self.Nk = 4
        # Create state
        self.create_state(plaintext)

        # Create keys for each round, requires the s_box.
        self.create_keys(key)

    def print(self) -> None:
        # This function is used for debugging purposes and prints the state.
        for i in range(4):
            for j in range(4):
                print(hex(self.state[j][i]), end=' ')
            print()

        print()

    def print_keys(self) -> None:
        # This function is used for debugging purposes and prints the keys.
        for i in range(11):
            print(f"Round {i} key")
            for j in range(4):
                for k in range(4):
                    print(hex(self.key[i][k][j]), end=' ')
                print()
            print()

    def create_state(self, plaintext) -> None:
        # This creates the state from the plaintext.
        if plaintext:
            self.state = np.array([[plaintext[i + j] for j in range(4)] for i in range(0, 16, 4)])
        else:
            self.state = np.array([[0 for _ in range(4)] for _ in range(4)])

    # The next 3 functions are used for key creation.
    def sub_word(self, word):
        # This function substitutes each byte in the word with the corresponding byte in the s_box.
        for i in range(len(word)):
            word[i] = AES.s_box[word[i]]
        return word

    def rot_word(self, word):
        # This function rotates the word by one byte.
        word = np.roll(word, -1)
        return word

    def create_keys(self, key) -> None:
        # This function creates an array of keys for each round.
        self.key = np.zeros((self.Nr + 1, 4, 4), dtype=int)

        # Rcon array.
        rcon = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]

        # Initialize with given key.
        for i in range(4):
            for j in range(4):
                self.key[0][i][j] = key[4*i + j]

        # Generate round keys.
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

    def sub_bytes(self, state) -> None:
        # This substitutes each byte in the state with the corresponding byte in the s_box.
        for i in range(4):
            for j in range(4):
                state[i][j] = AES.s_box[state[i][j]]

    def shift_rows(self, state) -> None:
        # This shifts the rows in the state by i positions.
        for i in range(4):
            state[:, i] = np.roll(state[:, i], -i)

    # Multiplying by 2 in GF(2^8).
    def xtimes(self, x):
        # If MSB is 1, then it will overflow.
        if x & 0x80:
            return ((x << 1) ^ 0x11B)
            # (x << 1) ^ 0x1B) & 0xFF also does the same thing.
        return x << 1

    def mix_columns(self, state) -> None:
        # This mixes the columns in the state.
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

    # Multiply by 0x09 in GF(2^8).
    def mul9(x):
        return aes.xtimes(aes.xtimes(aes.xtimes(x))) ^ x

    # Multiply by 0x0B in GF(2^8).
    def mul11(x):
        return aes.xtimes(aes.xtimes(aes.xtimes(x))) ^ aes.xtimes(x) ^ x

    # Multiply by 0x0D in GF(2^8).
    def mul13(x):
        return aes.xtimes(aes.xtimes(aes.xtimes(x))) ^ aes.xtimes(aes.xtimes(x)) ^ x

    # Multiply by 0x0E in GF(2^8).
    def mul14(x):
        return aes.xtimes(aes.xtimes(aes.xtimes(x))) ^ aes.xtimes(aes.xtimes(x)) ^ aes.xtimes(x)

    def add_round_key(self, state, round) -> None:
        # xor hex values.
        for i in range(4):
            for j in range(4):
                state[i][j] ^= self.key[round][i][j]

    def state_to_text(self, state) -> str:
        # Concatenate state.
        text = ""
        for i in range(4):
            for j in range(4):
                # Add hex value to text by slicing off the '0x' prefix.
                text += hex(state[i][j])[2:]

        return text

    def encrypt(self) -> None:
        # All print statements are commented out, but can be uncommented for debugging purposes.

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


if __name__ == "__main__":
    # Prompt user for plaintext and key.
    plaintext = input("Enter plaintext: ")
    key = input("Enter key: ")

    # Example use case, if no input is given.
    if plaintext == "":
        plaintext = "Two One Nine Two"

    if key == "":
        key = "Thats my Kung Fu"

    print("Plaintext: ", plaintext)
    print("Key: ", key)

    # Convert plaintext and key to bytes
    text_bytes = plaintext.encode('utf-8')
    key_bytes = key.encode('utf-8')

    # Pad text with null bytes if it is less than 16 bytes
    if len(text_bytes) <= 16:
        while len(text_bytes) < 16:
            text_bytes += b'\0'

    if len(key_bytes) != 16:
        print("Key must be 128 bits / 16 bytes")
        exit()

    if len(text_bytes) != 16:
        print("Plaintext must be 128 bits / 16 bytes")
        exit()

    aes = AES(text_bytes, key_bytes)
    aes.encrypt()
