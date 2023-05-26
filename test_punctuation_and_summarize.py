import add_punctuation
import summarize_document

def test_from_file():
    #add_punctuation.add_punctuation(original_sentence)

    punctuatedText = "p.txt"
    summaryText = "s.txt"

    file = "test3.txt"
    lines = add_punctuation.from_file(file)

    with open(punctuatedText, mode='w') as f:
        f.writelines(lines)

    lines =  summarize_document.document_summarize(punctuatedText)

    with open(summaryText, mode='w') as f:
        f.writelines(lines)

def test_from_string():

    punctuatedText = "p.txt"
    string = "句読点ありバージョンを書きました句読点があることで僕は逆に、読みづらく感じるので、句読点無しで書きたいと思いますおはようございます"
    lines = add_punctuation.from_sentence(string)

    with open(punctuatedText, mode='w') as f:
        f.writelines(lines)

if __name__ == "__main__":
    test_from_file()
