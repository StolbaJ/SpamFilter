import os


class Corpus:
    def __init__(self, path):
        self.path = path

    def emails(self):
        files = os.listdir(os.path.join(self.path))
        for file in files:
            if file[0] != "!":
                with open(os.path.join(self.path, file), 'r', encoding='utf-8') as f:
                    if f.readable():
                        body = f.read()
                        yield file, body
