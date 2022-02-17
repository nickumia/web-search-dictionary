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
```

The main function of this package is `lookup()` which returns the definitions of words.  There are two
under-the-hood mechanisms that may be expanded upon in the future.
1. Search Engine: Currently, since Google has it's `define [word]` capability built into search bar, it
   was the most logical option to retrieve definitions.  There is an unintended feature that uses the website
   previews from real search results (which enables more definitions to be returned).  Further integrations
   with other search engines can be written in the future.
1. HTML Parser:  For the quickest processing, `lxml` is used as the default HTML Parser.  There are other parsers
   that may provide a different understanding of web results.  Currently, lxml is the only supported parser.

```
# Example Output 1:

Part of speech [0]: adjective
Definition [0]: better, greater, or otherwise different from what is usual.
Example [0]: they always made a special effort at Christmas
Part of speech [1]: noun
Definition [1]: a thing, such as an event, product, or broadcast, that is designed or organized for a particular occasion or purpose.
Example [1]: television's election night specials

# Example Output 2:

/wərld/ |
Part of speech [0]: noun
Definition [0]: the earth, together with all of its countries, peoples, and natural features.
Example [0]: he was doing his bit to save the world
Synonyms [0]: ['synonyms: earth', 'globe', 'planet', 'sphere']
Part of speech [1]: noun
Definition [1]: a region or group of countries.
Example [1]: the English-speaking world
Synonyms [1]: None
Part of speech [2]: noun
Definition [2]: human and social interaction.
Example [2]: he has almost completely withdrawn from the world
Synonyms [2]: ['synonyms: society', 'high society', 'secular interests', 'temporal concerns', 'earthly concerns', 'human existence']
```

## Special Considerations

- The library makes a new web request to the search engine for every `lookup` call.  It is a non-special, very generic http
  call.  However, be wary making too many calls within a short time period.  The search engine or ISP or other middleman may
  begin to rate-limit or otherwise flag the connection.  This is not a known problem (hoewver, I will update if more details
  surface).
  
## Peers

There is a javascript-version of the same idea: https://github.com/meetDeveloper/freeDictionaryAPI
- It is a bit easier to [implement this](https://github.com/meetDeveloper/freeDictionaryAPI/blob/master/modules/dictionary.js#L37-L135) in javascript, since it's much more web-aware (js|html|css)
- This didn't work for me since it would've been a completely separate service architecture to implement.  

## Contributing + Reporting

As shown in the example above, there may be unintended results from the lookup (i.e. "how to pronounce s p e c i a l").
While I can't promise an entirely clean output.  I am striving to make this as useful and dependable as possible.  Feel free
to make new issues and/or submit PRs for bugs or new features.  Looking forward to making this legit!
