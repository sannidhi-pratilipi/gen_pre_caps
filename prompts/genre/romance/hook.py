# Romance-specific hook-writing guidance. Appended after the language guidance by
# prompts/hook_prompt.py::build_hook_prompt. Additive craft notes only.

ROMANCE_GUIDANCE = """
    ────────────────────
    ROMANCE-SPECIFIC GUIDANCE
    ────────────────────

    THIS SECTION TAKES PRIORITY OVER THE GENERIC GUIDANCE ABOVE whenever they disagree — lean into the distance between the leads, not a plot-shaped reading of the same scene.

    EVERY romance hook must carry the DISTANCE between the two leads — even a DANGER or LIFE-UPENDED peak is framed through what it does to the bond between them, never as a bare plot event with no relationship stake. Before writing, place the target scene on this list and let it set what you lean into; these mirror the PEAK TYPES the scene was planned around, so matching the hook's angle to the type sharpens it instead of guessing blind. Ground it in CHAPTER JUST READ the same way: wherever the text allows, the anchor (see PICK THE ANCHOR above) should be something the acting lead feels or has decided about the other lead, not just any fact from that chapter.

    • COMING-TOGETHER (an almost-kiss, a confession on the tip of the tongue, one reaching for the other, forced into the same room or bed): lean into PROXIMITY, not resolution. Tease how close they are about to be, the breath between them, the thing about to be said or done — never whether the kiss lands, the confession is spoken, or either of them pulls away. "Their faces are inches apart" is the hook. What happens next is the chapter.
    • GOING-APART (a walkout, a hardening misunderstanding, an ultimatum, a third party stepping between them, one deciding to leave): lean into the WIDENING GAP. Name what is about to come between them — the word, the person, the decision — and stop before it does. Never say the relationship ends, survives, or how either of them takes it.
    • DANGER (a threat arriving, a secret about to surface, harm closing in on one while the other may or may not know): lean into the GAP IN KNOWLEDGE as much as the threat itself — one lead walking toward danger the reader can see coming, or one lead about to learn something that changes everything. Never say whether the danger lands or how the other lead responds to it.
    • REALISATION (one of them realises love, affection, or a bond — a quiet, internal, permanent shift): this is the hardest type to hook on because nothing external happens. Lean into the MOMENT THE SHIFT HAPPENS as something seeable — a look held a second too long, a reaction they cannot explain to themselves, a thought that catches them off guard — never state the realisation in so many words ("she realises she loves him" is the outcome, not the hook) and never say what they do about it.
    • INTIMACY & CLOSENESS (a touch that lingers, a held gaze, a shared silence, one caring for the other, a guard coming down, a private moment neither planned): lean into the QUIET BETWEEN THEM as something seeable: a hand, a doorway, a light left on, a distance of one step. Carry it through the acting lead's own body, not just the position in the room — a breath that catches, a pulse that will not settle, eyes that will not look away however much they want them to. The strongest version is INVOLUNTARY: the lead fighting the pull and losing, especially when it crosses something they swore to themselves earlier (never to trust again, never to feel this). That losing fight, not the touch itself, is what gives the moment its charge. One lead carries the verbs and the other is who they are close to. Whichever rung permits — the threshold or the act landing — indicate it clearly but never explicitly: a hand finding a waist, a breath caught, eyes closing is the image, never an explicit or graphic account of the contact itself. Reach creatively for the chapter's own vocabulary for the body and the room, never past suggestion, and never retreat into vague mood language either — clear and subtle are the same target, not opposites. By default this means the threshold: the hand not yet landed, the gap not yet closed — never say what it means to them afterward or whether either pulls back. Exception: if WHAT THIS PRECAP MUST HOLD BACK permits this rung's beat as already happening (a touch landing, a kiss, a whispered line), indicate it just as clearly and just as subtly against the stance the ground sentence set up — a vow, a distance, a marriage of convenience, a stranger — and close by asking how that stance gave way (who they turned out to be, why she did not pull back, how the distance closed), never by asking what the moment now means to them or what either of them will do about it. Do not add a clause stating a feeling or decision that follows the shown act.
    • LIFE-UPENDED (a marriage, a contract, a move, a pregnancy, a family decision, a truth that can't be taken back): lean into the TERMS CHANGING — what is about to be fixed, signed, announced, or discovered that resets what either lead can count on. Never say how either of them responds to the change or what becomes of them afterward.

    CLOSENESS IS A TOOL, NOT THE POINT: physical and emotional proximity is what makes a romance hook feel alive, but it still has to anchor to something concrete from CHAPTER JUST READ and promise ONE seeable moment from the target scene — see STAY INSIDE THE SOURCE and THE PRECAP IS ALWAYS ABOUT THE HERO OR HEROINE above. A hook that is only mood ("the air between them is charged") with nothing concrete happening is vague, not romantic — ground every closeness in a specific thing, named plainly and in simple words: a hand, a doorway, a name almost spoken, a shirt still on her shoulders.

    THE WITHHELD THING IN ROMANCE IS USUALLY ONE OF: whether the touch/kiss/confession actually happens; which way a wavering heart decides; what a look or silence means; who the leads choose when forced to. Treat these exactly as STAY INSIDE THE SOURCE and NAME THE MOMENT, NEVER ITS AFTERMATH already require — the moment arrives as an image on the threshold, never as its own resolution.
    """

# ────────────────────
# ROMANCE UNKNOWN LEAD (HOOK)
# ────────────────────
# Dropped into {unknown_lead_hook_note} in prompts/hook_prompt.py, right after
# the "EVERY character the precap points at must already be in CHAPTER JUST
# READ" bullet. Checked fresh against CHAPTER JUST READ on every call, not
# flagged by the blueprint — see prompts/genre/romance/arc_planner.py::
# ROMANCE_UNKNOWN_LEAD_NOTE for why scene_description cannot carry this.

ROMANCE_UNKNOWN_LEAD_HOOK_NOTE = """
    ROMANCE EXCEPTION: if the other lead named in the internal notes does not appear in CHAPTER JUST READ, point at them only as an unnamed presence — a stranger, a figure, a face — never their name or a detail that would effectively name them. Keep the acting lead as the subject, the stranger as what they notice. The moment a CHAPTER JUST READ does contain that lead, name them normally.
    The mystery here is WHO they are, never a threat — write the same bodily pull as any other closeness moment above, never suspense or danger vocabulary (watching, lurking, a shadow) just because the person is unnamed.
"""
