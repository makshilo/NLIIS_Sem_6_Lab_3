import nltk
from nltk.corpus import wordnet as wn
from nltk.tree import *
import xml.etree.ElementTree as ET


def generate_semantic_tree(text):
    text = text.replace('\n', '')
    if text != '':
        sentences = nltk.sent_tokenize(text)
        result = '(S '
        for sent in sentences:
            sent = sent.replace('.', '')
            sent = sent.replace(',', '')
            sent = sent.replace('?', '')
            doc = nltk.word_tokenize(sent)
            result_sent = '(SENT '
            for word in doc:
                if word.isalpha():
                    result_sent += get_word_semantic(word) + ' '
            result_sent += ')'
            result += result_sent
        result += ')'
        return nltk.tree.Tree.fromstring(result)


def get_word_semantic(word: str) -> str:
    if len(wn.synsets(word)) == 0:
        return '(WS (W ' + word + '))'
    result = '(WS (W ' + word + ') (DEF ' + wn.synsets(word)[0].definition().replace(' ', '_') + ')'
    synonyms, antonyms, hyponyms, hypernyms = [], [], [], []
    word = wn.synsets(word)
    syn_app = synonyms.append
    ant_app = antonyms.append
    he_app = hyponyms.append
    hy_app = hypernyms.append
    for synset in word:
        for lemma in synset.lemmas():
            syn_app(lemma.name())
            if lemma.antonyms():
                ant_app(lemma.antonyms()[0].name())
    for hyponym in word[0].hyponyms():
        he_app(hyponym.name())
    for hypernym in word[0].hypernyms():
        hy_app(hypernym.name())
    if len(synonyms):
        result += ' (SYN '
        for synonym in synonyms:
            result += synonym + ' '
    if len(antonyms):
        result += ') (ANT '
        for antonym in antonyms:
            result += antonym + ' '
    if len(hyponyms):
        result += ') (HY '
        for hyponym in hyponyms:
            result += hyponym + ' '
    if len(hypernyms):
        result += ') (HE '
        for hypernym in hypernyms:
            result += hypernym + ' '
    result += '))'
    return result


def tree_to_text(sem_tree):
    # Convert tree to text
    return TreePrettyPrinter(sem_tree).text()


def tree_to_xml(sem_tree):
    data = ET.Element('semantic_tree')
    sentences = sem_tree.subtrees()
    for sent in sentences:
        if sent.label() == 'SENT':
            sentence = ET.SubElement(data, 'sentence')
            words = sent.subtrees()
            for word in words:
                if word.label() == 'WS':
                    word_data = ET.SubElement(sentence, 'word')
                    word_data.text = word.leaves()[0]
                    ET.SubElement(word_data, 'word_params').set('params', word.leaves())
    return ET.tostring(data)
