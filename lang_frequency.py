import re
import sys


def get_separator(sequence):
    for sign in ["\+", "/", "=", "\."]:
        if re.match("[\w-]+{}[\w-]+".format(sign), sequence):
            return sign


def load_data(filepath):
    with open(filepath) as text_file:
        text = text_file.read()
    return text


def get_most_frequent_words(text):
    sequence_pattern = re.compile("\(?[\w-]+[,\\.!\?:;\)]?", flags=re.U)
    double_sequence_pattern = re.compile("\(?[\w-]+[\+/=\.][\w-]+[,\\.!\?:;\)]?",
                                                                    flags=re.U)
    lines = text.split("\n")
    sequences = []
    for line in lines:
        sequences.extend(line.split(" "))
    words = []
    for sequence in sequences:
        if not re.match(".*\d.*", sequence):
            if re.match(sequence_pattern, sequence):
                words.append(re.sub("[,\\.!\?:;\)\(]", "", sequence).lower())
            elif re.match(double_sequence_pattern, sequence):
                words.extend(sequence.split(get_separator(re.sub(
                    "[,\\.!\?:;\)\(]","",
                    sequence).lower())))
    counts_dict = {}
    for word in words:
        if word in counts_dict:
            counts_dict[word] += 1
        else:
            counts_dict[word] = 1
    return sorted(counts_dict.items(), key=lambda x: x[1], reverse=True)


if __name__ == '__main__':
    filepath = sys.argv[1]
    text = load_data(filepath)
    counts = get_most_frequent_words(text)[:10]
    for item in counts:
        print("{}: {}".format(item[0], item[1]))
