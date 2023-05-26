import add_punctuation

def test_from_file():
    #add_punctuation.add_punctuation(original_sentence)

    file = "test3.txt"
    add_punctuation.from_file(file)

def test_from_sentence():
    #sentence = "句読点ありバージョンを書きました句読点があることで僕は逆に、読みづらく感じるので、句読点無しで書きたいと思います。おはようございます"
    sentence = "句読点ありバージョンを書きました句読点があることで僕は逆に、読みづらく感じるので、句読点無しで書きたいと思いますおはようございます"
    add_punctuation.from_sentence(sentence)

if __name__ == "__main__":
    test_from_sentence()
