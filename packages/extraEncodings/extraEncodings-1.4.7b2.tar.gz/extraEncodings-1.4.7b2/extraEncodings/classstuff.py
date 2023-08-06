import random
import extraEncodings.ciphers as ciphers
from ciphers import *
class TwoWayDict(dict):
    def __init__(self, my_dict):
        dict.__init__(self, my_dict)
        self.rev_dict = {v : k for k,v in my_dict.items()}

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)
        self.rev_dict.__setitem__(value, key)

    def pop(self, key):
        self.rev_dict.pop(self[key])
        dict.pop(self, key)
    def add(self,key,value):
        self.rev_dict[value] = key
        dict[value] = key
class Encoding():
    '''A way to generate a encoding for your purposes. \n
    Look at CreateAnEncoding.py to see an example of making an instance
    '''
    def __init__(self,rate):
        self.rate = rate
        x = 0
        self.encodingnormal = {}
        for letter in Encodeable_letters:
            x = x + rate
            self.encodingnormal[letter] = x
        self.encoding = TwoWayDict(self.encodingnormal)

class ListEncoding():
    def __init__(self,mix):
        self.encoding = []
        self.mix = mix
        for letter in Encodeable_letters:
            self.encoding.append(letter)
    def encode(self,Character_to_decode):
        Character_to_decode = str(Character_to_decode)
        for character in Character_to_decode:
            charpos = self.encoding.index(character)
            ResultStr = str(self.encoding[-charpos  -self.mix])
            print(ResultStr,end='')
class RandomEncoding():
    '''A way to generate a random encoding for your purposes. \n
    Encoding and decoding works the same as Encoding() \n
    Look at CreateAnEncoding.py and the Encoding() for an example of how to use it.
    '''
    def __init__(self,MaxRandom,MinRandom):
        self.rate = random.randint(MinRandom,MaxRandom)
        x = 0
        self.encodingnormal = {}
        for letter in Encodeable_letters:
            x = x + self.rate
            self.encodingnormal[letter] = x
        self.encoding = TwoWayDict(self.encodingnormal)
encoding1 = RandomEncoding(20,10)
print(encoding1.encoding[12])