from googletrans import Translator


lang_dict = {
    'Hindi': 'hi',
    'Bengali': 'bn'
}


async def trans(sentence, lang):
    translator = Translator()
    try:
        translated = await translator.translate(sentence, dest=lang_dict[lang])
    except Exception:
        return sentence
    return translated.text
