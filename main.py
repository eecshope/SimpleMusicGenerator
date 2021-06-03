import _pickle as pkl
import argparse
from generator import OrderOneGenerator, OrderTwoGenerator


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int)
    args = parser.parse_args()

    with open(f"data/order={args.order}.pkl", "rb") as file:
        obj = pkl.load(file)
        id_to_unit = obj["id_to_unit"]
        markov = obj["markov"]

    if args.order == 1:
        music_generator = OrderOneGenerator(id_to_unit, markov)
    else:
        music_generator = OrderTwoGenerator(id_to_unit, markov)
    music = music_generator.generate_and_play(20, "test.wav", 240)
    print(music)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
