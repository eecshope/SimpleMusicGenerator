import argparse
import numpy as np
import _pickle as pkl


def parse(sheet_path, output_path, order):
    """
    This is a function used to extract markov matrix from a given sheet

    :param sheet_path: path of the given sheet
    :param output_path: path of the output markov path
    :param order: order of the markov chain
    :return:
    """
    with open(sheet_path, "r") as file:
        tones = [ele.strip() for ele in file.readlines() if ele.strip() != ""]

    n_unit = len(set(tones))
    print(f"There are {n_unit} units in this sheet summarized from {len(tones)}")

    durations = [int(tone[-1]) for tone in tones]
    tones = [int(tone[:-1]) for tone in tones]
    unit_to_id = dict({})  # key: (tone, duration), value: matrix dim
    id_to_unit = dict({})  # key: matrix dim, value: (tone, duration)

    ptr = 0
    for tone, duration in zip(tones, durations):
        if (tone, duration) not in unit_to_id:
            unit_to_id[(tone, duration)] = ptr
            id_to_unit[ptr] = (tone, duration)
            ptr += 1

    markov = None
    if order == 1:
        markov = np.zeros((n_unit, n_unit), dtype=np.int32)
        for i in range(len(tones) - 1):
            markov[unit_to_id[(tones[i], durations[i])]][unit_to_id[(tones[i+1], durations[i+1])]] += 1

    elif order == 2:
        markov = np.zeros((n_unit, n_unit, n_unit), dtype=np.int32)
        for i in range(len(tones) - 2):
            n_0 = unit_to_id[(tones[i], durations[i])]
            n_1 = unit_to_id[(tones[i+1], durations[i+1])]
            n_2 = unit_to_id[(tones[i+2], durations[i+2])]
            markov[n_0][n_1][n_2] += 1

    with open(output_path, "wb") as file:
        output_dict = {"unit_to_id": unit_to_id,
                       "id_to_unit": id_to_unit,
                       "markov": markov}
        pkl.dump(output_dict, file)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, default=1)
    args = parser.parse_args()
    parse("data/data.txt", f"data/order={args.order}.pkl", args.order)


if __name__ == "__main__":
    main()
