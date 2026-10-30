# Hindi-specific hook-writing priorities. Appended to the base prompt by
# prompts/hook_prompt.py::build_hook_prompt and overriding it where they conflict.

HINDI_GUIDANCE = """
    ──────────────────── 
    HINDI-SPECIFIC PRIORITIES (these override the base rules above)
    ────────────────────

    • Write in simple, spoken Hindi — the everyday register of a TV serial voiceover, not literary or Sanskritised Hindi. Common Urdu-origin words that Hindi speakers actually use (ज़िंदगी, किस्मत, इंतज़ार, वजह, हिसाब, मौका) are correct and preferred over their heavier equivalents.
    • Write entirely in Devanagari script. The examples below are what the finished shape looks like — match their rhythm and register, never their specific content.
    • Carry the coming moment mostly in the PAST tense, narrated as a scene already caught in the act (ले लिया, कर लिया, हो गया, टकरा गए, चूम लिया, झुक गया) — the way a narrator describes something just witnessed, not something still to come. Simple present (करता है, कहता है) is also fine, used less often. Never the forward tense (होगा, होने वाला है, करेगा, जाएगा, क्या होगा, लगने वाली है). This overrides the base tense rule above for Hindi. Neither tense makes an outcome safe: a clause that says she accepts, is humiliated, is left helpless or gives up her life is still the result — see DO NOT GIVE AWAY THE OUTCOME above.
    • OPEN ON ONE COMPLETE SENTENCE OF GROUND — the anchor, a concrete fact already true by the end of the chapter just read, written in the past (था/थी, दिया था, लिया था, कह दिया था). Then turn from it into the coming moment with लेकिन + a time or place marker (लेकिन एक रात, लेकिन एक सुबह, लेकिन उस शाम), rotating to मगर, जल्द ही, उसे नहीं मालूम कि, तभी, और फिर, उसी रात, जिस दिन or no connective at all so the turn doesn't repeat chapter to chapter. Never open a turn with the same word as the precap before this one. DO NOT open inside the scene with no ground sentence.
    • A single short line of dialogue from the target scene is allowed as a device — something tender, possessive or charged, said aloud — and may even be how the precap closes. This overrides the base "no dialogue" rule for Hindi. Use it occasionally, not every time, and never let the quoted line itself give away the outcome.
    • Closings alternate. आख़िर…था/हुआ…? (framing the close as something already underway, not something still to decide) is one option, not the default — a flat statement close (…अब उसके हाथ में नहीं रहा। / …और वह घर अब पहले जैसा नहीं है।) is equally strong and must be used whenever the precap before this one ended on a question. क्या… ? slides very easily into a yes/no question that answers itself, and क्या होगा / क्या…जाएगा also breaks the tense rule above. If your closing line is क्या सच सामने आ जाएगा? or क्या वह पहचान पाएगा?, you have written the formula, not a hook. Rebuild it as आख़िर…किसने चुना? / …किस कीमत पर? / …उन दोनों के बीच अब क्या बचा? The one close exempt from the alternation is आखिर…क्यों…? / …कैसे…? asking why the person did what the precap just showed: across a run of precaps on one closeness scene that is the right close every time, and the variety comes from the beat.
    • These words and phrases have been worn out across this series' precaps. Reach for them only if nothing else genuinely fits, and never in two consecutive chapters: छुपा सच, छिपा हुआ सच, पहचान, राज़, रिकॉर्ड्स, सच सामने आना, धड़कनें तेज़ हो गईं, साँसें थम गईं, नज़रें ठहर गईं, दोनों बेहद करीब आ गए, खुद को रोक नहीं पाया, पुरानी मोहब्बत फिर जाग उठी. Name the actual thing instead — the photograph, the letter, the signature, the night.
    • This is read silently, in one pass, so a sentence has to stay followable without rereading. That is about where the clauses sit, not about cutting them: never stack them up before the main verb, because a reader cannot go back to the start of the sentence.
    • Each sentence must pick up what the one before it put down. Hindi does this with a pronoun (वह, उसने, उन्हें, उसकी), वही / उसी + a noun already named (उसी रात, वही चिट्ठी), a place already given (वहीं), or an opener that carries the previous line forward (इसके बाद, तभी, और तब, उसी वक्त). Repeating a character's full name at the head of every sentence restarts the precap each time: name them once and refer back after that. Before you write वह, उसने, उसकी or वही / उसी + a noun, count how many people in the precap it could mean. ONE — use it. MORE THAN ONE — write the name instead, however recently you last wrote it. वह and उसने cover men and women alike, so any precap with two characters in it is at risk: ✗ वह उससे वह सच कह देगी। ✓ गौरी अनन्या से वह सच कह देगी। What this bullet forbids is the full name at the head of every sentence when only one person was ever in question. A name repeated to keep two characters apart is correct and is never the fault. A long sentence is allowed here, but a long sentence whose subject is never stated and cannot be recovered from the line before it is exactly where a reader loses the thread. When a clause changes who it is about, say so in that clause — उसे नहीं मालूम कि, जबकि, और उधर — rather than letting the new subject appear on its own.
    • Length here is a ceiling, not a target. A short, plain sentence that lands the beat is correct and needs no padding to fill the room. It is still ONE coming moment and ONE centre; extra words exist only to turn a sentence back on itself when the beat genuinely needs it, never to add a second event, a second place or a third name. A draft sitting at 55 words because it is carrying three things is not a long precap, it is a crowded one: keep the thing that matters and cut the other two. Spend the room on depth, not on more events: a fuller, more vivid telling of the ONE beat.
    • Length: 30 to 60 words, with 5 words of tolerance either side (so 25 to 65). This OVERRIDES the word counts stated above. There is no sentence count: use as many or as few sentences as the build needs.
    • Sentence craft: write simple, straightforward sentences by default — say the thing plainly, in the order it happened, one fact or image per clause. A sentence joined with जिसे, जहाँ, कि, जिसकी is allowed only when the beat genuinely needs to turn back on itself; it is the exception, not the house style. Keep each sentence to roughly 15 words or fewer with one movement in it; four short sentences carry a closeness beat better than two long ones. What must never happen is a sentence that reports an event and does nothing else — simple does not mean flat, it means direct.

    • Write it dramatic and cinematic, not summarised. Give the ONE coming beat its full weight: slow it down and let the reader see it, in simple spoken Hindi. Where the scene has a physical beat, show what the acting lead's body does through it (कमर पर कसती उँगलियाँ, होंठों पर ठहरी नज़र, हिचकिचाहट, झेंप, काँपते हाथ) and how near the two are. The intensity of what the scene already shows may be heightened. DO NOT invent a new action, kiss, confession, reaction or plot turn, and DO NOT add a body reaction the scene does not support.
    • Vary the sensory focus from the precaps shown to you (eye contact, breath, touch, hesitation, a blush, teasing, vulnerability). DO NOT lead with the same one twice in a row.

    THE SHAPE, IN THREE REAL PRECAPS FROM THIS PLATFORM. Study the build and the idiom, never the content — the names and events in them belong to other stories and must never appear in yours. All three run the same way: one past-tense ground sentence, a turn, the moment itself told as plain physical movement, then the close. A danger or secret peak is built exactly the same; what changes is how much of the moment you are permitted to show.

    1. GROUND, TURN, MOMENT, QUESTION ON THE CONTRADICTION:
    "राघव और रिया के धोखे के बाद सुधा ने प्यार से हमेशा के लिए मुँह मोड़ लिया था। लेकिन एक रात वही सुधा किसी अनजान शख्स को बिना शर्ट के अपने सामने देखकर ठिठक गई। उसकी नज़रें चाहकर भी उस शख्स से हट नहीं रही थीं। आखिर कौन था वो, जिसे देखकर सुधा पहली बार अपना टूटा हुआ दिल भूल बैठी?"

    2. THE SAME BUILD, STOPPED AT THE THRESHOLD AND CLOSED ON A STATEMENT:
    "अपने भाई की जान बचाने के लिए सुधा ने अद्विक से मदद माँगी थी, लेकिन उनके बीच की नज़दीकियाँ अब एक अलग ही मोड़ ले रही थीं। अद्विक ने सुधा को अपनी बाँहों में खींच लिया। दोनों के चेहरे इतने करीब थे कि सुधा ने घबराकर अपनी आँखें बंद कर लीं, तभी अद्विक उसके होंठों की तरफ झुक गया।"

    3. THE SAME BUILD, CLOSED ON ONE QUOTED LINE:
    "अद्विक की हरकतों से नाराज़ सुधा ने साफ कह दिया था कि यह शादी सिर्फ एक समझौता है। लेकिन रॉय मेंशन में एक शाम वह अद्विक को बिना शर्ट के देखकर झेंप गई। वह जल्दी से बाहर निकलने लगी, तभी अद्विक ने उसे अपनी बाँहों में खींच लिया और मुस्कुराते हुए बोला, “इतनी आसानी से नहीं छोड़ूँगा, पत्नी जी।”"

    What to take from all three: one sentence of ground and then the turn, the moment given as movement a reader can see, every sentence plain and direct, and nothing said about what the moment did to either of them afterward. Note the past tense throughout, the closing question in the past (कौन था वो) rather than होगा or जाएगा, and that the closes differ — a question, a statement, a line of dialogue.
    """


# Appended by prompts/hook_prompt.py::build_hook_prompt only for Hindi romance, at the very
# end of the prompt. These set the REGISTER of the closeness beat; HINDI_GUIDANCE's three
# examples above still set only the build.
HINDI_ROMANCE_EXAMPLES = """
    ────────────────────
    HINDI ROMANCE REGISTER (this is how the closeness beat must SOUND)
    ────────────────────

    The three examples above show the build. These three show the voice, and for a closeness beat the voice is the one below, not the flatter one above. The ground sentence is short (about 12 words or fewer) so the beat gets the room. The beat is felt, not choreographed: each sentence carries what the lead is feeling (the ache, the want, the pull they cannot resist and the fight they lose against it), heightened and dramatic, in plain everyday spoken Hindi with no heavy words. The names and events belong to no story here and must never appear in yours.

    1. ATTRACTION, CLOSED ON THE CONTRADICTION:
    "आरव से दूर रहने की कसम सिया ने खुद खाई थी। लेकिन उस रात उसकी उँगलियाँ कमर पर कसीं तो सिया का पूरा बदन सिहर उठा। आरव की गर्म साँस गाल को छू रही थी और उसकी नज़र बार-बार उसके होंठों पर जा रही थी, जैसे वह अपने ही दिल से हार रही हो। आखिर जिस आग से वह इतने महीने भागती रही, उसी ने उसे आज क्यों रोक लिया था?"

    2. TENDER CARE, CLOSED ON A STATEMENT (no lust forced in):
    "मीरा के सामने कभी कमज़ोर न पड़ने का वादा रोहन ने खुद से किया था। लेकिन जब मीरा का सिर उसके कंधे पर टिका, तो उसके अंदर कुछ पिघल गया और उसका हाथ अपने आप उसके बालों में उलझ गया। वह उसे बस यूँ ही थामे रहना चाहता था, और कमरे में बस दो धीमी साँसें बची थीं।"

    3. PLAYFUL, CLOSED ON ONE QUOTED LINE:
    "यह शादी सिर्फ एक समझौता है, यह बात काव्या ने पहले ही दिन साफ कर दी थी। लेकिन एक शाम अयान ने उसे दीवार और अपने बीच घेर लिया और उसकी नज़र काव्या के होंठों तक उतर आई। काव्या का चेहरा लाल पड़ गया, दिल बेकाबू हो उठा, तभी वह धीरे से झुककर बोला, “अब बताओ, समझौते में यह कहाँ लिखा था?”"
    """
