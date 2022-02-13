
import wsd


def test_lookup():
    definitions = wsd.lookup('equal')
    assert definitions.getPronounciation() == '/&#712;&#275;kw&#601;l/'
    assert len(definitions.getDefinitions()) == 10
