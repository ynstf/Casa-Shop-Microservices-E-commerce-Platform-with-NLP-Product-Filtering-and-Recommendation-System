import translators as ts

def translate_text(text, source_lang='auto', target_lang='en'):
    try:
        translation = ts.translate_text(text, translator="bing", from_language='auto' ,to_language=target_lang)
    except:
        translation = text
    return translation

