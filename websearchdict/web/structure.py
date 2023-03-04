
import logging
import re

import websearchdict.web.constants as wwc


logger = logging.getLogger(__name__)


def queueToDict(queue, one_more=False):
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
    if one_more:
        definitions.append({
            'pos': pos,
            'definition': fed,
            'examples': exa,
            'synonyms': syn
        })
    return definitions


def acceptablePOS(possible_pos):
    '''
    Check whether the text is a valid POS qualifier
    '''
    positive = (lambda x: x.strip().lower() in wwc.POS_TAGS)
    if positive(possible_pos):
        return True

    multi = possible_pos.split(',')
    if all([positive(i) for i in multi]):
        return True

    return False


def notBad(possible_definition, pos, word, example=False):
    rules = []
    results = []

    ''' Question whether the definition should be considered '''

    # Not a generic web blurb nor a POS
    rules.append((lambda x: x not in wwc.MISC))
    rules.append((lambda x: not acceptablePOS(x)))

    for rule in rules:
        results.append(rule(possible_definition))
    logger.debug('notBad Definitions')
    logger.debug(results)

    ''' Postprocessing to weed out null results '''

    if all(results):
        for nonsense in wwc.BAD_PHRASES:
            possible_definition = re.sub(nonsense, '', possible_definition)
        if possible_definition not in ['', ' ']:
            return possible_definition
    return None

# a = 'used to link alternatives.'
# print(notBad(a, 'asdf', 'used'))
# print(acceptablePOS('N'))
