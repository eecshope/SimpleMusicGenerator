import _pickle as pkl
import argparse
import json
import os
from generator import OrderOneGenerator, OrderTwoGenerator


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, help="the order of the markov matrix")
    parser.add_argument("--n_tokens", type=int, default=20, help="length of the music")
    parser.add_argument("--n_times", type=int, default=1, help="individual gen time")
    parser.add_argument("--bpm", type=int, default=240, help="speed of the music")
    parser.add_argument("--music_output_path", default="test.wav", help="path of the output music")
    parser.add_argument("--tone_output_path", default="test.json", help="path of the output json tone")
    parser.add_argument("--music_output_dir", default="output/music", help="dir of beam search music")
    parser.add_argument("--tone_output_dir", default="output/tone", help="dir of beam search tone")
    parser.add_argument("--beam_search", action="store_true", help="whether to use beam search")
    parser.add_argument("--beam_size", type=int, default=10, help="beam size")
    parser.add_argument("--random_walk", action="store_true", help="whether to use random walk")
    parser.add_argument("--random_walk_prob", type=float, default=0.1, help="prob for random walk")
    args = parser.parse_args()

    with open(f"data/order={args.order}.pkl", "rb") as file:
        obj = pkl.load(file)
        id_to_unit = obj["id_to_unit"]
        markov = obj["markov"]

    if args.order == 1:
        music_generator = OrderOneGenerator(id_to_unit, markov, args.random_walk_prob if args.random_walk else 0)
    else:
        music_generator = OrderTwoGenerator(id_to_unit, markov, args.random_walk_prob if args.random_walk else 0)

    if args.beam_search:
        args.music_output_dir += f"order={args.order}"
        args.tone_output_dir += f"order={args.order}"
        if not os.path.exists(args.music_output_dir):
            os.makedirs(args.music_output_dir)
        if not os.path.exists(args.tone_output_dir):
            os.makedirs(args.tone_output_dir)
        music_generator.beam_search(args.n_tokens, args.beam_size, args.bpm, args.music_output_dir,
                                    args.tone_output_dir)
    else:
        args.music_output_path = f"order={args.order}_" + args.music_output_path
        args.tone_output_path = f"order={args.order}_" + args.tone_output_path
        music = list([])
        for i in range(args.n_times):
            output_path = f"id={i}_" + args.music_output_path
            try:
                music.append(music_generator.generate_and_play(args.n_tokens, output_path, args.bpm))
            except ValueError as e:
                print(e)
                print("music sample has a vital fault")

        with open(args.tone_output_path, "w") as file:
            json.dump(music, file)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
