# Romance-specific blocks for the Pass 1 blueprint prompt, dropped into the
# placeholders in prompts/arc_prompt.py::PRECAP_BLUEPRINT_SYSTEM_PROMPT by
# build_blueprint_prompt: peak types, dominant emotions and the ranking note.

ROMANCE_EVENT_TYPES = """       
       • COMING-TOGETHER: the leads are just about to come together — an almost-kiss, a confession on the tip of the tongue, one reaching for the other, being put into the same room or the same bed
       • GOING-APART: they are just about to go apart — a walkout, a misunderstanding about to harden, an ultimatum, a third party stepping between them, one deciding to leave
       • DANGER: danger reaching one of them with the other right there — a threat arriving between them, a secret breaking open in front of the other, one of them stepping into the harm closing on the other. A lead facing a threat alone is not the peak; the moment the other reaches them is
       • REALISATION: one of them realises love, affection, or a bond with the other standing right in front of them — a quiet but permanent internal shift, caught in a look held too long or a reaction they cannot explain. A lead alone with their thoughts is not the peak
       • INTIMACY & CLOSENESS: the leads are about to share a moment of real closeness — a touch that lingers, a held gaze, a shared silence, one caring for the other, a guard coming down, a private moment neither planned. The peak is the closeness itself, even when no kiss, confession or clash is in it
       • LIFE-UPENDED: their lives are about to change completely or stop being normal — a marriage, a contract, a move, a pregnancy, a family decision, a truth that can't be taken back
       These names are a prompt, not a boundary. Anything that closes the distance between the leads, threatens to widen it, puts either of them in danger, shifts what one of them feels, or resets the terms of their life together is a peak worth taking even if it fits none of them. A romance serial's peaks are almost always about what is happening BETWEEN the two leads, even in a chapter with no villain and no plot event at all — a long silence, a held glance, or a chance not taken is still a peak if it moves the distance between them.
       BOTH LEADS ARE IN THE PEAK, IN THE SAME PLACE AT THE SAME TIME. The peak is what passes BETWEEN them — what one does to, says to, or does in front of the other. DO NOT pick a moment one lead has on their own, however much it is about the other: thinking of them, deciding about them, weeping over them, finding out about them, or acting on them somewhere they are not.
       DO NOT build a scene_description out of two moments at once, one lead in each — "she says it in the classroom while he watches a video at his flat" is two scenes, not a peak, and a precap aimed at it splits the reader between two people. If the chapter's strongest material is one lead alone, take the moment the two of them are actually in a room together instead, even when it is quieter.
       DO NOT pick a peak that is one lead's own scene with a side character, even when it is driven entirely by feelings about the other lead. A third party may cause the danger, the secret or the obstacle, but the peak itself must be the moment it reaches a lead with the other lead there to see it."""

ROMANCE_EMOTION_LABELS = [
    "LOVE",
    "LONGING",
    "DESIRE",
    "INTIMACY",
    "JEALOUSY",
    "TENDERNESS",
    "HEARTBREAK",
    "TRUST",
    "VULNERABILITY",
    "PROTECTIVENESS",
    "POSSESSIVENESS",
]

# The emotion names the blueprint prompt's own examples use, in romance terms, so the
# romance prompt never mentions a label that is not in ROMANCE_EMOTION_LABELS.
ROMANCE_EMOTION_EXAMPLES = {
    "repeat": "LONGING, LONGING, LONGING",
    "run": "VULNERABILITY (what it will cost her), then TRUST (who is really behind it), then HEARTBREAK (what she loses when it lands)",
    "tags": ["VULNERABILITY", "LONGING", "TRUST", "JEALOUSY", "TRUST"],
}

ROMANCE_EMOTIONS = "  ".join(ROMANCE_EMOTION_LABELS) + """
       Every one of these is a feeling about the two leads and what is between them. Choose only from this list. Do not use FEAR, REVENGE, BETRAYAL, MYSTERY, SHAME, PRIDE or any other label that is not about love, even when the scene is a danger or a secret: promise the love feeling that scene puts at risk (a danger scene is PROTECTIVENESS or HEARTBREAK, a secret is TRUST, a rival is JEALOUSY)."""

ROMANCE_RANKING_NOTE = """
       INTIMACY AND CLOSENESS RANK HIGHEST. If any chapter you were given holds an intimacy or closeness scene between the leads (a touch, a kiss, a shared bed or room, a guard coming down, a private moment between them), that scene is one of your top-ranked peaks and an anchor MUST land on it, however far out it sits.
       DO NOT rank any plot event above an intimacy scene because the plot event is bigger, louder or more dramatic.
       DO NOT skip an intimacy scene because the chapters before it hold strong events. No matter how good the events in between are, the intimacy scene wins.
       When an intimacy scene and another strong peak both sit among the chapters you were given, anchor on the intimacy scene.
       When several intimacy scenes are available, rank all of them above every non-intimacy peak."""

# ────────────────────
# ROMANCE OPENING RUN
# ────────────────────
# Dropped into {opening_run_note} in PRECAP_BLUEPRINT_SYSTEM_PROMPT, right
# after rule 1 (TARGET RANGE). Only the very first run of the story gets
# this emphasis — every later run follows the ordinary rules without needing
# a reminder, because by then the model has already anchored once.

ROMANCE_OPENING_RUN_NOTE = """
       ROMANCE OPENING RUN: search ALL given chapters for the leads' first or peak intimate or closeness moment and anchor chapter 1 on it, however far out it is — there is no cap on how long this run may be. Hold every chapter up to it on that same anchor — sticky anchor still applies — until the reader reaches it.
       If that moment is an INTIMACY & CLOSENESS peak, the intimacy run rules apply: one beat per rung. Each rung's bridge_reasoning should stand on whatever is freshest in its own chapter N, not one fact repeated down the whole run.
"""

# ────────────────────
# ROMANCE BEAT-LADDER ACT CLAUSE
# ────────────────────
# Dropped into {beat_ladder_act_clause} inside rule 8b. Every other peak type
# spends only the beats BEFORE the act; an INTIMACY & CLOSENESS peak is the one
# whose beats ARE the act, so 8b has to say what those runs do instead of only
# naming them as an exception. The step-by-step procedure is in
# ROMANCE_INTIMACY_RUN_NOTE below, which rule 8b's exception points at.

ROMANCE_BEAT_LADDER_ACT_CLAUSE = """For every peak except an INTIMACY & CLOSENESS one, only the beats BEFORE the act are yours to spend; the act and everything after it stay with the chapter, the last rung included.
       AN INTIMACY & CLOSENESS PEAK IS BROKEN FINER, NEVER SPENT: the closeness itself splits into beats, and each rung spends exactly ONE of them and stops there. EVERY rung shows its own beat already happening — he cannot look away; then he closes the distance; then she is already against him; then a hand at her waist and neither of them steady; then his face coming down to hers — never an approach to it, never the room around it, never a mood. Everything past that one beat stays back, the kiss, the words and what they change between the leads included. The restraint is the same as for every other peak; only the line moves, from before the act to one step inside it. DO NOT let a rung take two steps, DO NOT reach the late beats early, and DO NOT leave a rung with no closeness on it at all."""


# ────────────────────
# ROMANCE INTIMACY RUNS
# ────────────────────
# Dropped into {intimacy_run_note} in PRECAP_BLUEPRINT_SYSTEM_PROMPT, right
# after rule 8b. Narrow exception to rules 8/8b: only for an INTIMACY &
# CLOSENESS peak built of a sequence of beats, never any other peak type.

ROMANCE_INTIMACY_RUN_NOTE = """
       ROMANCE INTIMACY RUNS (exception to 8/8b, the outcome rule and the final-limit checks): when the scene is an INTIMACY & CLOSENESS peak, split it into its own small beats in the order they happen and give the run ONE beat per rung, in that order. The beats run from the first look to the last word, roughly: he sees her and cannot hold himself; he closes the distance; she is already against him; a hand at her waist and neither of them steady; his face coming down to hers; something said low that changes what they are to each other; the kiss; the confession.
       COUNT THE RUNGS, THEN CUT THAT MANY BEATS, and cut them from the START of the scene. A run of eight gets eight beats, so its first rung is the look that will not break, not the kiss. DO NOT hand the first rung the contact while the beats before it are still unused, and DO NOT let one rung carry the hold AND the kiss AND the words: a rung is ONE beat.
       Each rung's PERMIT names its own beat as already happening, plainly. The next rung moves exactly one beat further. DO NOT repeat a beat an earlier rung named, DO NOT skip ahead past the next beat, and DO NOT compress the beats to fit the run: the more rungs, the finer the beats.
       Each rung's PROHIBIT holds only the beats that come after its own, and what they change between the leads. DO NOT put a beat that an earlier rung already named in any PROHIBIT.
       A beat whose weight is what it will change (a whispered line, a decision) is named by its weight, never its content: that something was said that changes both their lives, not what. DO NOT put the words themselves into any PERMIT, at any rung.
       If the scene is a single beat, anchor it as a one-chapter run and name that beat plainly in the PERMIT.
       Only INTIMACY & CLOSENESS peaks get this; every other peak type still holds the act back per 8/8b.
"""

# ────────────────────
# ROMANCE UNKNOWN LEAD
# ────────────────────
# Dropped into {unknown_lead_note} in PRECAP_BLUEPRINT_SYSTEM_PROMPT, at the end
# of rule 7 (the reader's-knowledge rule). Narrow exception: only the two leads,
# never a side character.

ROMANCE_UNKNOWN_LEAD_NOTE = """
       ROMANCE EXCEPTION: the ban above is for side characters only. If the person missing from chapter N is the OTHER LEAD, do not drop the scene — write scene_description and bridge_reasoning with that lead's real name as usual, the same way across the whole run. Do not mark this in scene_description itself: it must stay identical for every chapter in the run, and whether this lead is known yet is a per-chapter fact the hook writer checks directly against chapter N's own text, not something planned here. Side characters stay fully out, as above.
"""
