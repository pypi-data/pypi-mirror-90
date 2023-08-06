import pathlib
import tempfile
from collections import defaultdict

from os.path import isfile, isdir, join, basename
from statistics import mean, mode, median, stdev, quantiles
from typing import Optional

from .gibberish_score import GibberishScore, ProbabilityMarkovChain


def gibberish_score_factory(dataset_txt: str, model_pickle: Optional[str], threshold: bool = False) -> GibberishScore:
    if model_pickle is None:
        assert isfile(dataset_txt)
        model_pickle = join(tempfile.gettempdir(), f'{basename(dataset_txt)}.pickle')
        rmc = ProbabilityMarkovChain()
        rmc.training(dataset_txt)
        rmc.save_model(model_pickle)
    else:
        assert isfile(model_pickle)
        print(f'Model found at: {model_pickle}')
    gs = GibberishScore(model_pickle)
    if not threshold:
        return gs
    assert isfile(dataset_txt)
    with open(dataset_txt) as fp:
        words = {line: gs.get_gibberish_score(line) for line in fp.read().splitlines() if len(line) >= 2}
    len_to_gs = defaultdict(list)
    for k, v in words.items():
        len_to_gs[len(k)].append(v)
    if 'english_words.txt' in dataset_txt:  # precomputed
        gs.threshold = {2: 10, 3: 14, 4: 15, 5: 19, 6: 22, 7: 26, 8: 30, 9: 33, 10: 36, 11: 39, 12: 42, 13: 46, 14: 49,
                        15: 53, 16: 56, 17: 59, 18: 63, 19: 67, 20: 71, 21: 75, 22: 82, 23: 84, 24: 95, 25: 87, 27: 91}
    else:
        gs.threshold = {k: round(quantiles(v, n=10)[8]) for k, v in len_to_gs.items() if len(v) > 2}
    return gs


if __name__ == '__main__':
    pass
