# Additional Hindi pass criteria for the critique, mirroring the Hindi hook priorities.
# Appended by prompts/critique_prompt.py::build_critique_prompt.

HINDI_CRITIQUE = """

    ADDITIONAL HINDI CRITERIA (a hook FAILS if any is not met):

    18. LENGTH (OVERRIDES criterion 8): 30-60 words, with 5 words of tolerance either side — a hook under 25 or over 65 words FAILS, and anything inside that range passes on length. There is no sentence count in Hindi: do not fail a hook for having more or fewer sentences than another one.

    19. SENTENCES CONNECT: every sentence after the first picks up something the previous one named — through a pronoun (वह, उसने, उन्हें, उसकी), वही / उसी + an already-named noun (उसी रात, वही चिट्ठी), a place already given (वहीं), or a carrying opener (इसके बाद, तभी, और तब, उसी वक्त). FAILS if a sentence restarts by repeating the character's full name where NOTHING WAS AMBIGUOUS, or if a clause changes who it is about with nothing in that clause marking the change (उसे नहीं मालूम कि, जबकि, और उधर). Then check every वह, उसने, उसकी and वही / उसी + noun separately: how many people in the precap could it mean? More than one — FAIL, and say in the reason that the name belongs there. Exactly one — correct, leave it. वह and उसने cover men and women alike, so any precap with two characters in it is where this breaks. A name repeated to keep two characters apart NEVER fails this criterion, however often it repeats; only a name repeated where one person was ever in question does. Sentence LENGTH is not judged here — criterion 18 allows long sentences and this criterion does not take that back; this is about whether the subject stays recoverable on a single read.

    20. ONE MOMENT, NOT A FULLER ONE (applies criterion 1d to Hindi's longer budget): a simple, plain sentence is the default and never fails for being simple. The extra length Hindi's range allows, when a sentence does use it, is for a clause that turns the sentence back on itself, not for additional content. FAILS if the hook uses its length to carry a second event, a second location, or a third named person alongside the one coming moment. A hook at 58 words carrying one moment passes; a hook at 58 words carrying three things fails, however well each is written.

    21. PAST-TENSE COMING MOMENT (OVERRIDES criterion 12 for Hindi): the coming moment is narrated mostly in the past tense, as a scene already caught in the act (ले लिया, टकरा गए, चूम लिया) — simple present (करता है, कहता है) is also acceptable, used less often. FAILS if it uses the forward tense instead (होगा, होने वाला है, करेगा, लगने वाली है, क्या होगा, जाएगा), including in a closing question — "क्या वह मान जाएगी?" fails, "आखिर उसने क्या चुना?" does not.

    22. GROUND SENTENCE BEFORE THE TURN (reinforces T2 for Hindi): the hook opens on one complete sentence naming a concrete fact from the chapter just read, in the past, before it turns to the coming moment. FAILS if the coming moment is narrated with no such ground sentence first, or if that opening sentence is vague scene-setting rather than a concrete fact a reader can place.

    23. DIALOGUE EXCEPTION (OVERRIDES criterion 10 for Hindi): a single short quoted line from the target scene, used as a device, does NOT fail criterion 10. FAILS only if more than one line is quoted, or if the quoted line itself states the outcome.
    """
