# DGT Task for WNGT 2019 at EMNLP19

This repository contains helper scripts and tools for the [DGT task](https://sites.google.com/view/wngt19/dgt-task) in [WNGT 2019](https://sites.google.com/view/wngt19/) at EMNLP19.

## Tools

### Tokenization

Participants might want to utilize external resources from the list on the task website. We provide
a word tokenizer and a sentnence tokenizer which were used to create RotoWire Parallel dataset.
One can apply them on a raw text to get the consistent tokenization as the provided dataset.

#### Requirements

Please use python version `>=3.5`. Run `pip install nltk` to install nltk and download punkt models
by opening up a python interpreter:

```sh
$ python
>>> import nltk
>>> nltk.download("punkt")
```

#### Usage

Two functions are defined in `tokenizer.py`.

- `word_tokenize(string: str, language: str) -> List[str]`: Tokenize a string into a list of words.
- `sent_tokenize(string: str, language: str) -> List[str]`: Tokenize a string into a list of sentences.

The second argument can be one of `english` and `german`, depending on the langauge you want to tokenize.
The default language is `english`.


#### Examples

```python
# Copy and place the file in your project directory, and import in your code
from tokenizer import tokenize, sent_tokenize

tokenize("Vince Carter is a basketball player.", language="english")
# ['Vince', 'Carter', 'is', 'a', 'basketball', 'player', '.']

sent_tokenize("Vince Carter is a basketball player. Michael Jordan is a basketball player.")
# ['Vince Carter is a basketball player.', 'Michael Jordan is a basketball player.']
```

If interested, more details on the construciton of the tokenizer is discussed [here](doc/constructing_tokenizer.md).

## Helper Scripts

We include the following helper scripts for processing the outputs before the submission. Both of
the scripts are tested with python 2 and 3.

### Convert from plain text to JSON format

Use `scripts/plain2json.py` to convert from plain text to JSON format. This script might be useful
for the participants in the MT track.

```sh
$ python plain2json.py --source-dir /path/to/sentence-by-sentence/translations --target-json output.json
```

### Validate the output before submission

Use `scripts/validate_outputs.py` to confirm that the submission file is valid and contains all the
outputs for evaluation.

```sh
$ python validate_outputs.py /path/to/your/submission/file
```

## Contacts

* `wngt2019-organizers` [at] `googlegroups.com`
