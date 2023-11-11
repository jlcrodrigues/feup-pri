import nltk
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Get stopwords')
    parser.add_argument('--language', type=str, default='portuguese',
                        help='language')
    parser.add_argument('--file_name', type=str, default='../../data/stopwords.txt',
                        help='file name')
    return parser.parse_args()


def get_stopwords(language, file_name):
    nltk.download('stopwords')
    words = set(nltk.corpus.stopwords.words(language))
    with open(file_name, 'w') as file:
        for word in words:
            file.write(word + '\n')


def main():
    args = parse_args()
    get_stopwords(args.language, args.file_name)


if __name__ == '__main__':
    main()
