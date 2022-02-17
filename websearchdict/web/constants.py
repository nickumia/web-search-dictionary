
POS_TAGS = [
    'noun',
    'adjective',
    'verb',
    'adverb',
    'determiner',
    'conjunction',
    'number',
    'pronoun'
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
        'Best dictionary website', 'Duration:']

BAD_PHRASES = [
    # Google suggestions / Dictionary Result Titles
    r'Define ([a-z]|[A-z])+( .*)?',
    r'([a-z]|[A-z])+ (d|D)efinition',
    r'Definition of ([a-z]|[A-z])+(.*)?',
    r'How to pronounce ([a-z]|[A-z])+',
    r'Example (of )?([a-z]|[A-z])+( .*)?',
    r'([a-zA-Z])+( \([a-zA-Z]+\))?((d|D)efinition |(and|&) |(m|M)eaning|'
    r',| |(s|S)ynonyms?|(e|E)xamples?)+ \| .*',
    r'(A Definition)? &amp; Meaning (-|\|) ',
    r'Meaning of ([a-z]|[A-z])+( .*)?',
    r'.*? - Investopedia',
    r'.*(t|T)hesaurus.*',
    # Dates/Times/Money/Ratings
    r'([a-z]|[A-Z]){3} [0-9]{1,2}, [0-9]{4}',
    r'[0-9]{1,2}:[0-9]{2}',
    r'(\$?[0-9]+\.[0-9]{1,2}|\([0-9]+\)|^[0-9]$)',
    r'[0-9]+ days ago',
    r'(Results )?[0-9]+ - [0-9]+ of [0-9]+',
    # Misc
    r'.*&#; Best Sellers &#;.*',
    r'.*&#8250;.*',
    r'.*?\?',
    r'(Merriam-Webster|Vocabulary\.com|(Best English )?Dictionary(\.com)?|'
    r'Purdue Online Writing Lab|Merriam...|Urban|Webster\'s|Cambridge Advanced'
    r'...|Best dictionary website|In stock|Wikipedia|Noun:?|Collins English '
    r'Di...|Past participle:|Adverb and Its Kinds|Adjective:?|Verb:?|Oxford '
    r'English Di...| ?sites for students|He/she/it:|People also search for:|'
    r'Superlative:|Adv:)'
]

PRONUNCIATION = r'/(&#|[a-z}|[A-Z]|[0-9]|;|,|[^a-zA-Z\d\s])+/'
