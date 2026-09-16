# Unicode script ranges, keyed by script name. Gemini occasionally garbles
# low-resource scripts, splicing a handful of glyphs from another script into
# the middle of a word (e.g. "ఎవరాణ്" instead of "ఆరాణ്" in Malayalam). That
# kind of mid-word corruption is easy to miss in an LLM critique pass but
# trivial to catch with a Unicode range check, so we do it deterministically
# instead of trusting the model to notice its own glitch — for every language
# the pipeline can generate in, not just one.
_SCRIPT_RANGES = {
    "Latin": (0x0041, 0x024F),
    "Devanagari": (0x0900, 0x097F),
    "Bengali": (0x0980, 0x09FF),
    "Gurmukhi": (0x0A00, 0x0A7F),
    "Gujarati": (0x0A80, 0x0AFF),
    "Oriya": (0x0B00, 0x0B7F),
    "Tamil": (0x0B80, 0x0BFF),
    "Telugu": (0x0C00, 0x0C7F),
    "Kannada": (0x0C80, 0x0CFF),
    "Malayalam": (0x0D00, 0x0D7F),
    "Sinhala": (0x0D80, 0x0DFF),
    "Arabic": (0x0600, 0x06FF),  # Urdu
}

# Punctuation that lives inside the Devanagari Unicode block by assignment
# but is shared across most Brahmic scripts (Bengali, Gurmukhi, Oriya, etc.)
# as their own sentence-ending punctuation. Without this, a legitimate danda
# at the end of a Bengali/Punjabi/Odia hook gets misread as "foreign Devanagari".
_SHARED_PUNCTUATION = {
    0x0964,  # । DEVANAGARI DANDA
    0x0965,  # ॥ DEVANAGARI DOUBLE DANDA
}

# Which script each language's own output should be written in. Unmapped
# languages (e.g. "en", or anything not listed here) are skipped rather than
# guessed at — we only flag a language once we know what "foreign" means for it.
_LANGUAGE_SCRIPT = {
    "hi": "Devanagari",
    "mr": "Devanagari",
    "ne": "Devanagari",
    "sa": "Devanagari",
    "bn": "Bengali",
    "as": "Bengali",
    "pa": "Gurmukhi",
    "gu": "Gujarati",
    "or": "Oriya",
    "ta": "Tamil",
    "te": "Telugu",
    "kn": "Kannada",
    "ml": "Malayalam",
    "si": "Sinhala",
    "ur": "Arabic",
    "en": "Latin",
}


def find_foreign_script_chars(text: str, language: str | None) -> list[str]:
    """Return characters found in `text` that belong to a script which has no
    business appearing in `language` output. Latin characters are excluded for
    non-English target languages — those are legitimate for character
    names/nicknames quoted from the source text."""
    own_script = _LANGUAGE_SCRIPT.get((language or "").lower())
    if own_script is None:
        return []

    own_lo, own_hi = _SCRIPT_RANGES[own_script]
    allow_latin = own_script != "Latin"
    latin_lo, latin_hi = _SCRIPT_RANGES["Latin"]

    found = []
    for ch in text:
        code = ord(ch)
        if code in _SHARED_PUNCTUATION:
            continue
        if own_lo <= code <= own_hi:
            continue
        if allow_latin and latin_lo <= code <= latin_hi:
            continue
        for script, (lo, hi) in _SCRIPT_RANGES.items():
            if script == own_script:
                continue
            if lo <= code <= hi:
                found.append(ch)
                break
    return found
