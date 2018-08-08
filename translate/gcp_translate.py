import json
import logging

from google.cloud import translate

from translate import SOURCE_DIR, Translate

TARGET_DIR = "../gcp_translated"
CHUNK_SIZE_FOR_GCP_TRANSLATE_API = 100

# each tweet is 140 char * 100 chunk = 14000 char
# google api limits 1,000,000 per 100 seconds
SLEEP = 14

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class GoogleTranslate(object):

    def __init__(self):
        self.translate_client = translate.Client()

    def translate(self, values, target_language="en", source_language=None):
        if not source_language:
            return self.translate_client.translate(values, target_language=target_language)
        else:
            return self.translate_client.translate(values,
                                                   target_language=target_language,
                                                   source_language=source_language)

    def build_translation_to_save(self, translations):
        return "\n".join([t['translatedText'] for t in translations])

    def build_translations_response_to_save(self, translations):
        return "\n".join([json.dumps(t) for t in translations])


if __name__ == '__main__':
    google_translate = GoogleTranslate()
    translate_obj = Translate(google_translate,
                              SOURCE_DIR,
                              TARGET_DIR,
                              "Spanish",
                              "NonEnglish",
                              CHUNK_SIZE_FOR_GCP_TRANSLATE_API)
    translate_obj.translate_and_save()

"""

GCP Translate supports the following languages

def list_languages():
    translate_client = translate.Client()

    results = translate_client.get_languages()

    for language in results:
        print(u'{name} ({language})'.format(**language))

Afrikaans (af)
Albanian (sq)
Amharic (am)
Arabic (ar)
Armenian (hy)
Azerbaijani (az)
Basque (eu)
Belarusian (be)
Bengali (bn)
Bosnian (bs)
Bulgarian (bg)
Catalan (ca)
Cebuano (ceb)
Chichewa (ny)
Chinese (Simplified) (zh)
Chinese (Traditional) (zh-TW)
Corsican (co)
Croatian (hr)
Czech (cs)
Danish (da)
Dutch (nl)
English (en)
Esperanto (eo)
Estonian (et)
Filipino (tl)
Finnish (fi)
French (fr)
Frisian (fy)
Galician (gl)
Georgian (ka)
German (de)
Greek (el)
Gujarati (gu)
Haitian Creole (ht)
Hausa (ha)
Hawaiian (haw)
Hebrew (iw)
Hindi (hi)
Hmong (hmn)
Hungarian (hu)
Icelandic (is)
Igbo (ig)
Indonesian (id)
Irish (ga)
Italian (it)
Japanese (ja)
Javanese (jw)
Kannada (kn)
Kazakh (kk)
Khmer (km)
Korean (ko)
Kurdish (Kurmanji) (ku)
Kyrgyz (ky)
Lao (lo)
Latin (la)
Latvian (lv)
Lithuanian (lt)
Luxembourgish (lb)
Macedonian (mk)
Malagasy (mg)
Malay (ms)
Malayalam (ml)
Maltese (mt)
Maori (mi)
Marathi (mr)
Mongolian (mn)
Myanmar (Burmese) (my)
Nepali (ne)
Norwegian (no)
Pashto (ps)
Persian (fa)
Polish (pl)
Portuguese (pt)
Punjabi (pa)
Romanian (ro)
Russian (ru)
Samoan (sm)
Scots Gaelic (gd)
Serbian (sr)
Sesotho (st)
Shona (sn)
Sindhi (sd)
Sinhala (si)
Slovak (sk)
Slovenian (sl)
Somali (so)
Spanish (es)
Sundanese (su)
Swahili (sw)
Swedish (sv)
Tajik (tg)
Tamil (ta)
Telugu (te)
Thai (th)
Turkish (tr)
Ukrainian (uk)
Urdu (ur)
Uzbek (uz)
Vietnamese (vi)
Welsh (cy)
Xhosa (xh)
Yiddish (yi)
Yoruba (yo)
Zulu (zu)
"""
