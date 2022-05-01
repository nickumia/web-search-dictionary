[![Tests](https://github.com/nickumia/web-search-dictionary/actions/workflows/commit.yml/badge.svg)](https://github.com/nickumia/web-search-dictionary/actions/workflows/commit.yml)

# web-search-dictionary
A Definition Lookup API based on Google Search Results

## Installation

Currently, the project is not published on PyPI (maybe in the near future).  To install, run the following
```
pip install git+https://github.com/nickumia/web-search-dictionary.git@main#egg=websearchdict
```

## Example Usage

There is an example script, `example.py`.  Simply supply it with a word as a command-line argument and
it will return a list of definitions written to the terminal.
```
python example.py special

# When calling the main lookup function, google_search is the default.  However, either of the two
# options can be explicitly referenced.

import websearchdict
from websearchdict.web.fetch import google_search, wiktionary_search
websearchdict.lookup("<word-to-lookup>", search=<wiktionary_search|google_search>)
```

The main function of this package is `lookup()` which returns the definitions of words.  There are two
under-the-hood mechanisms that may be expanded upon in the future.
1. Lookup Engine: 
    1. Google: Currently, since Google has it's `define [word]` capability built into search bar, it
       was the most logical option to retrieve definitions.  There is an unintended feature that uses the website
       previews from real search results (which enables more definitions to be returned).  Further integrations
       with other search engines can be written in the future.
    1. Wiktionary: Inspired from online searching, wiktionary provides an open online dictionary with a relatively
       easy lookup url.  The parsing methodology is completely different from google; however, this seems like it
       would be the more stable option instead of relying on an intricate search engine.
1. HTML Parser:  For the quickest processing, `lxml` is used as the default HTML Parser.  There are other parsers
   that may provide a different understanding of web results.  Currently, lxml is the only supported parser.

```
# Example Output 1 (Google): special

Part of speech [0]: adjective
Definition [0]: better, greater, or otherwise different from what is usual.
Example [0]: they always made a special effort at Christmas
Part of speech [1]: noun
Definition [1]: a thing, such as an event, product, or broadcast, that is designed or organized for a particular occasion or purpose.
Example [1]: television's election night specials

# Example Output 2 (Google): world

/wərld/ |
Part of speech [0]: noun
Definition [0]: the earth, together with all of its countries, peoples, and natural features.
Example [0]: he was doing his bit to save the world
Synonyms [0]: ['earth', 'globe', 'planet', 'sphere']
Part of speech [1]: noun
Definition [1]: a region or group of countries.
Example [1]: the English-speaking world
Synonyms [1]: None
Part of speech [2]: noun
Definition [2]: human and social interaction.
Example [2]: he has almost completely withdrawn from the world
Synonyms [2]: ['society', 'high society', 'secular interests', 'temporal concerns', 'earthly concerns', 'human existence']

# Example Output 3 (Wiktionary): travel

/ËtÉ¹Ã¦vÉl/ | -Ã¦vÉl | /ËtrÃ¦ËÊÉÉ½/ |
Part of speech [0]: Verb
Definition [0]: ( intransitive )  To be on a  journey , often for pleasure or business and with luggage; to go from one place to another.
Synonyms [0]: None
Part of speech [1]: Verb
Definition [1]: ( intransitive )  To  pass  from one place to another; to move or  transmit
Synonyms [1]: None
Part of speech [2]: Verb
Definition [2]: ( intransitive , &#32; basketball )  To move illegally by walking or running without dribbling the ball.
Synonyms [2]: None
Part of speech [3]: Verb
Definition [3]: ( transitive )  To travel throughout (a place).
Synonyms [3]: None
Part of speech [4]: Verb
Definition [4]: ( transitive )  To force to journey.
Synonyms [4]: None
[truncated for brevity]
```

## Special Considerations

- Search Engine/ISP Rate-limiting:
  - The library makes a new web request to the search engine for every `lookup` call.  It is a non-special, very generic http
  call.  However, be wary making too many calls within a short time period.  The search engine or ISP or other middleman may
  begin to rate-limit or otherwise flag the connection.  
  - This is now a known problem as addressed in https://github.com/nickumia/web-search-dictionary/pull/9.
  - The current workaround is to use selenium to open up a web browser to manually complete a recaptcha.  By doing so 
  (within the context of the application), google allows the program to operate on a temporary lease.  When the problem does
  occur, the recaptcha should only need to be completed once within a 24 hour period (or until google releases the rate-limit
  on the crawler).
  
## Peers

There is a javascript-version of the same idea: https://github.com/meetDeveloper/freeDictionaryAPI
- It is a bit easier to [implement this](https://github.com/meetDeveloper/freeDictionaryAPI/blob/master/modules/dictionary.js#L37-L135) in javascript, since it's much more web-aware (js|html|css)
- This didn't work for me since it would've been a completely separate service architecture to implement.  

## Contributing + Reporting

As shown in the example above, there may be unintended results from the lookup (i.e. "how to pronounce s p e c i a l").
While I can't promise an entirely clean output.  I am striving to make this as useful and dependable as possible.  Feel free
to make new issues and/or submit PRs for bugs or new features.  Looking forward to making this legit!
