from transformers import pipeline, logging

def insert_char_to_sentence(i, char, sentence): # sentenceのi文字目にcharを挿入する
    l = list(sentence)
    l.insert(i, char)
    text = "".join(l)
    return text

def add_punctuation(corrected_sentence):

    nlp = pipeline("fill-mask", model="cl-tohoku/bert-base-japanese-char")
    thresh = 0.5 # このスコア以上の場合、句読点を挿入する
    i = 0
    punctuations = ["、", "。", "?"]
    chars_after_mask = 100

    while i < len(corrected_sentence):
        i += 1
        if corrected_sentence[i-1] in punctuations: continue # 句読点が連続してくることはない
        masked_text = insert_char_to_sentence(i, nlp.tokenizer.mask_token, corrected_sentence)

        # 入力値に句点が含まれている場合、句点で split したセンテンスに mask_token が含まれていないので split できない
        pre_context, post_context = masked_text.split("。")[-1].split(nlp.tokenizer.mask_token)
        res = nlp(f"{pre_context}{nlp.tokenizer.mask_token}{post_context[:chars_after_mask]}")[0] # scoreが一番高い文
        if res["token_str"] not in punctuations: continue
        if res["score"] < thresh: continue

        punctuation = res["token_str"] if res["token_str"] != "?" else "。" # 今回は"？"は"。"として扱う
        corrected_sentence = insert_char_to_sentence(i, punctuation, corrected_sentence)

    #print(corrected_sentence)
    return corrected_sentence
    # Todo: corrected_sentence の句点で改行する

def from_sentence(sentence):
    logging.set_verbosity_error()
    lines = ""

    for splitted_sentence in sentence.split("。"):
        lines += add_punctuation(splitted_sentence)

    return lines

def from_file(file):
    with open(file, encoding='utf-8') as f:
        sentence = f.read()

    return from_sentence(sentence)

# 1. 前処理：句点で改行する
# 2. 改行単位で句読点挿入を実行する（句点を削除しておいて、最終的には再挿入する）
