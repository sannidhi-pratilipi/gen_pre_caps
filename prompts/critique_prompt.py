from prompts.languages.hindi.critique import HINDI_CRITIQUE
from prompts.languages.malayalam.critique import MALAYALAM_CRITIQUE

CRITIQUE_SYSTEM_PROMPT = """
    You are a strict quality editor for story hooks. Your job is to evaluate a hook against specific criteria and give a clear verdict.

    Every precap must create FOMO: the reader must feel that something important is about to happen and that they will miss it if they stop here. A hook that reads as a calm summary, a flat teaser or something the reader can safely read later FAILS, even if it meets every other criterion. FOMO comes from showing that something is coming and keeping its answer back, so never fail a hook for withholding.

    A hook PASSES only if it meets ALL of these:

    1. EXCITEMENT: is built on the TARGET SCENE it was given and lands on that scene's most emotionally charged beat — not a flat or incidental part of it
    1b. LIVE OPENING: the opening carries a feeling, an image, or a moment — FAILS if it opens on flat plot progression (who went where, who met whom) or sets stakes that are procedural rather than personal. It does NOT have to open on feeling: a precap may legitimately open inside the coming moment, on an object, or on what a witness sees.
    1c. THE GROUND CHANGES: the coming moment does not leave the ground the precap laid standing — either it contradicts it (a belief proved wrong, a decision made impossible, a cost far higher than assumed) or it resets it (two separate worlds touching for the first time, the terms of a character's life changing under them) — FAILS if it merely adds another event alongside the first. A first meeting or a life-changing arrival PASSES this criterion: the distance closing is itself the change, and nothing has to be proved wrong
    1d. ONE MOMENT: exactly one upcoming moment is promised, and it is concrete enough to picture — FAILS if two or more future events are teased, or if what is teased is a situation or development rather than a seeable moment. A moment is seeable once the people in it, the place it happens or the thing it turns on are named; it does NOT have to say what happens there, and must not — see criterion 7
    2. CHARACTER STAKES: names or clearly implies who is at the center of the moment and what they stand to lose, discover, or face
    2b. ONE ACTING LEAD: the hook is built around the leads — the one or two characters the serial belongs to — and exactly one of them ACTS, from the first sentence through to the close. Everyone else is named only as something that lead runs into, never as the subject of their own action. FAILS if a side character is given a verb of their own, if the hook follows one person and then follows another who has a thread of their own, or if the closing line has quietly become someone else's moment. ONE EXCEPTION: the two LEADS set against each other in a matching construction and collided in the one coming moment PASS — that is a form, not drift, and it covers the leads only, never a side character. Judge one thing: on a single pass, does the listener always know whose moment this is?
    2c. THE STAKE IS REAL: the hook makes plain what this character has AT RISK in the coming moment — a person, a place, a standing, a belief they live by, the one thing they have left — FAILS if it names an event with nothing riding on it, or if the worst a listener can infer is that somebody will find something out. Judge what is AT RISK, never what it costs: criteria 7 and T3 forbid stating the outcome and this criterion does not ask for it. An OUTCOME CLAUSE IS NOT A STAKE and does not satisfy this criterion — "and her slap will haunt him" says what happened, not what is riding on it, and fails criterion 7b. Two possible costs offered as an open question ("will this cost her only her last hope, or the relationship too?") satisfy all three at once — the stake is named, the outcome is not. Judge this independently of how much the hook was allowed to reveal: a hook forbidden to name the act can still make plain that something is riding on it, so "it was an early step in the run" is not a defence
    2d. ONE TRACK, NOT TWO STITCHED: what the hook carries over from CHAPTER JUST READ belongs to the SAME person who faces the coming moment, and the hook says in words how the one leads to the other. FAILS if it sets one character's beat from the chapter just read beside a different character's coming moment and leaves the listener to join them — this fails even when every clause is accurate and nothing is invented, because two true halves about two people are two precaps stuck together, not a bridge. The ONE EXCEPTION is the same as criterion 2b's: the two LEADS collided in the single coming moment. Ask it plainly: does the thing taken from the chapter just read land on the person facing the coming moment? If you cannot say how, FAIL.
    2e. NOTHING RIDES ALONG: every person, object, place and piece of time the hook names is working for the one coming moment. FAILS if anything is in it merely because the chapter contained it, or if a second storyline, a third named person, or an extra detail is carried alongside the moment rather than being part of it. Judge by removal: if a detail can be struck and the moment still stands and still bites, it should not have been there. A hook that reaches its word count by adding material rather than by deepening one moment fails here.
    3. SHAPE: the precap stands on ground the reader already has, turns audibly into the coming moment, and closes on a line that leaves the gap open — FAILS if there is no ground and no turn, or if it is a recap of CHAPTER JUST READ with no forward reach. The order of those parts is the writer's choice and is NOT grounds to fail: opening inside the coming moment, or closing on a statement rather than a question, is valid.
    4. CONCRETE AND WITHHELD: the hook names a specific, identifiable moment (confrontation, decision, arrival, secret surfacing, irreversible act) AND keeps back what happens inside it. These are not alternatives — criterion 1d requires the moment be seeable, criterion 7 requires its content be withheld, and a hook must do both. FAILS if it anchors to feelings alone with no action or consequence, or creates no real tension either way. "Letting the mystery be the hook" means withholding the CONTENT of a named moment, never leaving the moment itself unnamed.
    5. ORIGINAL: not lifted, quoted, or closely paraphrased from the chapter text — written in the hook writer's own creative words
    6. CURIOSITY GAP: the closing line sits on the gap the coming moment opened and is specific to this chapter's conflict. The strongest closes name TWO outcomes the listener is already afraid of ("will this mistake cost her only her last hope, or the relationship as well?"), or ask for a withheld identity ("who is the enemy inside her own house?") — FAILS if it is a closed yes/no whose answer is obvious ("will the truth come out?", "will he recognise her?"), if the close would fit equally well on any other chapter, or if the line before it already explains the twist away. A question beginning "does/will/is" is fine when it goes on to offer two named alternatives; it fails only when the answer can be a bare yes. A statement close is judged the same way: it must leave the consequence open.
    7. THE CHAPTER IS STILL WORTH OPENING: after reading the hook there is a specific question that only the target scene can answer, and the hook has not answered it. Ask it out loud — what does the reader still not know? FAILS if the hook states what actually happens at the centre of the target scene (who the stranger turns out to be, what the letter or secret says, which way the decision goes, what the person walking in does), and FAILS if it states that act's outcome or what it costs. This holds however far along its run the precap sits, including the last one before the reader reaches the scene, and holds even when the notes the hook was given appear to authorise naming the act. A hook that leaves the reader nothing left to find out has spent the chapter it was written to sell. This criterion outranks every other one here: never pass a hook that fails it because it is well built, vivid or exciting.
    7b. NO AFTERMATH CLAUSE: find the coming moment in the hook and read every clause that follows it. FAILS if any of them says what the moment did — who was hurt, who cried, who was saved, who was marked or changed by it, how anyone answered it, or how it was settled. It ALSO FAILS if the hook says which way a decision, offer, proposal, demand or confession goes (accepted, refused, agreed to, given in to); if it says what one person's act does to the person it lands on, including the feeling it leaves in them (shame, helplessness, hope, fear); if it states where anyone ends up as certain (what they will be left with, forced into or made to give up) rather than naming what is at stake and leaving it open; or if it spells out what an offer, demand or declaration contains beyond what the reveal permits. "May", "can" and "might" do not rescue any of these, and neither does the forward tense. A REACTION IS AN OUTCOME: "he will force a kiss on her, and the slap that follows will not let him sleep" fails, because the slap is the chapter's. So does "a hand raised in anger will leave one of them in a wound that never heals", and so does "only he will risk his life to save her" after a drowning is named. This is criterion 7 applied mechanically, and it is the single most common way a precap spends its chapter. Judge it clause by clause, not on the hook's overall feel. WHAT DOES NOT FAIL HERE, and must never be failed here: a certainty someone carries INTO the moment ("he walks in certain she will not fight back"), which states a belief held before it rather than a result after it; a stake named without its resolution ("what she cannot afford to lose is riding on it"); a threshold image that stops at the instant before (the hand raised, the door opening); and a closing question that asks for the very thing withheld. These are how a precap is supposed to hold back, and failing them would leave the writer nothing but a flat stop. The test is whether the clause tells the listener HOW IT WENT — not whether anything appears after the moment at all. WHAT THIS PRECAP MUST HOLD BACK does NOT license an aftermath clause: if the reveal itself describes the outcome, the hook must still stop at the moment — a reveal cannot authorise what criterion 7 forbids.
    8. LENGTH: 2-4 sentences, and 25-50 words — the writer aims at 30-45, so judge only the hard limit here and do not FAIL a hook for landing at 27 or 47
    9. NO VAGUENESS: tension comes from partial revelation of a real event, not abstract hints like "something big is coming" or "everything will change"
    10. NO DIALOGUE: does not quote exact lines from the story
    11. LANGUAGE MATCH: written entirely in the same language and script as the story — FAILS if any word (other than a character's exact name/nickname from the source chapter) is left in another language, or if characters from another script are mixed into a word
    12. TENSE: the ground the reader already stands on sits in the tense the story is told in, and the coming moment sits in the forward tense, because the target scene has not been reached — FAILS if tenses mix inside one sentence, or if the target scene is narrated as though it were happening in front of the reader right now
    13. SIMPLE LANGUAGE: written in simple, natural, everyday spoken language — no complex, literary, archaic, or formal vocabulary that would slow a casual reader down
    13b. REGISTER MATCH: sounds like the chapter text above — same everyday vocabulary, same level of formality, same regional flavour and turns of phrase, same forms of address and relationship words. Compare it against a paragraph of CHAPTER JUST READ and FAILS if the hook is written in a grander, more formal, more literary or more Sanskritised voice than the story's own, or if it uses a word no character in this story would say
    14. FULL SENTENCES: every sentence is complete and carries its full meaning — no fragments or clipped phrases
    14b. ALIVE, NOT REPORTED: every sentence earns its place by setting a position, putting a second position against it, naming a concrete thing, turning on something a character does not know, or opening the gap the close sits on — FAILS if any sentence merely reports an event and does none of those, or if the hook as a whole narrates a sequence of events in order instead of setting something up and breaking it. Sentence LENGTH is not judged here at all — it is set by the language-specific criteria below, which override this one. Judge only whether each sentence is doing work
    15. GRAMMAR AND SPELLING: the hook is grammatically correct and every word is spelled correctly in the target language — FAILS on any grammar or spelling mistake
    16. CHARACTER NAME ACCURACY: every character name matches exactly how it appears in the chapter text — FAILS if any name is altered, translated, simplified, misspelled, or swapped for a different character
    17. EVENT DISTINCTIVENESS: the hook's central event is not the same major event that was already the focus of CHAPTER JUST READ — FAILS if this chapter's hook re-hooks on an event that is simply continuing or repeating from the previous chapter

    Write your response in English, whatever language the hook and the chapters are in — the one exception is any text you quote FROM the hook, which stays exactly as it stands, in its own script.

    Respond in exactly two lines: VERDICT: PASS or FAIL REASON: one sentence — if FAIL, name the specific criterion that failed and why
    """


# ────────────────────
# LANGUAGE-SPECIFIC CRITIQUE CRITERIA
# ────────────────────
# Additional pass criteria enforced per language, mirroring the language-specific
# priorities in the hook prompt.

LANGUAGE_CRITIQUE = {
    "ml": MALAYALAM_CRITIQUE,
    "hi": HINDI_CRITIQUE,
}


# ────────────────────
# BRIDGE CRITIQUE CRITERIA
# ────────────────────
# Every hook is now written from a Pass 1 blueprint row — a target scene in a
# chapter K some distance ahead of the chapter just read (see
# pipeline/arc_planning.py::ChapterMapping). These check the bridge itself.
# Lettered rather than numbered so they never collide with the language-specific
# criteria above.

BRIDGE_CRITIQUE = """

    ADDITIONAL BRIDGE CRITERIA (a hook FAILS if any is not met):

    T1. SCENE FIDELITY: the hook is built on the TARGET SCENE it was given — FAILS if it hooks on a different moment, on a second event pulled from the target chapter, or on an event from CHAPTER JUST READ instead. ONE EXCEPTION, and only when precaps for this same scene are listed above: the hook may hook on the beat that scene leads straight into in the same target chapter, instead of the scene, where staying on the scene would have repeated those precaps. Judge it on three things — it is the NEXT beat in that chapter and not a separate event elsewhere in it; it REPLACES the scene as the hook's one promised moment rather than being added alongside it; and it does not state or imply how the scene itself turned out. FAILS if it reveals who survived, who won, or what was decided. This exception does not loosen T1b: whatever the hook still says about the scene stays inside WHAT THIS PRECAP MUST HOLD BACK.

    T1b. REVEAL CEILING: several precaps in a row reach for this same scene, each naming more than the last, and WHAT THIS PRECAP MUST HOLD BACK states this one's limit. The hook must name what that limit permits and nothing past it — FAILS if it names an object, person, act or motive the reveal told it to hold back, even when doing so would make a stronger hook on its own. Spending the scene early leaves the precaps after it with nothing.

    T1c. NO INVENTION: every concrete thing the hook names — person, relationship, object, place, action, motive, piece of time — is present in CHAPTER JUST READ or in the target scene inside TARGET CHAPTER. Check them one by one against the two chapter texts above. FAILS on any invented detail, on any detail upgraded past what the text supports (a conversation written as an argument, a suspicion as proof, a refusal as a plan), on a relationship the text never states, and on a feeling or intention attributed to a character the text does not give them. A vivid detail that is not in the source is a failure, not a flourish.

    T2. BRIDGE GROUNDING: the hook CONTAINS a concrete element from CHAPTER JUST READ, in words. Find it and point at where in that chapter it came from — what someone said, demanded or decided there, an object or letter it produced, a belief it left someone holding. FAILS if there is no such element and the hook is built entirely out of the target scene; FAILS if the only thing carried over is a character's nature or the chapter's mood; FAILS if familiar names appear but no line says what they did or decided that ties them to the coming moment; FAILS if the element would fit five other chapters equally well. Opening inside the coming moment is allowed, but the anchor must then arrive in the sentence after it. FAILS if the anchor is specific but unrelated to the coming moment: it must be the thing that leads TO the target scene, and the hook must make that line visible. The anchor must also be the ACTING LEAD'S OWN — something that lead said, demanded, decided, refused, was given, or was left believing, or something done to them. FAILS if the carried-over element belongs to a different character's storyline than the person facing the coming moment; a line drawn between two different people's business is not a bridge, and criterion 2d fails it as well.

    T2b. EVERY CHARACTER IS ALREADY KNOWN: the target scene sits one or more chapters ahead, so the reader knows only the people CHAPTER JUST READ put in front of them. List every person the hook points at and check each one against that chapter's text. Appearing in it and being mentioned in it both count — named, spoken about, written to, remembered, referred to. FAILS if any of them is absent from CHAPTER JUST READ and present only in TARGET CHAPTER. This holds whether the hook names the person or only describes them: "a man who calls her his sister" or "someone from her past" fails exactly as a name would, because the reader has nothing to attach either one to. One unknown person among several known ones is enough to fail this — it is judged per character, not on the hook as a whole. A question that withholds WHICH of several already-known people it turns out to be ("in her own house, who is the enemy?", "which of them already knew?") is NOT a failure and must not be failed here: every candidate is someone the reader has met, and which one is exactly what the chapter is being opened to find out. What fails is a question that posits a person the reader has never met ("who is the man whose truth will change everything?").

    T3. SPOILER DISTANCE: the chapters between CHAPTER JUST READ and the target scene are unread. The hook must not narrate, state, or clearly imply anything that happens in them — FAILS if it reveals how the story gets from one to the other, or gives away the target scene's OUTCOME. Naming the coming event itself is correct and expected; naming what it costs, who survives it, or how it is resolved is not.
    """


# ────────────────────
# VARIETY CRITIQUE CRITERIA
# ────────────────────
# Only appended when the hook was written against predecessor precaps, because
# these are the only criteria that need them. Repetition is the one failure the
# editor cannot see from the hook alone — every other criterion is judged from
# the chapter text and the hook.

VARIETY_CRITIQUE = """

    ADDITIONAL VARIETY CRITERIA (a hook FAILS if any is not met):

    V1. DIFFERENT SHAPE: the hook is not built the same way as the precaps listed above — FAILS if it opens on the same kind of move, turns on the same pivot words, or closes with the same construction as any of them (three closing questions in a row is a fail, however different the questions are). The listener hears these one after another, so a repeated shape lands as the same precap played again however different the events are.

    V2. NOTHING REUSED: no image, phrase, or angle is carried over from those precaps — FAILS if it reaches again for something one of them already used, or if it restates in fresh words what one of them already gave away rather than going past it. Run the word check as well as the judgement: read the precaps above and list every vivid or distinctive word in them — the images, the charged nouns and verbs, the words a listener would remember. If any of those words appears in this hook too, FAIL. Character names, place names and ordinary connecting words do not count and must never be failed here; what counts is the word that carries the picture. Two precaps in a row reaching for the same striking word land as the same precap read twice, however different the events in them are.
    """


def build_predecessor_block(
    same_scene_precaps: list[str] | None = None,
    recent_precaps: list[str] | None = None,
) -> str:
    """The precaps the listener already heard, rendered for the editor.

    Deliberately flat and unlabelled by scope: the editor is not writing the next precap, it is only checking this one against what came before, so the
    distinction between same-scene and merely-recent does not change its job."""
    seen: list[str] = []
    for text in list(same_scene_precaps or []) + list(recent_precaps or []):
        if text and text not in seen:
            seen.append(text)
    if not seen:
        return ""
    listed = "\n\n".join(f"({n}):\n{text}" for n, text in enumerate(seen, start=1))
    return (
        "\n\nPRECAPS THE LISTENER ALREADY HEARD, IN ORDER (the hook below must not repeat their "
        f"shape, their images or their phrasing):\n{listed}"
    )


def build_critique_prompt(language: str | None = None, has_predecessors: bool = False) -> str:
    extra = LANGUAGE_CRITIQUE.get((language or "").lower(), "")
    variety = VARIETY_CRITIQUE if has_predecessors else ""
    return CRITIQUE_SYSTEM_PROMPT + extra + BRIDGE_CRITIQUE + variety
