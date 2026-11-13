# DISABLED: the arc planner now runs one prompt for every genre (prompts/arc_prompt.py),
# with romance folded into its ranking. Kept commented for reference.

# # Romance-specific blocks for the Pass 1 blueprint prompt, dropped into the
# # placeholders in prompts/arc_prompt.py::PRECAP_BLUEPRINT_SYSTEM_PROMPT by
# # build_blueprint_prompt: peak types, dominant emotions and the ranking note.
#
# ROMANCE_EVENT_TYPES = """       ONLY A ROMANTIC MOMENT BETWEEN A LEAD AND SOMEONE THE STORY RUNS A REAL ROMANCE FOR THEM WITH CAN BE A TARGET, NO MATTER WHAT.
#        • The leads are the hero and heroine, and ALSO a second man or woman the story gives many chapters and real romantic moments with one of them. They are a lead for those scenes, and their scenes with that lead are targets exactly like the main pair's.
#        • What settles this is the romantic moments on the page, NOT who the story calls its hero. An author's note naming the hero, or one man being the one the heroine loves, does not rule the other out. Being powerful, often present, or married to a lead does not make one a lead.
#        • Both must be in the moment, together. DO NOT pick a kiss, touch or closeness between a lead and anyone who is not a lead. DO NOT pick a moment one of them has alone. The moment is between two people. If three people act on each other at once (two men and one woman, a rival stepping in), DO NOT pick it. Separate pair moments are allowed only when each is its own scene, never one scene split across PERMITs.
#        • The moment is one of these: a kiss, a touch, a hold, coming close, a shared room or bed, one caring for the other with their hands or body, a near-kiss, a charged closeness. A target scene must contain physical closeness or touch between the two leads in it.
#        • DO NOT pick a plot event, a confrontation, a danger, a secret, a family or career event, a walkout, a conversation or a realisation as the target, however big it is. The types below are only ways a romantic moment can be shaped. A scene with no touch or closeness between the leads in it is never picked, even if it fits one of them.
#        • If no chapter in view holds a kiss or touch, take the scene with the most physical closeness between the leads (the two in the same place, near each other, the charge of being close).
#        • COMING-TOGETHER: the leads are just about to come together — an almost-kiss, a confession on the tip of the tongue, one reaching for the other, being put into the same room or the same bed
#        • GOING-APART: they are just about to go apart — a walkout, a misunderstanding about to harden, an ultimatum, a third party stepping between them, one deciding to leave
#        • DANGER: danger reaching one of them with the other right there — a threat arriving between them, a secret breaking open in front of the other, one of them stepping into the harm closing on the other. A lead facing a threat alone is not the peak; the moment the other reaches them is
#        • REALISATION: one of them realises love, affection, or a bond with the other standing right in front of them — a quiet but permanent internal shift, caught in a look held too long or a reaction they cannot explain. A lead alone with their thoughts is not the peak
#        • INTIMACY & CLOSENESS: the leads are about to share a moment of real closeness — a touch that lingers, a held gaze, a shared silence, one caring for the other, a guard coming down, a private moment neither planned. The peak is the closeness itself, even when no kiss, confession or clash is in it
#        • LIFE-UPENDED: their lives are about to change completely or stop being normal — a marriage, a contract, a move, a pregnancy, a family decision, a truth that can't be taken back
#        These names are a prompt, not a boundary, but every peak taken must be a romantic moment with physical closeness or touch between the two leads in it (see the rule at the top of this list). Anything that closes the physical distance between the leads counts, even in a chapter with no villain and no plot event at all. A moment with no touch or closeness is not a peak for this blueprint.
#        BOTH LEADS ARE IN THE PEAK, IN THE SAME PLACE AT THE SAME TIME. The peak is what passes BETWEEN them — what one does to, says to, or does in front of the other. DO NOT pick a moment one lead has on their own, however much it is about the other: thinking of them, deciding about them, weeping over them, finding out about them, or acting on them somewhere they are not.
#        DO NOT build a scene_description out of two moments at once, one lead in each — "she says it in the classroom while he watches a video at his flat" is two scenes, not a peak, and a precap aimed at it splits the reader between two people. If the chapter's strongest material is one lead alone, take the moment the two of them are actually in a room together instead, even when it is quieter.
#        DO NOT pick a peak that is one lead's own scene with a side character, even when it is driven entirely by feelings about the other lead. A second lead is not a side character: a scene between a lead and a second lead is a peak. A third party may cause the danger, the secret or the obstacle, but the peak itself must be the moment it reaches a lead with the other lead there to see it."""
#
# ROMANCE_EMOTION_LABELS = [
#     "LOVE",
#     "LONGING",
#     "DESIRE",
#     "LUST",
#     "INTIMACY",
#     "JEALOUSY",
#     "TENDERNESS",
#     "HEARTBREAK",
#     "TRUST",
#     "VULNERABILITY",
#     "PROTECTIVENESS",
#     "POSSESSIVENESS",
# ]
#
# # The emotion names the blueprint prompt's own examples use, in romance terms, so the
# # romance prompt never mentions a label that is not in ROMANCE_EMOTION_LABELS.
# ROMANCE_EMOTION_EXAMPLES = {
#     "repeat": "LONGING, LONGING, LONGING",
#     "run": "VULNERABILITY (what it will cost her), then TRUST (who is really behind it), then HEARTBREAK (what she loses when it lands)",
#     "tags": ["VULNERABILITY", "LONGING", "TRUST"],
# }
#
# ROMANCE_EMOTIONS = "  ".join(ROMANCE_EMOTION_LABELS) + """
#        Every one of these is a feeling about the two leads and what is between them. Choose only from this list. Do not use FEAR, REVENGE, BETRAYAL, MYSTERY, SHAME or any other label that is not about love, even when the scene is a danger or a secret: promise the love feeling that scene puts at risk (a danger scene is PROTECTIVENESS or HEARTBREAK, a secret is TRUST, a rival is JEALOUSY). Use LUST only for a scene of raw physical pull (a body drawn to a body, heat, wanting to touch); never for a scene of care, comfort or distress."""
#
# ROMANCE_RANKING_NOTE = """
#        INTIMACY AND CLOSENESS RANK HIGHEST. If any chapter after {precap_limit} holds an intimacy or closeness scene between the leads (a touch, a kiss, a shared bed or room, a guard coming down, a private moment between them), the marquee event is one of those scenes.
#        DO NOT rank any plot event above an intimacy scene because the plot event is bigger, louder or more dramatic.
#        ONLY A ROMANTIC MOMENT BETWEEN A LEAD AND SOMEONE THE STORY ROMANCES THEM WITH (A KISS, A TOUCH, A COMING CLOSE, PHYSICAL CLOSENESS) CAN BE THE MARQUEE EVENT, AND A SECOND LEAD'S SCENES COUNT.
#        A FIRST outranks any escalation: the leads' first kiss or first intimate moment beats any later or more intimate scene, however far along the story it sits.
#        When several such scenes are available, take the one with the highest stakes for the leads anywhere in chapters after {precap_limit}, and DO NOT prefer one for being near.
#        Among them, the strongest is the one that most overturns where chapters 1 to {precap_limit} leave the leads, so that a reader asks how it came to this. Examples: leads set up as enemies who are now together, now married or bound by a marriage, or in an intimate moment they swore would never happen.
#        Prefer an event that sets a lead's hope in chapters 1 to {precap_limit} against a coming moment the reader can see coming and the lead cannot, so each precap can play the one against the other."""
#
# # ────────────────────
# # ROMANCE INTIMACY EVENT
# # ────────────────────
# # Dropped into {intimacy_run_note} in PRECAP_BLUEPRINT_SYSTEM_PROMPT, right after rule 8b.
# # Applies when the event is a romantic moment between the leads.
#
# ROMANCE_INTIMACY_RUN_NOTE = """
#        ROMANCE INTIMACY EVENT (applies to rule 8's beats and its outcome rule): when the event is a romantic moment between the leads — them touching, holding, reaching for, caring for or coming together — split it into its own small beats in the order they happen and give each chapter ONE beat, in that order. The beats run from the CONTACT to the last word, roughly: she is already against him; his hands have not caught up with her; a hand at her waist and neither of them steady; his face coming down to hers; something said low that changes what they are to each other; the kiss; the confession. The approach is not a beat and never gets a chapter: crossing a room, reaching, almost touching are the run-up, and a limit spent on one shows nothing.
#        • Count the chapters, then cut that many beats from the CONTACT onward. THE FIRST CHAPTER ALREADY SHOWS THE LEADS TOUCHING: never a look across a room. DO NOT hold the touch back for a later chapter, and DO NOT let one chapter carry the hold AND the kiss AND the words: one beat each.
#        • Each PERMIT names its own beat as already happening, plainly. The next chapter moves exactly one beat further. DO NOT repeat a beat an earlier chapter named, DO NOT skip ahead past the next beat, and DO NOT compress the beats to fit: the more chapters, the finer the beats.
#        • Each PROHIBIT holds only the beats that come after its own, and what they change between the leads. DO NOT put a beat that an earlier chapter already named in any PROHIBIT, and NEVER put the contact itself in one: "any physical touch", "any embrace", "what she does with her arms", "whether they touch" are the one thing this event exists to show.
#        • A beat whose weight is what it will change (a whispered line, a decision) is named by its weight, never its content: that something was said that changes both their lives, not what. DO NOT put the words themselves into any PERMIT.
#        • THE INTENSE CLOSE MOMENT IS NEVER FULLY PROHIBITED, HOWEVER FAR AHEAD IT IS: every PERMIT carries at least a HINT that the leads are heading toward it (the pull between them, the line they are near, the want they cannot hide), and no PROHIBIT may rule out the existence of that closeness or the lead's pull toward it. A PROHIBIT holds back only the specifics: how far it goes, the words, and what it changes between them.
#        • EVERY romantic moment between the leads gets this, whatever peak type you labelled it, and every chapter shows closeness and touch, including the chapters still building toward the moment.
# """
#
#
# # ────────────────────
# # ROMANCE UNKNOWN LEAD
# # ────────────────────
# # Dropped into {unknown_lead_note} in PRECAP_BLUEPRINT_SYSTEM_PROMPT, at the end
# # of rule 7 (the reader's-knowledge rule). Narrow exception: only the two leads,
# # never a side character.
#
# ROMANCE_UNKNOWN_LEAD_NOTE = """
#        ROMANCE EXCEPTION: the ban above is for side characters only. If the person missing from chapter N is the OTHER LEAD, do not drop the scene. Write scene_description and bridge_reasoning with that lead's real name as usual, the same way across the whole run. DO NOT mark this in scene_description: it must stay identical for every chapter in the run. Whether this lead is known yet is a per-chapter fact the hook writer checks against chapter N's own text, not something planned here. Side characters stay fully out, as above.
# """
#
#
# ROMANCE_ARC = {
#     "event_types_block": ROMANCE_EVENT_TYPES,
#     "emotion_labels": ROMANCE_EMOTION_LABELS,
#     "emotions_block": ROMANCE_EMOTIONS,
#     "emotion_examples": ROMANCE_EMOTION_EXAMPLES,
#     "ranking_note_block": ROMANCE_RANKING_NOTE,
#     "unknown_lead_note": ROMANCE_UNKNOWN_LEAD_NOTE,
#     "intimacy_run_note": ROMANCE_INTIMACY_RUN_NOTE,
# }
