

class Word():
    def __init__(self, word):
        '''
        IN: word, str: word to define
        VAR: pronounciation, str: phonetic spelling of word
        VAR: definition, dict(int: dict(str)): meanings of word
            e.g. {0 : {'pos': 'noun',
                       'definition': 'a clear explanation of word'},
                  1 : {'pos': 'adjective',
                       'definition': 'a descriptively delicious adjective'}
        VAR: parts_of_speech, list: all known parts of speech the word can be
                                    used in.
        '''
        self.id = word.lower()
        self.pronounciation = None
        self.definition = {}
        self.parts_of_speech = []
        self.no_of_senses = 0

    def addPronounciation(self, pronounce):
        self.pronounciation = pronounce

    def addDefinition(self, new_definition):
        try:
            new_pos = new_definition['pos']
            if new_pos not in self.parts_of_speech:
                self.parts_of_speech.append(new_pos)
        except KeyError:
            pass
        self.definition[self.no_of_senses] = new_definition
        self.no_of_senses += 1

    def getDefinitions(self):
        return self.definition

    def getPronounciation(self):
        return self.pronounciation
