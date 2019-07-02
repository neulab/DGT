"""plain2json.py: converts sentence-by-sentence translation results into a single
JSON file that is compatible to the submission format. In order to run, specify
the directory where your predictions exist:

    $ python plain2json.py --source-dir /path/to/translations --target-json submission.json

Tested with both Python 2 and 3.
"""
import argparse
import json
import sys
import os
import os.path as op

if sys.version_info[0] == 2:
    import codecs

    open = codecs.open


def assert_quit(condition, msg):
    try:
        assert condition
    except AssertionError:
        print(msg)
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Converter from plaintext translations to JSON.")
    parser.add_argument(
        "--source-dir",
        type=str,
        required=True,
        help="Source directory containing plaintext translations.",
    )
    parser.add_argument(
        "--target-json", type=str, required=True, help="Target JSON filename."
    )
    args = parser.parse_args()
    assert_quit(op.isdir(args.source_dir), "Please specify an existing directory.")

    gathered = []
    for filename in os.listdir(args.source_dir):
        id_ = ".".join(filename.split(".")[:-1])

        with open(op.join(args.source_dir, filename), "r") as f:
            sentences = [s.split(" ") for s in f.read().strip().split("\n")]
            summary = [word for sent in sentences for word in sent]

        gathered.append({"id": id_, "summary": summary})

    with open(args.target_json, "w") as f:
        json.dump(gathered, f, ensure_ascii=False)
