# Additional Hindi pass criteria for the critique, mirroring the Hindi hook priorities.
# Appended by prompts/critique_prompt.py::build_critique_prompt.

HINDI_CRITIQUE = """

    ADDITIONAL HINDI CRITERIA (a hook FAILS if any is not met):

    18. LENGTH (OVERRIDES criterion 8): 30-60 words, with 5 words of tolerance either side — a hook under 25 or over 65 words FAILS, and anything inside that range passes on length. There is no sentence count in Hindi: do not fail a hook for having more or fewer sentences than another one.

    19. SENTENCES CONNECT: every sentence after the first picks up something the previous one named — through a pronoun (वह, उसने, उन्हें, उसकी), वही / उसी + an already-named noun (उसी रात, वही चिट्ठी), a place already given (वहीं), or a carrying opener (इसके बाद, तभी, और तब, उसी वक्त). FAILS if a sentence restarts by repeating the character's full name where NOTHING WAS AMBIGUOUS, or if a clause changes who it is about with nothing in that clause marking the change (उसे नहीं मालूम कि, जबकि, और उधर). Then check every वह, उसने, उसकी and वही / उसी + noun separately: how many people in the precap could it mean? More than one — FAIL, and say in the reason that the name belongs there. Exactly one — correct, leave it. वह and उसने cover men and women alike, so any precap with two characters in it is where this breaks. A name repeated to keep two characters apart NEVER fails this criterion, however often it repeats; only a name repeated where one person was ever in question does. Sentence LENGTH is not judged here — criterion 18 allows long sentences and this criterion does not take that back; this is about whether the subject stays recoverable by ear.

    20. ONE MOMENT, NOT A FULLER ONE (applies criterion 1d to Hindi's longer budget): the extra words Hindi allows are for clauses that turn a sentence back on itself, not for additional content. FAILS if the hook uses its length to carry a second event, a second location, or a third named person alongside the one coming moment. A hook at 58 words carrying one moment passes; a hook at 58 words carrying three things fails, however well each is written.
    """
