import _pickle as pkl
from generator import Generator


def main():

    with open("data/order=1.pkl", "rb") as file:
        obj = pkl.load(file)
        id_to_unit = obj["id_to_unit"]
        markov = obj["markov"]

    music_generator = Generator(id_to_unit, markov, 0.00000001)
    music = music_generator.generate_and_play(20, "test.wav")
    print(music)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
