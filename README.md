# SimpleMusicGenerator

Required package:
- PySynth `git clone git@github.com:mdoege/PySynth.git` `python setup.py install`


Usage:

If you want to generate one music scrap with Order-one Markov Matrix, run the following order in the main directory:
```shell
python main.py --order=1
```

Else, if you want a scrap from Order-two Markov Matrix, the order is
```shell
python main.py --order=2
```

If you want to do beam search, just use 
```shell
python main.py --order=[your order] --beam_search
```

As for other options, use the following order to understand them
```shell
python main.py -h
```

For statistic analysis, just review the generated json files.