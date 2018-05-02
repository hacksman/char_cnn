# -*- coding: utf-8 -*-
# @Time    : 4/25/18 8:29 AM

import pickle
import numpy as np
import copy


def batch_generator(arr, n_seqs, n_steps):
    arr = copy.copy(arr)
    batch_size = n_seqs * n_steps
    n_batches = int(len(arr)/batch_size)
    arr = arr[:n_batches * batch_size]
    arr = arr.reshape((n_seqs, -1))
    while True:
        np.random.shuffle(arr)
        for n in range(0, arr.shape[1], n_steps):
            x = arr[:, n:n + n_steps]
            y = np.zeros_like(x)
            y[:, :-1], y[:, -1] = x[:, 1:], x[:, 0]
            yield x, y

class TextCoverter(object):

    def __init__(self, text=None, max_vocab=5000, filename=None):
        if filename is not None:
            with open(filename, 'rb') as f:
                self.vocab = pickle.load(f)
        else:
            vocab = set(text)
            vocab_count = {}
            for word in vocab:
                vocab_count[word] = 0

            for word in text:
                vocab_count[word] += 1

            vocab_count_list = [(i, vocab_count[i]) for i in vocab_count]
            vocab_count_list.sort(key=lambda x: x[1], reverse=True)
            vocab = [x[0] for x in vocab_count_list]
            self.vocab = vocab

        self.word_to_int_table = {c: i for i, c in enumerate(self.vocab)}
        self.int_to_word_table = dict(enumerate(self.vocab))


    def text_to_arr(self, text):
        arr = [self.word_to_int_table[word] for word in text]
        return np.array(arr)

    def arr_to_text(self, arr):
        words = [self.int_to_word(index) for index in arr]
        return ''.join(words)

    def int_to_word(self, index):
        if index == len(self.vocab):
            return '<unk>'
        elif index < len(self.vocab):
            return self.int_to_word_table[index]
        else:
            raise Exception('Unknow index')

    @property
    def vocab_size(self):
        return len(self.vocab) + 1


    def save_to_file(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.vocab, f)


