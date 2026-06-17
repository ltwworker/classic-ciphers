def get_alphabet(language='russian'):
    if language == 'russian':
        return 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    else:
        return 'abcdefghijklmnopqrstuvwxyz'


def caesar_cipher(text, shift, language='russian'):
    alphabet = get_alphabet(language)
    result = ''
    for char in text:
        if char.lower() in alphabet:
            is_upper = char.isupper()
            idx = alphabet.index(char.lower())
            new_idx = (idx + shift) % len(alphabet)
            new_char = alphabet[new_idx]
            result += new_char.upper() if is_upper else new_char
        else:
            result += char
    return result


def vigenere_cipher(text, key, encrypt=True, language='russian'):
    alphabet = get_alphabet(language)
    key = key.lower()
    result = ''
    key_index = 0
    for char in text:
        if char.lower() in alphabet:
            is_upper = char.isupper()
            idx = alphabet.index(char.lower())
            shift = alphabet.index(key[key_index % len(key)])
            if not encrypt:
                shift = -shift
            new_idx = (idx + shift) % len(alphabet)
            new_char = alphabet[new_idx]
            result += new_char.upper() if is_upper else new_char
            key_index += 1
        else:
            result += char
    return result


class PolybiusCipher:
    
    def __init__(self, language='russian'):
        self.language = language
        self.size = 6 if language == 'russian' else 5
        self.alphabet = get_alphabet(language)
        if language == 'english':
            self.alphabet = self.alphabet.replace('j', '')
        self.table = self._generate_table()
        self.char_to_coords = {}
        self.coords_to_char = {}
        self._build_mappings()
    
    def _generate_table(self):
        table = []
        idx = 0
        for i in range(self.size):
            row = []
            for j in range(self.size):
                if idx < len(self.alphabet):
                    row.append(self.alphabet[idx])
                    idx += 1
                else:
                    row.append('')
            table.append(row)
        return table
    
    def _build_mappings(self):
        for i in range(self.size):
            for j in range(self.size):
                char = self.table[i][j]
                if char:
                    self.char_to_coords[char] = (i, j)
                    self.coords_to_char[(i, j)] = char
    
    def encrypt(self, text):
        text = text.lower()
        result = ''
        for char in text:
            if char in self.char_to_coords:
                row, col = self.char_to_coords[char]
                result += f"{row+1}{col+1}"
            else:
                result += char
        return result
    
    def decrypt(self, ciphertext):
        result = ''
        i = 0
        while i < len(ciphertext):
            if i+1 < len(ciphertext) and ciphertext[i].isdigit() and ciphertext[i+1].isdigit():
                row = int(ciphertext[i]) - 1
                col = int(ciphertext[i+1]) - 1
                if (row, col) in self.coords_to_char:
                    result += self.coords_to_char[(row, col)]
                i += 2
            else:
                result += ciphertext[i]
                i += 1
        return result