import random
import pysynth
import numpy as np

PITCH_CLASS_MAP = {1: "a4", 2: "a#4", 3: "b4", 4: "c5", 5: "c#5", 6: "d5", 7: "d#5", 8: "e5", 9: "f5", 10: "f#5",
                   11: "g5", 12: "g#5", 13: "a5", 14: "a#5", 15: "b5", 16: "c6", 17: "c#6"}
DURATION_MAP = {1: 4, 2: 2, 3: -2, 4: 1}
PITCH_RANGE = 17

FREQ_TABLE = {
    "C0": 16.35, "C#0": 17.32, "D0": 18.35, "D#0": 19.45, "E0": 20.60, "F0": 21.83, "F#0": 23.12, "G0": 24.50,
    "G#0": 25.96, "A0": 27.50, "A#0": 29.14, "B0": 30.87,
    "C1": 32.70, "C#1": 34.65, "D1": 36.71, "D#1": 38.89, "E1": 41.20, "F1": 43.65, "F#1": 46.25, "G1": 49.00,
    "G#1": 51.91, "A1": 55.00, "A#1": 58.27, "B1": 61.74,
    "C2": 65.41, "C#2": 69.30, "D2": 73.42, "D#2": 77.78, "E2": 82.41, "F2": 87.31, "F#2": 92.50, "G2": 98.00,
    "G#2": 103.83, "A2": 110.00, "A#2": 116.54, "B2": 123.47,
    "C3": 130.81, "C#3": 138.59, "D3": 146.83, "D#3": 155.56, "E3": 164.81, "F3": 174.61, "F#3": 185.00, "G3": 196.00,
    "G#3": 207.65, "A3": 220.00, "A#3": 233.08, "B3": 246.94,
    "C4": 261.63, "C#4": 277.18, "D4": 293.66, "D#4": 311.13, "E4": 329.63, "F4": 349.23, "F#4": 369.99, "G4": 392.00,
    "G#4": 415.30, "A4": 440.00, "A#4": 466.16, "B4": 493.88,
    "C5": 523.25, "C#5": 554.37, "D5": 587.33, "D#5": 622.25, "E5": 659.25, "F5": 698.46, "F#5": 739.99, "G5": 783.99,
    "G#5": 830.61, "A5": 880.00, "A#5": 932.33, "B5": 987.77,
    "C6": 1046.50, "C#6": 1108.73, "D6": 1174.66, "D#6": 1244.51, "E6": 1318.51, "F6": 1396.91, "F#6": 1479.98,
    "G6": 1567.98, "G#6": 1661.22, "A6": 1760.00, "A#6": 1864.66, "B6": 1975.53,
    "C7": 2093.00, "C#7": 2217.46, "D7": 2349.32, "D#7": 2489.02, "E7": 2637.02, "F7": 2793.83, "F#7": 2959.96,
    "G7": 3135.96, "G#7": 3322.44, "A7": 3520.00, "A#7": 3729.31, "B7": 3951.07,
    "C8": 4186.01, "C#8": 4434.92, "D8": 4698.63, "D#8": 4978.03, "E8": 5274.04, "F8": 5587.65, "F#8": 5919.91,
    "G8": 6271.93, "G#8": 6644.88, "A8": 7040.00, "A#8": 7458.62, "B8": 7902.13
}


class Generator:
    def __init__(self, id_to_unit, markov_matrix):
        self.id_to_unit = id_to_unit
        self.unit_list = list(self.id_to_unit.keys())  # need to be aligned
        self.markov_matrix = markov_matrix
        self.n_pitch = len(self.unit_list)

    def simple_generate(self, length):
        pass

    def play(self, tone_ids, output_path, bpm=120):
        _tones = [self.id_to_unit[idx] for idx in tone_ids]
        tones = list([])
        for tone, duration in _tones:
            while duration > 0:
                tones.append((PITCH_CLASS_MAP[tone], DURATION_MAP[(duration-1) % 4 + 1]))
                duration -= 4
        pysynth.make_wav(tones, fn=output_path, bpm=bpm)
        return tones

    def generate_and_play(self, length, output_path, bpm=120):
        tone_ids = self.simple_generate(length)
        tones = self.play(tone_ids, output_path, bpm)
        return tones


class OrderOneGenerator(Generator):
    def __init__(self, id_to_unit, markov_matrix):
        super(OrderOneGenerator, self).__init__(id_to_unit, markov_matrix)
        row_sum = np.sum(self.markov_matrix, -1, keepdims=True)
        row_sum[row_sum == 0] = 1
        self.markov_matrix = np.divide(self.markov_matrix, row_sum)

    def simple_generate(self, length):
        try:
            assert length > 0
        except AssertionError:
            print(f"Generated length should be larger than 0, but given {length}")
        start_point = random.sample(self.unit_list, 1)[0]
        generated_tones = [start_point]

        for i in range(length - 1):
            last_tone = generated_tones[-1]
            probs = self.markov_matrix[last_tone]
            next_tone = np.random.choice(a=self.unit_list, size=1, replace=True, p=probs)[0]
            generated_tones.append(next_tone)

        return generated_tones


class OrderTwoGenerator(Generator):
    def __init__(self, id_to_unit, markov_matrix):
        super(OrderTwoGenerator, self).__init__(id_to_unit, markov_matrix)
        order_1_matrix = self.markov_matrix.sum(axis=-1)
        row_sum = np.sum(order_1_matrix, -1, keepdims=True)
        row_sum[row_sum == 0] = 1
        self.order_one_matrix = np.divide(order_1_matrix, row_sum)

        row_sum = np.sum(self.markov_matrix, -1, keepdims=True)
        row_sum[row_sum == 0] = 1
        self.markov_matrix = np.divide(self.markov_matrix, row_sum)

    def simple_generate(self, length):
        try:
            assert length > 1
        except AssertionError:
            print(f"Generated length should be larger than 1, but given {length}")
        start_point = random.sample(self.unit_list, 1)[0]
        generated_tones = [start_point, np.random.choice(a=self.unit_list, size=1, replace=True,
                                                         p=self.order_one_matrix[start_point])[0]]

        for i in range(length - 2):
            last_one = generated_tones[-2]
            last_two = generated_tones[-1]
            probs = self.markov_matrix[last_one][last_two]
            if probs.sum().data == 0:
                probs = self.order_one_matrix[last_two]
            next_tone = np.random.choice(a=self.unit_list, size=1, replace=True, p=probs)[0]
            generated_tones.append(next_tone)

        return generated_tones
