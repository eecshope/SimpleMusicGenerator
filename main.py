import csv
import numpy as np
import json

from generator import Generator


def main():
    # read the markov matrix
    with open("data/sample.csv", "r") as file:
        reader = csv.reader(file, delimiter="\t")
        markov = [line for line in reader]
    header = markov[0]
    markov = np.asarray(markov[1:]).astype(np.float32)

    # build the init parameters
    pitch_vocab = dict({})
    for idx, pitch in enumerate(header):
        pitch_vocab[idx] = pitch
    with open("12.json", "r") as file:
        freq_table = json.load(file)

    music_generator = Generator(pitch_vocab, markov, freq_table, 0.001)
    music = music_generator.generate_and_play(20, "test.wav")
    print(music)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
