from functools import reduce

import nltk
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Get a list of portuguese synonyms')
    parser.add_argument('--file_name', type=str, default='../../data/synonyms_pt.txt',
                        help='file name')
    parser.add_argument('--download_dependencies', type=bool, default=True,
                        help='Download the text corpus and the wordnet')
    return parser.parse_args()


def download_dependencies():
    nltk.download('wordnet')
    nltk.download('floresta')
    nltk.download('mac_morpho')
    nltk.download('machado')
    nltk.download('omw')


def get_synonyms_word(word):
    sysnets = nltk.corpus.wordnet.synsets(word, lang='por')
    synonyms = set()
    for synset in sysnets:
        for lemma in synset.lemmas('por'):
            synonyms.add(lemma.name())
    return synonyms


def get_synonyms(file_name):
    synonyms = list()
    words = set()
    words.update(nltk.corpus.floresta.words())
    words.update(nltk.corpus.machado.words())
    words.update(nltk.corpus.mac_morpho.words())

    words = set(nltk.corpus.floresta.words())
    words.update(nltk.corpus.mac_morpho.words())
    for word in words:
        synonyms_word = get_synonyms_word(word)
        if len(synonyms_word) > 1 and synonyms_word not in synonyms:
            synonyms.append(synonyms_word)

    with open(file_name, 'w') as file:
        for synonym_line in synonyms:
            file.write(reduce(lambda x, y: x + ', ' + y, synonym_line, '')[2:] + '\n')


def main():
    args = parse_args()
    if args.download_dependencies:
        download_dependencies()
    get_synonyms(args.file_name)


if __name__ == '__main__':
    main()
