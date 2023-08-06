"""polish -> simplified polish -> english/french transcription"""

import re

# relative vs non relative import bs
try:
    from nums import num_to_speech
except:
    from .nums import num_to_speech

langs = {"en": "en_US", "fr": "fr_FR"}

# ~40 lines of regexp
repolon = {
    r"(\b[wz])(\s)": r"\1",  # lone letters
    "rz": "ż",  # upraszczam polski
    # r"([^pt])ch": r"\1h",  # ph i th nie mogą powstać
    "ó": "u",
    "ęł": "eł",
    "ął": "oł",
    r"([ea])u": r"\1ł",
    r"ci(\b|[^eaouęą])": r"ći\1",  # ć, ś, dź i ź w różnych sytuacjach
    r"ci([^e])": r"ć\1",
    r"ci": r"ć",
    r"si(\b|[^eaouęą])": r"śi\1",
    r"si([^e])": r"ś\1",
    r"si": r"ś",
    r"dzi(\b|[^eaouęą])": r"dźi\1",
    r"dzi([^e])": r"dź\1",
    r"dzi": r"dź",
    r"zi(\b|[^eaouęą])": r"źi\1",
    r"zi([^e])": r"ź\1",
    r"zi": r"ź",
    r"ni(\b|[^eaouęą])": r"ńi\1",  # i ń
    r"ni([^e])": r"ń\1",
    r"ni": r"ń",
    r"([śptkh])ż(\w+)": r"\1sz\2",  # ubezdźwięcznienie
    r"([śptksh])w(\w+)": r"\1f\2",
    r"([śptkh])d(\w+)": r"\1t\2",
    r"([^cs])z([kptf])": r"\1s\2",
    r"w([kptshf])": r"f\1",
    r"ż([kptsfh])": r"sz\1",
    r"ż\b": "sz",
    r"(\S)w\b": r"\1f",
    r"\Bb\b": "p",
    r"\Bg\b": "k",
    r"\Bd\b": "t",
    r"([^cs\s])z\b": r"\1s",
    r"ź\b": "ś",
    r"dź\b": "ć",
    r"dż\b": "cz",
    # "ń": "n",
    # r"ą\b": "om",  # nasals
    r"ę\b": "e",
    r"ę([zscśćtdkgż]|cz|sz)": r"en\1",
    r"ą([zscśćtdgkż]|cz|sz)": r"on\1",
    r"ą([pb])": r"om\1",
    r"ę([pb])": r"em\1",
}


# ~60 lns of regexp. yet another mess that could be avoided with IPA
angl = {
    "ń": "n",
    "ą": "om",  # ą in polish actually still works
    "\be\b": r"\bFF\b",
    r"\B[ji]i": "i",  # ji/ii nie umie rozroznic
    r"([^pt])ch": r"\1h",  # ph i th nie mogą powstać
    "ch": "kh",  # niedobitki ch
    r"([fk])i(e)": r"\1\2",  # bez palatalizacji po nich
    # r'([fk])i(e)': r'\1i\2hh',
    r"\bnie\b": "ne",  # nie i mnie są hardcoded XD
    r"\bmnie\b": "mne",
    r"w": "v",  # ogół spółgłosek
    "ś": "sz",
    "ź": "ż",
    "ć": "cz",
    "dź": "dż",
    r"s([^z]|\b)": r"ss\1",
    r"([^cs]|\b)z": r"\1s",
    r"(\b)cz": r"\1ch",  # szeleszczące
    "cz": "tch",
    "sz": "sh",
    "dż": "J",
    r"([^bvzg]|\b)ż": r"\1zsh",
    "ż": "sh",
    r"c([^h]|\b)": r"ts\1",
    # 'a' 'i' 'e' samotne
    r"a([^jłr]|\b)": r"ah\1",
    r"([^ji])e([^j]|\b)": r"\1eh\2",
    r"eh\b": "ehh",
    r"\bi\b": r"e",
    # ogół samogłosek
    r"y": "I",  # igrek na razie pod placeholderem takim
    r"(\w{2,})iej": r"\1 yay",
    r"(\w{2,})[ij]e": r"\1 yeah",  # końcówka -ie zależnie od sylabowości
    r"\bje(\w+)([eioua])": r"yeah \1\2",
    r"(\w+)je(\w+)": r"\1yeh\2",
    r"(\w{1})ie": r"\1ieh",
    r"i([^eao]|\b)": r"EE\1",  # EE by ominąć zmiany na małych e
    r"ej\b": "ei",  # dyftongi
    r"ej\B": "ay",
    r"EE": "ee",  # i powrót ee
    r"I": "ih",  # igrek wraca
    r"ał": "ow",
    r"([aeoi])(\w+)oł": r"\1\2 oh",
    "oł": "ow",
    "ł": "w",
    r"(\b\w{1})aj": r"\1ie ",
    r"(\w{1,})(\w{1})aj(\w+)": r"\1\2igh \3",
    r"(\w+)(\w{1})aj": r"\1 \2ie",
    r"aj": " i",
    r"a\b": "ah",  # wstawiam a tam gdzie się mogło zgubić przy rozdzielaniu na np 'yeah'
    "j": "y",
    r"J": "dj",
    r"o([^whym]|\b)": r"aw\1",
    r"uw\b": "ooo",
    r"u([^w]|\b)": r"oo\1",
    r"u(w\w+)": r"oo \1",
    r"g([ei])": r"gh\1",  # g != dż
    r"\bb\b": "bhehh",
    r"\bts\b": "tsehh",  # letters when not in words ie. their names
    r"\bd\b": "dehh",  # eg. y == igrek
    r"\bFF\b": "ehh",
    r"\bf\b": "ehf",
    r"\bg\b": "ghiehh",
    r"\bh\b": "hah",
    r"\by\b": "yacht",
    r"\bk\b": "kah",
    r"\bp\b": "pehh",
    r"\bq\b": "coo",
    r"\br\b": "ehr",
    r"\bss\b": "ess",
    r"\bt\b": "tehh",
    r"\bv\b": "voo",
    r"\bx\b": "eeks",
    r"\bih\b": "eegrehk",
    r"\bs\b": "seht",
}


franc = {
    "ch": "r",
    "w": "v",
    r"e\b": "é",
    r"n\b": "ne",
    r"m\b": "mE",
    r"ą": "on",
    r"(sz|ś)": r"ch",
    r"(.*)ché\b": r"\1chaI",
    "j": "J",
    r"ż|ź": "j",
    r"(ć|cz)": r"tch",
    "u": "ou",
    "y": "Eu",
    "J": "y",
    "s": "ss",
    "z": "s",
    r"c([^h])": r"ts\1",
    r"c\b": "tsE",
    r"(g)([ei])": r"\1u\2",
    "łou": "wou",
    r"ł([^u])": r"ou\1",
    r"([^u])ł": r"\1ou",
    r"(a|o)(i|y)": r"\1ï",
    "I": "i",
    r"en(\B)": r"ain\1",
    "en": "aine",
    r"e([^nm]+[ouie])": r"é\1",
    r"e([^u])": r"è\1",
    r"E": "e",
    r"([tklph])\b": r"\1e",
    r"([^cp])kh": "h",
    "ń": "gn",
}


def repolonizuj(s: str) -> str:
    """
    changes given text in standard polish ortography into a simplified
    phonetic version inspired by futuryści
    """
    subbed = s
    for key in repolon:
        subbed = re.sub(re.compile(key), repolon[key], subbed)
    return subbed


def anglicyzuj(s: str) -> str:
    "anglicises simplified polish text"
    subbed = []
    for w in s.split():
        sub = w
        if re.match(r"(-|)\d+", w):
            sub = num_to_speech(int(re.match(r"(-|)\d+", w).group(0))) + "".join(
                re.findall(r"\D+", w)
            )
        elif re.match(r"(\w+[^\d-])((-|)\d+)", w):
            # eg "kot18"
            sub = (
                anglicyzuj(re.match(r"(\w+[^\d-])((-|)\d+)", w).group(1))
                + " "
                + num_to_speech(int((re.match(r"(\w+[^\d-])((-|)\d+)", w).group(2))))
            )
        elif re.match(r"(.)(\d+)", w):  # this needs to be improved
            # eg "'-7" should be dealt with as well
            sub = num_to_speech(
                int((re.match(r"(.)(\d+)", w).group(2)))
            )  # + ''.join(re.findall(r'\D+', w))
        else:
            for key in angl:
                sub = re.sub(re.compile(key), angl[key], sub)
        subbed.append(sub)
    return " ".join(subbed)


def francyzuj(s: str) -> str:
    "francises simplified polish text"
    subbed = []
    for w in s.split():
        sub = w
        if re.match(r"(-|)\d+", w):
            pass
        elif re.match(r"(\w+[^\d-])((-|)\d+)", w):
            pass
        elif re.match(r"(.)(\d+)", w):  # this needs to be improved
            pass
        else:
            for key in franc:
                sub = re.sub(re.compile(key), franc[key], sub)
        subbed.append(sub)
    return " ".join(subbed)


def tłumacz(s: str, lang="en") -> str:
    """
    returns given polish text transcribed into english.
    can also be called with tlumacz(s).
    Specify the output language with `lang`
    """
    if lang not in langs:
        raise NotImplementedError(
            "Language '%s' not found among avalaible languages, which are:" % lang,
            list(langs.keys())
        )

    s = repolonizuj(s)
    return {"en": anglicyzuj, "fr": francyzuj}[lang](s)
