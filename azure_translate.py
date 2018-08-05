import logging
import http.client, urllib.parse, uuid, json
import os

from translate import SOURCE_DIR, Translate

TARGET_DIR = "azure_translated"

# AWS limit is 5000 char per call
# 140 char per tweet * 30 = 4200
CHUNK_SIZE_FOR_AZURE_TRANSLATE_API = 30

# AWS limits per time window?
SLEEP = 14

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

azure_key = os.getenv("AZURE_KEY")
host = 'api.cognitive.microsofttranslator.com'
path = '/translate?api-version=3.0'

class AzureTranslate(object):

    def __init__(self):
        return

    def translate_one(self, text, target_language):

        requestBody = [{
            'Text': text,
        }]

        params = "&to=%s" % target_language

        content = json.dumps(requestBody, ensure_ascii=False).encode('utf-8')

        headers = {
            'Ocp-Apim-Subscription-Key': azure_key,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        conn = http.client.HTTPSConnection(host)
        conn.request("POST", path + params, content, headers)
        response = conn.getresponse()
        result = response.read()
        return result

        # Note: We convert result, which is JSON, to and from an object so we can pretty-print it.
        # We want to avoid escaping any Unicode characters that result contains. See:
        # https://stackoverflow.com/questions/18337407/saving-utf-8-texts-in-json-dumps-as-utf8-not-as-u-escape-sequence
        #return json.dumps(json.loads(result), indent=4, ensure_ascii=False)


    def translate(self, values, target_language="en", source_language=None):

        translations = []
        for text in values:
            translated = self.translate_one(text, target_language)
            translations.append(translated)

        return translations

    def build_translation_to_save(self, translations):
        return "\n".join([self.process_translation(t) for t in translations])

    def process_translation(self, translation):
        return json.loads(translation)[0]['translations'][0]['text']

    def build_translations_response_to_save(self, translations):
        return "\n".join([json.dumps(json.loads(t)) for t in translations])

if __name__ == '__main__':
    translate_obj = Translate(AzureTranslate(),
                              SOURCE_DIR,
                              TARGET_DIR,
                              "Spanish",
                              "NonEnglish",
                              CHUNK_SIZE_FOR_AZURE_TRANSLATE_API)
    translate_obj.translate_and_save()

"""
Azure supports the following languages

"""
