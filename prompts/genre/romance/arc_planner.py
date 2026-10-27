# Romance-specific blocks for the Pass 1 blueprint prompt, dropped into the
# placeholders in prompts/arc_prompt.py::PRECAP_BLUEPRINT_SYSTEM_PROMPT by
# build_blueprint_prompt: peak types, dominant emotions and the ranking note.

ROMANCE_EVENT_TYPES = """       
       • COMING-TOGETHER: the leads are just about to come together — an almost-kiss, a confession on the tip of the tongue, one reaching for the other, being put into the same room or the same bed
       • GOING-APART: they are just about to go apart — a walkout, a misunderstanding about to harden, an ultimatum, a third party stepping between them, one deciding to leave
       • DANGER: one of them is about to face danger — a threat arriving, a secret about to be exposed, harm closing in on one while the other may or may not know
       • REALISATION: one of them realises love, affection, or a bond — a quiet but permanent internal shift, even when nothing external happens
       • INTIMACY & CLOSENESS: the leads are about to share a moment of real closeness — a touch that lingers, a held gaze, a shared silence, one caring for the other, a guard coming down, a private moment neither planned. The peak is the closeness itself, even when no kiss, confession or clash is in it
       • LIFE-UPENDED: their lives are about to change completely or stop being normal — a marriage, a contract, a move, a pregnancy, a family decision, a truth that can't be taken back
       These names are a prompt, not a boundary. Anything that closes the distance between the leads, threatens to widen it, puts either of them in danger, shifts what one of them feels, or resets the terms of their life together is a peak worth taking even if it fits none of them. A romance serial's peaks are almost always about what is happening BETWEEN the two leads, even in a chapter with no villain and no plot event at all — a long silence, a held glance, or a chance not taken is still a peak if it moves the distance between them."""

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
       INTIMACY AND CLOSENESS RANK HIGHEST. If any chapter inside the window holds an intimacy or closeness scene between the leads (a touch, a kiss, a shared bed or room, a guard coming down, a private moment between them), that scene is one of your top-ranked peaks and an anchor MUST land on it.
       DO NOT rank any plot event above an intimacy scene because the plot event is bigger, louder or more dramatic.
       DO NOT skip an intimacy scene because the chapters before it hold strong events. No matter how good the events in between are, the intimacy scene wins.
       When an intimacy scene and another strong peak sit in the same lookahead window, anchor on the intimacy scene.
       When several intimacy scenes are in the window, rank all of them above every non-intimacy peak."""

# ────────────────────
# ROMANCE OPENING RUN
# ────────────────────
# Dropped into {opening_run_note} in PRECAP_BLUEPRINT_SYSTEM_PROMPT, right after
# rule 1 (LOOKAHEAD WINDOW). Only the very first run of the story gets this —
# see pipeline/arc_planning.py::enforce_constraints, exempt_first_run.

ROMANCE_OPENING_RUN_NOTE = """
       ROMANCE OPENING RUN: the run starting at chapter 1 is exempt from the {lookahead}-chapter window. Search ALL given chapters for the leads' first or peak intimate or closeness moment and anchor chapter 1 on it, however far out it is. Hold every chapter up to it on that same anchor — sticky anchor still applies — until the reader reaches it; after that, the ordinary window and target-reuse cap return for every later run.
       Its final limit may also permit a glimpse of the beat right after the moment, never the moment's own outcome. Each rung's bridge_reasoning should stand on whatever is freshest in its own chapter N, not one fact repeated down the whole run.
"""

# ────────────────────
# ROMANCE INTIMACY RUNS
# ────────────────────
# Dropped into {intimacy_run_note} in PRECAP_BLUEPRINT_SYSTEM_PROMPT, right
# after rule 8b. Narrow exception to rules 8/8b: only for an INTIMACY &
# CLOSENESS peak built of a sequence of beats, never any other peak type.

ROMANCE_INTIMACY_RUN_NOTE = """
       ROMANCE INTIMACY RUNS (exception to 8/8b): when the scene is an INTIMACY & CLOSENESS peak made of a sequence of distinct beats (a look, a touch, an embrace, a kiss, a whispered line), break it into those beats and give the run one beat per rung, in the order they actually happen. The FIRST rung of the run already names its own beat as happening, not as approaching — it is not a threshold-only tease. Each later rung moves on to the NEXT beat in that same order: never repeat a beat already named, and never jump ahead to a later beat before the one before it has had its own rung. If the scene genuinely has only one beat and cannot be broken up this way, anchor it as a one-chapter run instead (rule 5) and name that one beat plainly. What must still stay back at every rung, including the last, is what the closeness means to them afterward: any change in a feeling, a resolve, or what happens next between them. Only INTIMACY & CLOSENESS peaks get this; every other peak type still holds the act back per 8/8b.
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
