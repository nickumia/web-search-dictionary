
import wsd


def test_lookup():
    definitions = wsd.lookup('equal')
    print(definitions.getDefinitions())
    assert definitions.getPronounciation() == '/&#712;&#275;kw&#601;l/'
    assert len(definitions.getDefinitions()) == 8
