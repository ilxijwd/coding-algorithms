import json
import math


def load_appearances(filename):
    return json.load(open(filename, 'r', encoding='utf-8'))


def generate_appearances(msg, appearance_map):
    result = {}
    total_appearance = 0

    for letter in "".join(set(msg)):
        if letter in appearance_map:
            letter_appearance = appearance_map[letter]
            result[letter] = letter_appearance
            total_appearance += letter_appearance

    for letter, appearance in result.items():
        result[letter] = appearance / total_appearance

    return result


def print_map(map):
    for key, value in map.items():
        if type(value) == float:
            print(f'\t-> {key}: {value:.6f}')
        elif type(value) == str:
            print(f'\t-> {key}: {value}')


def calculate_entropy(alphabet, k):
    return -k * sum([value * math.log2(value) for value in alphabet.values()])


def calculate_compression(entropy, appearances_map):
    return entropy / math.log2(len(appearances_map))
