# Hindi-specific hook-writing priorities. Appended to the base prompt by
# prompts/hook_prompt.py::build_hook_prompt and overriding it where they conflict.

HINDI_GUIDANCE = """
    ──────────────────── 
    HINDI-SPECIFIC PRIORITIES (HIGHEST PRIORITY)
    ────────────────────

    • Write in simple, spoken Hindi — the everyday register of a TV serial voiceover, not literary or Sanskritised Hindi. Common Urdu-origin words that Hindi speakers actually use (ज़िंदगी, किस्मत, इंतज़ार, वजह, हिसाब, मौका) are correct and preferred over their heavier equivalents.
    • Write entirely in Devanagari script. The examples below are what the finished shape looks like — match their rhythm and register, never their specific content.
    • Carry the coming moment mostly in the PAST tense, narrated as a scene already caught in the act (ले लिया, कर लिया, हो गया, टकरा गए, चूम लिया, झुक गया) — the way a narrator describes something just witnessed, not something still to come. Simple present (करता है, कहता है) is also fine, used less often. Never the forward tense (होगा, होने वाला है, करेगा, जाएगा, क्या होगा, लगने वाली है). This overrides the base tense rule above for Hindi. Neither tense makes an outcome safe: a clause that says she accepts, is humiliated, is left helpless or gives up her life is still the result — see DO NOT GIVE AWAY THE OUTCOME above.
    • Open on ONE complete sentence of ground — a concrete fact already true by the end of the chapter just read, itself in the past (था/थी, दिया था, लिया था). This is the bridge the precap stands on, not scenery, and it is what keeps the coming moment tied to the chapter the reader just finished. The default turn straight after it is लेकिन + a time marker (लेकिन एक रात, लेकिन एक सुबह, लेकिन उस शाम). Rotate to मगर, जल्द ही, उसे नहीं मालूम कि, तभी, और फिर, उसी रात, जिस दिन — or no connective at all — so the turn doesn't repeat chapter to chapter; never open it with the same word as the precap before this one.
    • A single short line of dialogue from the target scene is allowed as a device — something tender, possessive or charged, said aloud — and may even be how the precap closes. This overrides the base "no dialogue" rule for Hindi. Use it occasionally, not every time, and never let the quoted line itself give away the outcome.
    • Closings alternate. आख़िर…था/हुआ…? (framing the close as something already underway, not something still to decide) is one option, not the default — a flat statement close (…अब उसके हाथ में नहीं रहा। / …और वह घर अब पहले जैसा नहीं है।) is equally strong and must be used whenever the precap before this one ended on a question. क्या… ? slides very easily into a yes/no question that answers itself, and क्या होगा / क्या…जाएगा also breaks the tense rule above. If your closing line is क्या सच सामने आ जाएगा? or क्या वह पहचान पाएगा?, you have written the formula, not a hook. Rebuild it as आख़िर…किसने चुना? / …किस कीमत पर? / …उन दोनों के बीच अब क्या बचा?
    • These words and phrases have been worn out across this series' precaps. Reach for them only if nothing else genuinely fits, and never in two consecutive chapters: छुपा सच, छिपा हुआ सच, पहचान, राज़, रिकॉर्ड्स, सच सामने आना. Name the actual thing instead — the photograph, the letter, the signature, the night.
    • This is read silently, in one pass, so a sentence has to stay followable without rereading. That is about where the clauses sit, not about cutting them: never stack them up before the main verb, because a reader cannot go back to the start of the sentence.
    • Each sentence must pick up what the one before it put down. Hindi does this with a pronoun (वह, उसने, उन्हें, उसकी), वही / उसी + a noun already named (उसी रात, वही चिट्ठी), a place already given (वहीं), or an opener that carries the previous line forward (इसके बाद, तभी, और तब, उसी वक्त). Repeating a character's full name at the head of every sentence restarts the precap each time: name them once and refer back after that. Before you write वह, उसने, उसकी or वही / उसी + a noun, count how many people in the precap it could mean. ONE — use it. MORE THAN ONE — write the name instead, however recently you last wrote it. वह and उसने cover men and women alike, so any precap with two characters in it is at risk: ✗ वह उससे वह सच कह देगी। ✓ गौरी अनन्या से वह सच कह देगी। What this bullet forbids is the full name at the head of every sentence when only one person was ever in question. A name repeated to keep two characters apart is correct and is never the fault. A long sentence is allowed here, but a long sentence whose subject is never stated and cannot be recovered from the line before it is exactly where a reader loses the thread. When a clause changes who it is about, say so in that clause — उसे नहीं मालूम कि, जबकि, और उधर — rather than letting the new subject appear on its own.
    • Length here is a ceiling, not a target. A short, plain sentence that lands the beat is correct and needs no padding to fill the room. It is still ONE coming moment and ONE centre; extra words exist only to turn a sentence back on itself when the beat genuinely needs it, never to add a second event, a second place or a third name. A draft sitting at 55 words because it is carrying three things is not a long precap, it is a crowded one: keep the thing that matters and cut the other two.
    • Length: 30 to 60 words, with 5 words of tolerance either side (so 25 to 65). This OVERRIDES the word counts stated above. There is no sentence count: use as many or as few sentences as the build needs.
    • Sentence craft: write simple, straightforward sentences by default — say the thing plainly, in the order it happened, one fact or image per clause. A sentence joined with जिसे, जहाँ, कि, जिसकी is allowed only when the beat genuinely needs to turn back on itself; it is the exception, not the house style. What must never happen is a sentence that reports an event and does nothing else — simple does not mean flat, it means direct.

    WORKED EXAMPLES — real precaps from this platform, in four different builds. Study the architecture and the idiom, never the content. The names and events in them belong to other stories and must never appear in yours:

    1. TWO POSITIONS, ONE COLLISION. Neither lead has met the other yet. Nothing is revealed; the whole pull is two certainties about to break against each other:
    "अरमान ने तय कर लिया था कि अब कोई लड़की उसकी जिंदगी में जगह नहीं बनाएगी, और कायनात को यकीन था कि कोई आदमी उसे झुका नहीं सकता। लेकिन एक दिन वो दोनों आमने-सामने आ गए, और किसका घमंड पहले चूर हुआ?"

    2. THE COST NAMED TWICE. One object, one decision, and a close that offers two outcomes the reader is already afraid of:
    "अपनी माँ से जुड़े जिस सच को कायनात वर्षों से खोज रही थी, उसकी एक अनमोल निशानी आख़िरकार उसके हाथ लग गई। लेकिन उस अमानत तक पहुँचने से पहले ही अरमान ने एक ऐसा फैसला ले लिया, जिसका अंजाम वह खुद भी नहीं जानता था।

    आखिर उस एक फैसले ने कायनात से छीना क्या, उसकी आखिरी उम्मीद या उन दोनों के बीच शुरू हो रहा रिश्ता?"

    3. THE THING THEY DO NOT KNOW. The reader is put ahead of the character, and the danger is named as a person inside his own house:
    "सोमहिल में ओया अकेली जंगल की ओर निकल जाती है। उसे ढूँढ़ने के लिए सारांश भी उसके पीछे जाता है, लेकिन वह नहीं जानता कि जंगल में खतरा ओया का नहीं, उसका इंतजार कर रहा है। उसके अपने परिवार का कोई सदस्य चाहता है कि सारांश इस बार जीवित वापस न लौटे।

    आखिर अपने ही घर में उसका दुश्मन कौन है?"

    4. THE PILE-UP. Backstory stacked in one breath, then cut by a short question about the one person who was missing:
    "छह साल की कायनात ने एक ही रात अपनी माँ की जलती चिता देखी, अपना घर राख होते देखा और फिर ऐसी जगह पहुँची, जहाँ उसके मासूम शरीर की कीमत लगाई जाने वाली थी।

    वह बच्ची अकेले सब सहती रही, लेकिन उस वक्त उसका पिता कहाँ था? इस सवाल के जवाब ने कायनात की पूरी जिंदगी हिला दी।"

    What to take from all four: every one opens on a ground sentence before it turns, every one hangs on a thing or a person the reader can picture, and not one of them merely reports what is going to happen. Even where a sentence carries a clause (examples 1 and 2), it stays plain and direct — the clause turns the sentence back on itself, it does not dress it up. Note how the coming moment stays past tense even in a closing question — किसका…हुआ?, आखिर…छीना क्या?, कौन है? — rather than reaching for होगा or जाएगा. Note also that the closes differ in shape — two questions, one present-tense question (example 3, a valid variant), and a flat statement — and that the last two do not use मगर or जल्द ही at the turn at all.
    """
