
import re

import websearchdict.web.constants as wwc


def queueToDict(queue):
    '''
    All items are tagged with what type of data it is,
    - POS
    - DEFINITION
    - EXAMPLE
    - SYNONYM

    This groups the items in the list accordingly.  Groups always begin
    with a POS.
    '''
    definitions = []
    pos = None
    fed = None
    exa = []
    syn = None

    while len(queue) > 0:
        # Always start with POS
        if pos is None:
            pos = queue.pop(0)[1]

        if queue[0][0] != wwc.ID_POS:
            current_thing = queue.pop(0)
            if current_thing[0] == wwc.ID_DEFINITION:
                fed = current_thing[1]
            elif current_thing[0] == wwc.ID_EXAMPLE:
                exa.append(current_thing[1])
            elif current_thing[0] == wwc.ID_SYNONYM:
                syn = current_thing[1]
        else:
            # Summary results in entry
            definitions.append({
                'pos': pos,
                'definition': fed,
                'examples': exa,
                'synonyms': syn
            })
            pos = None
            exa = []
            syn = None
    return definitions


def acceptablePOS(possible_pos):
    '''
    Check whether the text is a valid POS qualifier
    '''
    positive = (lambda x: x.strip().lower() in wwc.POS_TAGS)
    if positive(possible_pos):
        return True

    multi = possible_pos.strip().split(',')
    if all([positive(i) for i in multi]):
        return True

    return False


def notBad(possible_definition, pos, word, example=False):
    rules = []
    results = []

    ''' Question whether the definition should be considered '''

    # Not a generic web blurb
    rules.append((lambda x: x not in wwc.MISC))
    # Not a POS
    # rules.append((lambda x: len(x.strip().split(' ')) > 1))
    rules.append((lambda x: x.strip().lower() not in wwc.POS_TAGS))

    for rule in rules:
        try:
            results.append(rule(possible_definition))
        except TypeError:
            if pos != 'determiner':
                # Word should not define itself
                results.append(rule(possible_definition, word))
                # TODO: Ignore lemmas
                if word[-1] == 's':
                    results.append(rule(possible_definition, word[0:-1]))
            results.append(rule(possible_definition, 'define'))
    # print(results)

    ''' Postprocessing to weed out null results '''

    if all(results):
        for nonsense in wwc.BAD_PHRASES:
            possible_definition = re.sub(nonsense, '', possible_definition)
        if possible_definition not in ['', ' ']:
            # print(possible_definition)
            # print("_-_-_-_")
            return possible_definition
    return None

# a = 'secondhand.'
# print(notBad(a, 'asdf', 'used'))
