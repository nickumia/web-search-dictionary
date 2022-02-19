
ID_POS = 0
ID_DEFINITION = 1
ID_EXAMPLE = 2
ID_SYNONYM = 3

POS_TAGS = [
    'noun',
    'adjective',
    'verb',
    'adverb',
    'determiner',
    'conjunction',
    'number',
    'pronoun',
    'preposition'
]

BAD_TAGS = [
    r'<style>.*?</style>',
    r'<img .*?">',
    r'<input .*?">',
    r'<br>',
    r'<script.*?</script>',
    r'<!--.*?-->',
    r'<meta .*?">',
    r'<hr( +)?>'
]

MISC = ['G', 'o', 'g', 'l', 'e', 'Videos', 'Please click', 'here', 'All',
        'News', 'Images', 'Videos', 'Maps', 'Shopping', 'Books', '×',
        'Search tools', 'Any time', 'Past hour', 'Past 24 hours', '',
        'Past week', 'Past month', 'Past year', 'All results', 'Verbatim',
        'Related searches', 'Next &gt;', '&nbsp;-&nbsp;', 'Learn more',
        'Sign in', 'Settings', 'Privacy', 'Terms', 'People also ask',
        'See results about', '·', 'More results', 'Rating', 'View all',
        'Best dictionary website', 'Duration:', 'In stock', 'Past participle:',
        'Cambridge Advanced...', 'Webster\'s Dictionary', 'Urban Dictionary',
        'Oxford English Di...', 'Dictionary sites for students', 'Merriam...',
        'Class parts of speech', 'Dictionary sites online']
# &#; Best Sellers &#;
# r'(Results )?[0-9]+ - [0-9]+ of [0-9]+',

BAD_PHRASES = [
    # Google suggestions / Dictionary Result Titles
    r'Define ([a-z]|[A-z])+( .*)?',
    r'([a-z]|[A-z])+ (d|D)efinition',
    r'Definition of ([a-z]|[A-z])+(.*)?',
    r'How to pronounce ([a-z]|[A-z])+',
    r'Example (of )?([a-z]|[A-z])+( .*)?',
    r'Meaning of ([a-z]|[A-z])+( .*)?',
    r'Past tense of [a-zA-Z]+',
    r'$[a-zA-Z]+ meaning',
    # Dates/Times/Money/Ratings
    r'([a-z]|[A-Z]){3} [0-9]{1,2}, [0-9]{4}',
    r'[0-9]{1,2}:[0-9]{2}',
    r'(\$?[0-9]+\.[0-9]{1,2}|\([0-9]+\)|^[0-9]$)',
    r'[0-9]+ days ago',
    # Misc
    r'.*?\?',
]
MARKETING = r'.*?/div/div/div/div\[[0-9]\]/div/span'

PRONUNCIATION = r'/(&#|[a-z}|[A-Z]|[0-9]|;|,|[^a-zA-Z\d\s])+/'
