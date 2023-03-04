
ID_POS = "pos"
ID_DEFINITION = "def"
ID_EXAMPLE = "exa"
ID_SYNONYM = "syn"

POS_TAGS = [
    'noun',
    'adjective',
    'verb',
    'adverb',
    'determiner',
    'conjunction',
    'number',
    'pronoun',
    'preposition',
    'predeterminer'
]

BAD_TAGS = [
    r'<style>.*?</style>',
    r'<img .*?" ?/?>',
    r'<link .*?"/?>',
    r'<source .*?" ?/?>',
    r'<input .*?" ?/?>',
    r'<br ?/?>',
    r'<script.*?</script>',
    r'<nav.*?</nav>',
    r'<!--.*?-->',
    r'<meta .*?"/?>',
    r'<hr ?.*?"?/?>'
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
        'Class parts of speech', 'Dictionary sites online',
        'Adverb and Its Kinds', 'SI unit:',
        'Dictionary buy', 'The Merriam...', 'Oxford Dictionary...',
        'Black\'s Law Dictionary']
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
    r'[a-zA-Z\/]+:',
    r'^&#[A-F0-9]+;$',
    r'Â.',
]
MARKETING = r'.*?/div/div/div/div\[[0-9]\]/div/span'
LINK = r'.*?/a(\[[0-9]{1,2}\])?/.*'

PRONUNCIATION = r'/(&#|[a-z}|[A-Z]|[0-9]|;|,|[^a-zA-Z\d\s])+/'

ERROR = [{
    'pos': 'Unexpected Error :(',
    'definition': ('It looks like there was a robot error that we could not '
                   'avert.  Please try again later.'),
    'examples': ['Try changing your environment, IP address, Machine, etc'],
    'synonyms': ['We tried completing the captcha, but it was too advanced '
                 'for us']
}]

GOOGLES = ["google.com", "google.ad", "google.ae", "google.com.af", "google.com.ag", "google.com.ai", "google.al", "google.am", "google.co.ao", "google.com.ar", "google.as", "google.at", "google.com.au", "google.az", "google.ba", "google.com.bd", "google.be", "google.bf", "google.bg", "google.com.bh", "google.bi", "google.bj", "google.com.bn", "google.com.bo", "google.com.br", "google.bs", "google.bt", "google.co.bw", "google.by", "google.com.bz", "google.ca", "google.cd", "google.cf", "google.cg", "google.ch", "google.ci", "google.co.ck", "google.cl", "google.cm", "google.com.co", "google.co.cr", "google.com.cu", "google.cv", "google.com.cy", "google.cz", "google.de", "google.dj", "google.dk", "google.dm", "google.com.do", "google.dz", "google.com.ec", "google.ee", "google.com.eg", "google.es", "google.com.et", "google.fi", "google.com.fj", "google.fm", "google.fr", "google.ga", "google.ge", "google.gg", "google.com.gh", "google.com.gi", "google.gl", "google.gm", "google.gr", "google.com.gt", "google.gy", "google.com.hk", "google.hn", "google.hr", "google.ht", "google.hu", "google.co.id", "google.ie", "google.co.il", "google.im", "google.co.in", "google.iq", "google.is", "google.it", "google.je", "google.com.jm", "google.jo", "google.co.jp", "google.co.ke", "google.com.kh", "google.ki", "google.kg", "google.co.kr", "google.com.kw", "google.kz", "google.la", "google.com.lb", "google.li", "google.lk", "google.co.ls", "google.lt", "google.lu", "google.lv", "google.com.ly", "google.co.ma", "google.md", "google.me", "google.mg", "google.mk", "google.ml", "google.com.mm", "google.mn", "google.ms", "google.com.mt", "google.mu", "google.mv", "google.mw", "google.com.mx", "google.com.my", "google.co.mz", "google.com.na", "google.com.ng", "google.com.ni", "google.ne", "google.nl", "google.no", "google.com.np", "google.nr", "google.nu", "google.co.nz", "google.com.om", "google.com.pa", "google.com.pe", "google.com.pg", "google.com.ph", "google.com.pk", "google.pl", "google.pn", "google.com.pr", "google.ps", "google.pt", "google.com.py", "google.com.qa", "google.ro", "google.ru", "google.rw", "google.com.sa", "google.com.sb", "google.sc", "google.se", "google.com.sg", "google.sh", "google.si", "google.sk", "google.com.sl", "google.sn", "google.so", "google.sm", "google.sr", "google.st", "google.com.sv", "google.td", "google.tg", "google.co.th", "google.com.tj", "google.tl", "google.tm", "google.tn", "google.to", "google.com.tr", "google.tt", "google.com.tw", "google.co.tz", "google.com.ua", "google.co.ug", "google.co.uk", "google.com.uy", "google.co.uz", "google.com.vc", "google.co.ve", "google.vg", "google.co.vi", "google.com.vn", "google.vu", "google.ws", "google.rs", "google.co.za", "google.co.zm", "google.co.zw", "google.cat"]  # NOQA
# Unsupported: "google.cn",
