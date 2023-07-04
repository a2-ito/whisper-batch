def from_sentence(sentence):
    return sentence.replace("。", "。\n")

def from_file(file):
    with open(file, encoding='utf-8') as f:
        sentence = f.read()

    return from_sentence(sentence)
