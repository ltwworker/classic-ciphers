# cryptanalysis.py
# Модуль содержит функции для криптоанализа

from encryption import get_alphabet, caesar_cipher


def frequency_analysis(text, language='russian'):
    alphabet = get_alphabet(language)
    text = ''.join([ch for ch in text.lower() if ch in alphabet])
    freq = {char: 0 for char in alphabet}
    for char in text:
        if char in freq:
            freq[char] += 1
    return {k: v for k, v in sorted(freq.items(), key=lambda item: item[1], reverse=True) if v > 0}


def crack_caesar(ciphertext, language='russian'):
    alphabet = get_alphabet(language)
    freq = frequency_analysis(ciphertext, language)
    if not freq:
        return None, "Текст пуст или не содержит букв"

    most_freq_char = list(freq.keys())[0]

    if language == 'russian':
        candidates = ['о', 'е', 'а', 'и', 'н', 'т', 'с']
    else:
        candidates = ['e', 't', 'a', 'o', 'i', 'n', 's']

    best_shift = 0
    best_result = None
    best_score = -1

    for lang_most_freq in candidates:
        shift = (alphabet.index(lang_most_freq) - alphabet.index(most_freq_char)) % len(alphabet)
        decrypted = caesar_cipher(ciphertext, shift, language)

        if language == 'russian':
            common_chars = 'оеаинтс'
        else:
            common_chars = 'etaoins'

        score = sum(1 for ch in decrypted.lower() if ch in common_chars)

        if best_result is None or score > best_score:
            best_score = score
            best_shift = shift
            best_result = decrypted

    return best_result, best_shift


def calculate_ic(text, language='russian'):
    alphabet = get_alphabet(language)
    text = ''.join([ch for ch in text.lower() if ch in alphabet])
    N = len(text)
    if N < 2:
        return 0.0
    freq = {char: 0 for char in alphabet}
    for char in text:
        if char in freq:
            freq[char] += 1
    sum_fi = sum([f * (f - 1) for f in freq.values()])
    ic = sum_fi / (N * (N - 1))
    return ic


def estimate_vigenere_key_length(ciphertext, max_key_len=20, language='russian'):
    ciphertext = ''.join([ch for ch in ciphertext.lower() if ch.isalpha()])
    if len(ciphertext) < 2:
        return 1, 0.0
    
    best_len = 1
    best_score = float('inf')
    
    for key_len in range(1, min(max_key_len, len(ciphertext)) + 1):
        avg_ic = 0.0
        count = 0
        for i in range(key_len):
            substring = ciphertext[i::key_len]
            if len(substring) > 1:
                ic = calculate_ic(substring, language)
                avg_ic += ic
                count += 1
        if count > 0:
            avg_ic /= count
            expected_ic = 0.056 if language == 'russian' else 0.066
            score = abs(avg_ic - expected_ic)
            if score < best_score:
                best_score = score
                best_len = key_len
    
    return best_len, best_score