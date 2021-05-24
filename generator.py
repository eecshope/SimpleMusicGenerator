import random
import numpy as np
import scipy.io.wavfile as wf


class Generator:
    def __init__(self, pitch_class_vocab, markov_matrix, freq_table, unit_time=0.1):
        self.pitch_class_vocab = pitch_class_vocab  # id to name
        self.pitch_list = list(self.pitch_class_vocab.keys())  # need to be aligned
        self.markov_matrix = markov_matrix
        self.n_pitch = len(pitch_class_vocab)
        self.freq_table = freq_table
        self.unit_time = unit_time

    def simple_generate(self, length):
        try:
            assert length > 0
        except AssertionError:
            print(f"Generated length should be larger than 0, but given {length}")
        start_point = random.sample(self.pitch_list, 1)[0]
        generated_tones = [start_point]

        # start generate new tones
        for i in range(length-1):
            last_tone = generated_tones[-1]
            probs = self.markov_matrix[last_tone]
            next_tone = np.random.choice(a=self.pitch_list, size=1, replace=True, p=probs)[0]
            generated_tones.append(next_tone)

        return generated_tones

    def play(self, tone_ids, output_path, sample_rate=44100):
        tones = [self.pitch_class_vocab[idx].split(".") for idx in tone_ids]
        tones = [(tone, int(duration)) for tone, duration in tones]

        music = np.empty(shape=1)

        # 合成波形文件数据
        for tone, duration in tones:
            times = np.linspace(0, duration, int(duration * sample_rate))
            sound = np.sin(2 * np.pi * self.freq_table[tone] * times)
            music = np.append(music, sound)
        music *= 2 ** 15
        music = music.astype(np.int16)

        # 写入波形文件
        wf.write(output_path, sample_rate, music)
        return tones

    def generate_and_play(self, length, output_path, sample_rate=44100):
        tone_ids = self.simple_generate(length)
        tones = self.play(tone_ids, output_path, sample_rate)
        return tones
