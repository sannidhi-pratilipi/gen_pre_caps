# Malayalam-specific hook-writing priorities. Appended to the base prompt by
# prompts/hook_prompt.py::build_hook_prompt and overriding it where they conflict.

MALAYALAM_GUIDANCE = """
    ──────────────────── 
    MALAYALAM-SPECIFIC PRIORITIES (these override the base rules above)
    ────────────────────

    • Nothing in this block lets you reveal more. These rules are about how Malayalam SOUNDS: register, verb form, sentence length, build and close. WHAT THIS PRECAP MUST HOLD BACK still decides how much you may say, and you never give the outcome, at any step of a run. Before finishing, ask "does the reader still need to open the chapter?", not "have I said enough?". If a reader could retell the scene from your precap, you have said too much.
    • Write 20-25 words in 2-3 short sentences. This replaces the word and sentence counts above, tolerance included. Count before finalizing and cut if over. The length is fixed; the build is not. Do not build two Malayalam precaps in a row the same way.
    • Write simple, direct, spoken Malayalam, not written Malayalam. Say every line aloud to test it. Choose the plain everyday word over the literary or Sanskritised one, even if the heavy word fits the rhythm better. Use the story's own words for places, relatives, customs and kinds of people, and keep everyday borrowed words as the story uses them. Do not purify them into words no one says.
    • One idea per sentence, in the order a person would say it. Nothing ornate, nothing crowded.
    • Write only in Malayalam script. No English, Hindi, Tamil, Telugu or Kannada words or letters, except a character's exact name or nickname from the chapter. If a concept has no natural Malayalam word, use the Malayalam-script spelling readers actually use. Never leave the English word as it is and never let another script's letters slip into a Malayalam word. An English title before a name (Mr., Dr., Miss) is not part of the name: write it in Malayalam script (മിസ്റ്റർ, ഡോക്ടർ) or leave it out.
    • Every word must be correct standard Malayalam: right case endings (വിഭക്തി), verb tense and agreement, and sandhi (word joining). Re-read once for grammar alone before finalizing.
    • One jaw-dropping action, by one acting lead. Keep the stakes and the drama. Every question in the precap belongs to that one thread.
    • Show what the acting lead feels while doing or receiving the action (കൈ വിറയ്ക്കുന്നു, ശ്വാസം നിലച്ചു, മാറിനിൽക്കാനാവാതെ). Do not name the feeling as a bare label (സങ്കടം തോന്നി) and do not leave a sentence as pure information.

    TENSE
    • The coming moment takes a forward form: ...ും (വരും, പറയും, നടക്കും), ...ാൻ പോകുന്നു, ...ാനിരിക്കുന്നു. This holds even when you open inside the moment. Open on the image (the door, the room, the letter, the night) and let the verb say it has not happened yet: ആ വാതിൽ വൈകാതെ തുറക്കും, never ആ വാതിൽ തുറക്കുന്നു.
    • Do not tell the coming moment in the plain present (ഒരുങ്ങുന്നു, തകരുന്നു, അകപ്പെടുന്നു). The reader would feel they are already inside a scene still chapters away. This is the most common Malayalam failure, so check the main verb of the coming moment first: ✗ അവൾ ആ സത്യം അറിയുന്നു. ✓ അവൾ ആ സത്യം അറിയും. ✗ അവൻ ആ മുറിയിലേക്ക് കടക്കുകയാണ്. ✓ അവൻ ആ മുറിയിലേക്ക് കടക്കാൻ പോകുന്നു. ✗ ആ രഹസ്യം പുറത്തുവരുന്നു. ✓ ആ രഹസ്യം വൈകാതെ പുറത്തുവരും.
    • The ground, where the reader stands now, takes the ongoing present (...ുകയാണ്, ...ുന്നു), never the past: someone is setting out, searching, hoping, praying. This is the one place ...ുന്നു belongs. Ongoing present for the ground, forward form for the coming moment: that split shows the reader where they are. Do not put the coming moment in the ground's form, even when you open mid-action.
    • ...ാൻ പോകുന്നു and ...ാനിരിക്കുന്നു are forward forms even though പോകുന്നു and ഇരിക്കുന്നു look present. Use them freely. A participle or noun form inside the sentence is fine as long as the main verb of the coming moment is forward.

    NEVER GIVE THE OUTCOME
    • A forward form does not make an outcome safe. This is the most common way a Malayalam precap spends its chapter. ...ും and ...ാൻ പോകുന്നു are required for the coming moment, so a result written in them can look allowed. It is not. Find the coming moment, read every clause after it, and ask whether any clause tells HOW IT WENT: who was hurt, what broke, what it led to, how anyone answered. ✗ ആ സാഹസം അവനെ വലിയൊരു ആപത്തിൽ എത്തിക്കും. ✓ അപ്പന്റെ പേരുതന്നെയാണ് ആ സാഹസത്തിൽ പണയം. ✗ മകളുടെ രഹസ്യ സ്വപ്നം ഇതോടെ തകരാൻ പോകുന്നു. ✓ മകൾ ആരോടും പറയാത്ത ആ സ്വപ്നമാണ് അവിടെ ചോദ്യം ചെയ്യപ്പെടുക. ✗ ആ നിമിഷം ഡോക്ടറുടെ ജീവിതത്തെ പ്രതിസന്ധിയിലേക്ക് എത്തിക്കും. ✓ ആ നിമിഷം ഡോക്ടർ കേൾക്കുന്നത് എന്തായിരിക്കും? The ✗ lines are correct Malayalam and follow the forward-form rule, and they still give the chapter away. These are always fine: the ground in the ongoing present, a stake named without its result, a certainty the lead carries INTO the moment (അവൾ വഴങ്ങില്ലെന്ന ഉറപ്പോടെയാണ് അയാൾ ചെല്ലുന്നത്), and a closing question that asks for the very thing held back.

    BUILD
    • The Malayalam precap has a standard three-beat spine:
      1. THE GROUND, in the ongoing present: where the chapter left the reader. Who is setting out, who is hoping, what is already moving.
      2. THE MOVE, in a forward form: the one coming thing, with ...ും or ...ാൻ പോകുന്നു. Point at the moment, do not lay it out. Give ONE concrete thing and no more: the room, the night, the letter, the person already standing there. Do not add who else is in it, what it turns on and how it starts. One hint is a hint; three is the whole scene. Hang the hint on something CHAPTER JUST READ already gave the reader, so one word does the work of three. പക്ഷേ / എന്നാൽ / ഉടൻ / വൈകാതെ work here, or no connective at all.
      3. THE GAP: an open question (ആരുടെ...? എന്തിൽ...? എത്രത്തോളം...?) or one more forward statement that points at what is riding on the moment and stops. A statement here says what the character stands to lose, never what the moment does to anyone. A line that reports the result closes the gap instead of opening it. Keep the spine and change what fills it. The rule against repeating shapes is about the content of the beats and the close (whose ground, which connective, question or statement), never about dropping the three beats.
    • A second build, to rotate with the spine, never used twice running: THE TURN BUILD. Start with the lead's hope in the ongoing present (an exclamation is fine). Add, if you want, one short question about their next step on THE PATH. Then എന്നാൽ and the one coming moment that the reader can see coming and the lead cannot (a plain forward statement or a what-if). Close on the lead's own reaction or choice. It is a feel, not a form: drop or move any part and change how it ends. It may use the extra length the EVENT SERIES note allows. Do not name a second act. Do not go past what WHAT THIS PRECAP MUST HOLD BACK allows. Do not ask about a later discovery or choice unless THE PATH or the LEAD-IN names it.
    • Name people the way this story's own community would, not by bare name alone. A character lands harder with an epithet built from words the chapters use: a place the reader knows joined to a trait, a role used in place of a name, or a pair of opposed moral tags when two people are about to collide. The name can sit beside the epithet or be held back entirely. A precap of bare names sounds flat in Malayalam.
    • Never name, or describe by an epithet, a person CHAPTER JUST READ has not introduced, such as the other lead of the event. Call them only an unnamed stranger (അപരിചിതൻ, ഒരാൾ) and keep the acting lead as the subject. Do not use ആ + a noun or അവൻ/അവൾ for them before they are introduced. The epithet rule above is only for people the reader has already met.
    • Let the coming moment ARRIVE somewhere physical. These precaps land hardest when something reaches a place the reader can see: a doorstep, a house, a family's name, a vehicle pulling up. Prefer a thing reaching a place over saying in the abstract that a change is coming. This guards against vagueness and never lets you disclose more. It asks for ONE seeable thing, still bound by WHAT THIS PRECAP MUST HOLD BACK. If the limit will not let you show what arrives, show only that something is on its way to a door the reader already knows, and stop.
    • The turn into the coming moment can use പക്ഷേ, എന്നാൽ, ഉടൻ, വൈകാതെ, അവൾക്കറിയില്ല, അന്ന് രാത്രി, ആ ദിവസം, or no connective at all by naming the moment outright. Rotate through these. Never open the turn with the same word as the precap before.

    CLOSING
    • Alternate the closings. This is where these precaps go wrong most often. A question close is right when it asks for a withheld identity (സ്വന്തം വീട്ടിലെ ശത്രു ആരാണ്?) or names two outcomes that both hurt.
    • Do not use the yes/no form. A line ending ...ഉമോ? or ...ആണോ? (രക്ഷപ്പെടാൻ കഴിയുമോ?) answers itself, because the reader knows the story is not over. Exception: allowed when it asks whether the lead will see through something the reader already sees (തിരിച്ചറിയുമോ?).
    • Question closes may run back to back, but never three in a row. When the two precaps before this one both ended on a question, close this one on a statement. Build that statement on what is at stake, not on what the moment costs: ...അവൾക്ക് നഷ്ടപ്പെടാനുള്ളത് ആ ഒരൊറ്റ പേരാണ്. / ...ആ മറുപടിയിലാണ് രണ്ടുപേരുടെയും ജീവിതം.
    • A statement close must not report the result. Avoid two shapes: ...സകല പ്രതീക്ഷകളും അതോടെ തകരും and ...ഇനി പഴയതുപോലെയാകില്ല. The first says how it went, and the second would fit the end of any precap for any chapter.
    • These words are worn out in this series. Use one only if nothing else fits, and never in two chapters in a row: രക്ഷപ്പെടുക, കെണി, ചതി, നിഗൂഢ, രൂപം, ഭയം. Name the actual thing instead: the room, the letter, the phone call, that night.

    LINKING AND NAMES
    • Each sentence must pick up what the one before it put down. Malayalam does this without getting longer: a pronoun (അവൾ, അയാൾ), ആ + a noun already named (ആ രാത്രി, ആ കത്ത്), a place already given (അവിടെ), or a carrying opener (അതോടെ, അപ്പോൾ, അതിനുശേഷം).
    • Do not start every sentence with the character's full name. That breaks the chain and restarts the precap each time. Name them once, then refer back.
    • Before you write അവൾ, അയാൾ or ആ + a noun, count how many people in the precap it could mean. One: use it. More than one: write the name, however recently you last wrote it. Two women both take അവൾ and two men both take അയാൾ, so two leads of the same gender need names, not pronouns: ✗ അവൾ അവളോട് ആ സത്യം പറയും. ✓ ഗൗരി അനന്യയോട് ആ സത്യം പറയും.
    • A name repeated to keep two characters apart is correct. The fault is a full name at the head of every sentence when only one person was ever in question.
    • Watch for two failures:
      – a middle sentence that restates the first from another angle instead of moving forward (അനം ഹമീദിക്ക് ഭയം തോന്നുന്നു, after her danger was already named);
      – a closing line that drops the concrete thing just named and ends on something general enough to fit any other chapter. The close lands on what the sentence before it put down.
    """


# Appended by prompts/hook_prompt.py::build_hook_prompt only for Malayalam romance, at the
# very end of the prompt. Fits the romance voice into Malayalam's own limits (20-25 words,
# short sentences, forward form for the coming moment) and never relaxes them.
MALAYALAM_ROMANCE_GUIDANCE = """
    ────────────────────
    MALAYALAM ROMANCE VOICE (sensual, inside Malayalam's own limits)
    ────────────────────

    • The romance voice above applies in full, and it is carried inside the Malayalam limits: 20-25 words, short sentences, plain spoken words, and the forward form for the coming moment. Nothing here lengthens a sentence or lets in a heavy word.
    • Make it sensual through the body and the pull, in simple words: a hand tightening on a waist, a breath on a cheek, eyes dropping to lips, a touch in hair, a body drawn close. Show the touch plainly in the forward form (...മുറുകാൻ പോകുന്നു, ...തൊടും), never as a bare mood and never graphic.
    • Put what the lead cannot resist in ONE short phrase: the want they cannot hide, the pull they lose against. Let the forward form carry the touch and the want together, so one sentence does both.
    • Keep the ground sentence very short (about 8 words), in the ongoing present, so the beat gets the room.
    • The body and the pull stay required in every build, THE TURN BUILD included: the sentence that carries the coming moment names what the body does (a breath, a hand, eyes, heat) and the want the lead cannot resist, in ONE short phrase. A turn build with only plot and questions and no body or pull is not a romance precap.
    • Vary the focus from the precap before (eyes, breath, hands, hair, closeness, teasing). In a care or comfort scene the pull is tenderness, still shown through touch.
    • Tell every action with the feeling it is done with, in your own way: lean most on വയറ്റിൽ ചിത്രശലഭങ്ങൾ പറക്കുന്ന പോലെ, ദേഹത്തിലൂടെ ഒരു തരിപ്പ് പാഞ്ഞു, സ്വയം തടയാനാവാതെ; also സ്നേഹത്തോടെ, അമ്പരന്ന്, വിറയ്ക്കുന്ന കൈകളോടെ. Pick the one that fits the moment and change it from precap to precap. DO NOT write an action bare.

    REFERENCE EXAMPLES, for the feel only. DO NOT copy their order, questions or endings, or their names and facts:

    1. "ഹരിയോടുള്ള പ്രണയം തുറന്നുപറയാൻ കാത്തിരിക്കുന്ന നിള അവനെ നേരിൽ കാണുമ്പോൾ എന്ത് സംഭവിക്കും? എന്നാൽ ഒരുനാൾ അവൾക്ക് ലഭിക്കുന്ന ആദ്യ ചുംബനം താൻ കരുതുന്ന ആളിൽ നിന്നല്ലെങ്കിലോ?"

    2. "തന്നെ അവഗണിച്ച ഹരി അടുത്ത കൂടിക്കാഴ്ചയിൽ സ്നേഹത്തോടെ പെരുമാറുന്നത് കണ്ട് നിള അമ്പരക്കുന്നു! എന്നാൽ ആ സ്നേഹത്തിന് പിന്നിൽ അവൻ ഒളിച്ചുവച്ച ഒരു കാര്യമുണ്ട്, അത് നിളയുടെ ഇഷ്ടത്തോടാണ് ഏറ്റുമുട്ടാൻ പോകുന്നത്."

    3. "മാറിമാറുന്ന ഹരിയുടെ പെരുമാറ്റത്തിനിടയിലും നിള പ്രണയം തുറന്നുപറയാൻ പോകുന്നു! അവന്റെ മറുപടി എന്തായിരിക്കും? എന്നാൽ തന്നെ ചുംബിച്ചതിന് പിന്നിലെ സത്യം അറിയുമ്പോൾ നിള ആരെ തിരഞ്ഞെടുക്കും?"
    """
