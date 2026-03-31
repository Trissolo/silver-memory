
usable = dict()
[ usable.update({chr(n): f'{n:08b}'}) for n in range(8, 256)]

#file_path = '/home/tris/Downloads/utf_json.txt'
file_path = '/home/tris/Downloads/one_use/utf_json.txt'

lines = None
with open(file_path, 'r') as file:
    #print(f'there are {len(file.readlines())} lines')
    lines = (q for q in file.readlines())
    # print(f'{type(lines)}')

for l in lines:
    #print(l)
    for c in l:
        if c not in usable:
            print(f'Char {c} not allowed')
        # else:
        #     print(f'ok! -> {c} [{usable.get(c)}]')


### for fun
class StreamGen():
    def __init__(self):
        self.byte = 0
        self.idx = 0
        self.res = []
        self._allowed = {0, 1, '0', '1'}
        self.usable = dict()
        [self.usable.update({chr(n): f'{n:08b}'}) for n in range(8, 256)]
    def reset(self):
        self.byte = 0
        self.idx = 0
    def clearAll(self):
        self.reset()
        self.res.clear()
    @staticmethod
    def _integer_to_string(num):
        return f'{num:08b}'
    def addBit(self, bit = 0):
        if bit not in self._allowed:
            return
        if type(bit) is str:
            bit = 0 if bit == '0' else 1
        self.byte <<= 1
        self.idx +=1
        if bit:
            self.byte |= 1
        if self.idx == 8:
            self.res.append(self.byte)
            self.reset()
    def addChar(self, c):
        if c in self.usable:
            for bas in self.usable.get(c):
                self.addBit(bas)
    def get_output(self):
        self.finalize()
        for i, byte in enumerate(self.res):
            print(f'{i} {byte:08b} {byte:>3}')
        return self.res
    def finalize(self):
        if self.idx != 0:
            i = self.idx
            print(f'Last bit is incomplete. Idx = {i}')
            self.byte <<= (8 - i)
            self.res.append(self.byte)
            


st = StreamGen()


# for i in "01000111 00000111 01111011 1":
#     st.addBit(i)

# byte_arr = st.get_output()
# some_bytes = bytearray(byte_arr)

# # some_bytes.append(33)

# immutable_bytes = bytes(some_bytes)

# with open("my_file.txt", "wb") as binary_file:
#     binary_file.write(immutable_bytes)


# from: https://www.wscubetech.com/resources/dsa/huffman-code

import heapq
from collections import Counter

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.freq < other.freq
    
    def is_leaf(self):
        return self.left is None # and self.right is None

    def get_char(self):
        return self.char
    
    # def get_value(self):
    #     return self.value

class MyHuffman:
    def __init__(self, text):
        self.text = text
        self.root = self.build_huffman_tree(self.text)
        self.huffman_dict = {}

    def build_huffman_tree(self, text):
        frequency = Counter(text)
        heap = [Node(char, freq) for char, freq in frequency.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            merged = Node(None, left.freq + right.freq)
            merged.left = left
            merged.right = right
            heapq.heappush(heap, merged)

        return heap[0]

    def generate_codes(self, node, prefix, huffman_dict):
        if node:
            if node.char is not None:
                huffman_dict[node.char] = prefix
            self.generate_codes(node.left, prefix + "0", huffman_dict)
            self.generate_codes(node.right, prefix + "1", huffman_dict)
    def preOrder(self, node, res):
        if not node:
            return
        # Visit the current node first
        res.append(node.data)
        # Traverse the left subtree
        self.preOrder(node.left, res)
        # Traverse the right subtree
        self.preOrder(node.right, res)




    def huffman_encoding(self):
        text = self.text
        huffman_dict = self.huffman_dict
        self.generate_codes(self.root, "", huffman_dict)
        encoded_text = ''.join(huffman_dict[char] for char in text)
        return encoded_text


text = "HUFFMAN CODING IS FUN"
test_huff = MyHuffman(text)
encoded_text = test_huff.huffman_encoding() # huffman_encoding(text)
print("Encoded Text:", encoded_text)
print("Huffman Codes:", test_huff.huffman_dict)
