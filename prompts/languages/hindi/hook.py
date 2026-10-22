# Hindi-specific hook-writing priorities. Appended to the base prompt by
# prompts/hook_prompt.py::build_hook_prompt and overriding it where they conflict.

HINDI_GUIDANCE = """
    ──────────────────── 
    HINDI-SPECIFIC PRIORITIES (HIGHEST PRIORITY)
    ────────────────────

    • Write in simple, spoken Hindi — the everyday register of a TV serial voiceover, not literary or Sanskritised Hindi. Common Urdu-origin words that Hindi speakers actually use (ज़िंदगी, किस्मत, इंतज़ार, वजह, हिसाब, मौका) are correct and preferred over their heavier equivalents.
    • Write entirely in Devanagari script. The examples below are what the finished shape looks like — match their rhythm and register, never their specific content.
    • Carry the coming moment in the forward tense (करेगा, होने वाला है, लगने वाली है, आने वाला है). The forward tense does NOT make an outcome safe. A clause in it that says she will accept, will be humiliated, will be left helpless or will have to give up her life is still the result: see DO NOT GIVE AWAY THE OUTCOME above. Keep the coming moment itself in the forward tense and let nothing after it say how it went or what it did to anyone.
    • The turn into it can be made with मगर, लेकिन, जल्द ही, उसे नहीं मालूम कि, तभी, और फिर, उसी रात, जिस दिन — or with no connective at all, by simply naming the moment. This is a pool to rotate through, not a house style: never open the turn with the same word as the precap before this one, and if the last two both began मगर जल्द ही, that construction is spent for now. Turning without a connective is the cleanest way to break the pattern.
    • Closings alternate. आख़िर… ? is one option, not the default — a flat statement close (…अब उसके हाथ में नहीं रहा। / …और वह घर अब पहले जैसा नहीं रहेगा।) is equally strong and must be used whenever the precap before this one ended on a question. क्या… ? slides very easily into a yes/no question that answers itself. If your closing line is क्या सच सामने आ जाएगा? or क्या वह पहचान पाएगा?, you have written the formula, not a hook. Rebuild it as आख़िर…क्या चुनेगा? / …किस कीमत पर? / …उन दोनों के बीच अब क्या बचेगा?
    • These words and phrases have been worn out across this series' precaps. Reach for them only if nothing else genuinely fits, and never in two consecutive chapters: छुपा सच, छिपा हुआ सच, पहचान, राज़, रिकॉर्ड्स, सच सामने आना. Name the actual thing instead — the photograph, the letter, the signature, the night.
    • This is read aloud by a narrator, so a sentence has to stay followable by ear. That is about where the clauses sit, not about cutting them: never stack them up before the main verb, because a listener cannot go back to the start of the sentence.
    • Each sentence must pick up what the one before it put down. Hindi does this with a pronoun (वह, उसने, उन्हें, उसकी), वही / उसी + a noun already named (उसी रात, वही चिट्ठी), a place already given (वहीं), or an opener that carries the previous line forward (इसके बाद, तभी, और तब, उसी वक्त). Repeating a character's full name at the head of every sentence restarts the precap each time: name them once and refer back after that. Before you write वह, उसने, उसकी or वही / उसी + a noun, count how many people in the precap it could mean. ONE — use it. MORE THAN ONE — write the name instead, however recently you last wrote it. वह and उसने cover men and women alike, so any precap with two characters in it is at risk: ✗ वह उससे वह सच कह देगी। ✓ गौरी अनन्या से वह सच कह देगी। What this bullet forbids is the full name at the head of every sentence when only one person was ever in question. A name repeated to keep two characters apart is correct and is never the fault. A long sentence is allowed here, but a long sentence whose subject is never stated and cannot be recovered from the line before it is exactly where a listener loses the thread. When a clause changes who it is about, say so in that clause — उसे नहीं मालूम कि, जबकि, और उधर — rather than letting the new subject appear on its own.
    • Length here is permission, not a target. Hindi runs longer than the other languages because its clauses carry the drama, not because there is room for more content. It is still ONE coming moment and ONE centre; the extra words exist to turn a sentence back on itself, never to add a second event, a second place or a third name. A draft sitting at 55 words because it is carrying three things is not a long precap, it is a crowded one: keep the thing that matters and cut the other two.
    • Length: 30 to 60 words, with 5 words of tolerance either side (so 25 to 65). This OVERRIDES the word counts stated above. There is no sentence count: use as many or as few sentences as the build needs.
    • Sentence craft: a Hindi precap sentence is allowed to be long, and usually is. Clauses joined with जिसे, जहाँ, कि, जिसकी are correct here and carry the drama — "एक ऐसी रात में ला खड़ा करेगी, जहाँ बदला लेने का मौका भी होगा और पीछे हटने की वजह भी" works precisely because the clause turns the sentence back on itself. What must never happen is a sentence that reports an event and does nothing else.

    WORKED EXAMPLES — real precaps from this platform, in four different builds. Study the architecture and the idiom, never the content. The names and events in them belong to other stories and must never appear in yours:

    1. TWO POSITIONS, ONE COLLISION. Neither lead has met the other yet. Nothing is revealed; the whole pull is two certainties about to break against each other:
    "अरमान ने तय कर लिया था कि अब कोई लड़की उसकी जिंदगी में जगह नहीं बनाएगी और कायनात को यकीन था कि कोई आदमी उसे झुका नहीं सकता। लेकिन जब वो दोनों टकराएंगे तो होगा किसका घमंड चूर चूर?"

    2. THE COST NAMED TWICE. One object, one decision, and a close that offers two outcomes the listener is already afraid of:
    "अपनी माँ से जुड़े जिस सच को कायनात वर्षों से खोज रही है, जल्द ही उसकी एक अनमोल निशानी उसके हाथ लगने वाली है। लेकिन उस अमानत तक पहुँचने से पहले ही अरमान एक ऐसा फैसला लेगा, जिसका अंजाम वह खुद भी नहीं जानता।

    क्या उसकी यह भूल कायनात से सिर्फ उसकी आखिरी उम्मीद छीनेगी, या उन दोनों के बीच शुरू हो रहे रिश्ते को भी खत्म कर देगी?"

    3. THE THING THEY DO NOT KNOW. The reader is put ahead of the character, and the danger is named as a person inside his own house:
    "सोमहिल में ओया अकेली जंगल की ओर निकल जाती है। उसे ढूँढ़ने के लिए सारांश भी उसके पीछे जाता है, लेकिन वह नहीं जानता कि जंगल में खतरा ओया का नहीं, उसका इंतजार कर रहा है। उसके अपने परिवार का कोई सदस्य चाहता है कि सारांश इस बार जीवित वापस न लौटे।

    आखिर अपने ही घर में उसका दुश्मन कौन है?"

    4. THE PILE-UP. Backstory stacked in one breath, then cut by a short question about the one person who was missing:
    "छह साल की कायनात ने एक ही रात अपनी माँ की जलती चिता देखी, अपना घर राख होते देखा और फिर ऐसी जगह पहुँची, जहाँ उसके मासूम शरीर की कीमत लगाई जाने वाली थी।

    वह बच्ची अकेले सब सहती रही, लेकिन उस वक्त उसका पिता कहाँ था? जल्द मिलने वाला इस सवाल का जवाब कायनात की पूरी जिंदगी हिला देगा।"

    What to take from all four: every one sets something up before it turns, every one hangs on a thing or a person the listener can picture, and not one of them merely reports what is going to happen. Note also that the closes differ — किसका…?, या…?, कौन…?, and a flat statement — and that the last two do not use मगर or जल्द ही at the turn at all.
    """
