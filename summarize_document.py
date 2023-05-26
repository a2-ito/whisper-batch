from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
from pysummarization.tokenizabledoc.mecab_tokenizer import MeCabTokenizer
from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor

def document_summarize(file):

    #ファイルの読み込み
    with open(file,encoding='utf-8') as f:
        contents = f.readlines()

    #全ての行を結合
    document = ''.join(contents)
    # 自動要約のオブジェクトを生成
    auto_abstractor = AutoAbstractor()
    # トークナイザー（単語分割）にMeCabを指定
    auto_abstractor.tokenizable_doc = MeCabTokenizer()
    # 文書の区切り文字を指定
    auto_abstractor.delimiter_list = ["。", "\n"]
    # キュメントの抽象化、フィルタリングを行うオブジェクトを生成
    abstractable_doc = TopNRankAbstractor()
    # 文書の要約を実行
    result_dict = auto_abstractor.summarize(document, abstractable_doc)

    for x in zip(result_dict['scoring_data'],result_dict["summarize_result"]):
        print(x)

    return [x.replace('\n','') for x in result_dict["summarize_result"]]


