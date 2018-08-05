import json
import logging

import boto3

from translate import SOURCE_DIR, Translate

TARGET_DIR = "aws_translated"

# AWS limit is 5000 char per call
# 140 char per tweet * 30 = 4200
CHUNK_SIZE_FOR_AWS_TRANSLATE_API = 30

# AWS limits per time window?
SLEEP = 14

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class AWSTranslate(object):

    def __init__(self):
        self.translate_client = boto3.client(service_name='translate', use_ssl=True)

    def translate(self, values, target_language="en", source_language=None):
        if not source_language:
            source_language = "auto"

        translations = []
        for text in values:
            translated = self.translate_client.translate_text(Text=text,
                                                              SourceLanguageCode=source_language,
                                                              TargetLanguageCode=target_language)
            translations.append(translated)

        return translations

    def build_translation_to_save(self, translations):
        return "\n".join([t['TranslatedText'] for t in translations])

    def build_translations_response_to_save(self, translations):
        return "\n".join([json.dumps(t) for t in translations])


if __name__ == '__main__':
    translate_obj = Translate(AWSTranslate(),
                              SOURCE_DIR,
                              TARGET_DIR,
                              "Spanish",
                              "NonEnglish",
                              CHUNK_SIZE_FOR_AWS_TRANSLATE_API)
    translate_obj.translate_and_save()

"""
AWS supports the following languages
https://docs.aws.amazon.com/translate/latest/dg/what-is.html

Arabic
Chinese (Simplified)
Chinese (Traditional)
Czech
French
German
Italian
Japanese
Portuguese
Russian
Spanish
Turkish

"""
