import os
import re
from collections import defaultdict

import utils
import corpus
# pattern for mail find in text
pattern = re.compile("([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+")

# so we can edit sensitivity without looking into code
with open("options.txt", "r", encoding='utf-8') as f:
    contents = f.read()
    stripped = contents.strip()
    splitted = stripped.split()
    threshold = float(splitted[1])
    ifInSpamListAdd = float(splitted[3])
    ifInOkListMinus = float(splitted[5])


class MyFilter:
    def __init__(self):
        self.spam_words = defaultdict(int)
        self.ok_words = defaultdict(int)
        self.spam_messages = 0
        self.ok_messages = 0
        self.spam_mails = []
        self.ok_mails = []

    def train(self, path):
        dictionary = utils.read_classification_from_file(os.path.join(path, "!truth.txt"))
        corp = corpus.Corpus(path)
        for fname, body in corp.emails():
            words = re.findall(r'\b\w+\b', body.lower())
            a = re.search(pattern, body)
            if dictionary[fname] == "SPAM":
                self.spam_mails.append(a.string)
                self.spam_messages += 1
                for word in words:
                    self.spam_words[word] += 1
            else:
                #if a was in spam list remove it
                if a in self.spam_mails:
                    self.spam_mails.remove(a)
                self.ok_mails.append(a.string)
                self.ok_messages += 1
                for word in words:
                    self.ok_words[word] += 1

    def calculate_word_probability(self, word, is_spam):
        # laplacian smoothing so if some word isn't in list it doesn't mess with results
        if is_spam:
            return (self.spam_words[word] + 1) / (self.spam_messages + 2)
        else:
            return (self.ok_words[word] + 1) / (self.ok_messages + 2)

    def calculate_spam_probability(self, message):
        words = re.findall(r'\b\w+\b', message.lower())
        spam_prob = 1.0
        ok_prob = 1.0

        # generate spam/ok prob based on words in message
        for word in words:
            spam_prob *= self.calculate_word_probability(word, is_spam=True)
            ok_prob *= self.calculate_word_probability(word, is_spam=False)

        total_messages = self.spam_messages + self.ok_messages
        if total_messages > 0:
            spam_prob *= self.spam_messages / total_messages
            ok_prob *= self.ok_messages / total_messages
        else:
            # if no words in message
            spam_prob = 0.5
            ok_prob = 0.5
        # so if the probability is too low that it's zero return normal low number
        try:
            return spam_prob / (spam_prob + ok_prob)
        except ZeroDivisionError:
            return 0.01

    def test(self, path):
        file = open(os.path.join(path, "!prediction.txt"), 'w', encoding='utf-8')
        corp = corpus.Corpus(path)
        for fname, body in corp.emails():
            spam_probability = 0
            spam_probability += self.calculate_spam_probability(body)
            a = re.search(pattern, body)
            if a:
                if a.string in self.spam_mails:
                    spam_probability += ifInSpamListAdd
                else:
                    spam_probability -= ifInOkListMinus
            if spam_probability > threshold:
                result = " SPAM"
            else:
                result = " OK"
            file.write(fname + result + "\n")
        file.close()
