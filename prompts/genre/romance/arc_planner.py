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
