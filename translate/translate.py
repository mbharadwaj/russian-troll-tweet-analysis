import logging
import time
from os import listdir, mkdir
from os.path import join, isfile, exists

SOURCE_DIR = "../categorized"

# each tweet is 140 char * 100 chunk = 14000 char
# google api limits 1,000,000 per 100 seconds
SLEEP = 14

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class Translate(object):

    def __init__(self, translation_api, source_dir, target_dir, source_language, account_category, chunk_size):
        self.translation_api = translation_api
        self.source_dir = source_dir
        self.target_dir = target_dir
        self.source_language = source_language
        self.account_category = account_category
        self.chunk_size = chunk_size

    def get_files_to_translate(self):
        """
        get CSV files from source directory
        :return: names of files that match the source language and account cateogry
        """
        return [join(self.source_dir, f) for f in listdir(self.source_dir) if
                isfile(join(self.source_dir, f)) and f.startswith(self.source_language) and self.account_category in f]

    def invoke_translate_api_and_save_results(self, source_filename):

        """
        source fils if read, and split to chunks.
        if a chunk has not been processed before, it will be passed to the translate API wrapper
        the results from this are saved

        chunking allows for the translation process to continue from where it left off. it also enables to work
        within the API limits (daily, bulk etc)

        :param source_filename: name of the source that is to be translated
        :return: nothing
        """
        if not exists(self.target_dir):
            mkdir(self.target_dir)

        with open(source_filename) as file:
            logger.debug("processing %s", source_filename)
            lines = file.readlines()
            chunks = [lines[x:x + self.chunk_size] for x in range(0, len(lines), self.chunk_size)]
            logger.debug("%s: chunk size=%s" % (source_filename, self.chunk_size))
            number_of_chunks = len(chunks)
            logger.debug("%s: split %s lines in %s chunks" % (source_filename, len(lines), number_of_chunks))

            for index, chunk in enumerate(chunks):
                chunk_number = index + 1

                translated_filename = source_filename.replace(SOURCE_DIR, self.target_dir) + "." + str(chunk_number)
                translated_full_result_filename = translated_filename + ".full"

                # process if chunk has not been translated before
                if not exists(translated_filename):
                    logger.debug("%s: processing chunk %s of %s..." % (source_filename, chunk_number, number_of_chunks))
                    translations = self.translation_api.translate(chunk, target_language="en")
                    self.save_translated_file(translations, translated_filename, translated_full_result_filename)
                    time.sleep(SLEEP)
                else:
                    logger.debug("%s: skipping chunk %s of %s as it exists..." % (
                    source_filename, chunk_number, number_of_chunks))

    def save_translated_file(self, translations, translated_filename, translated_full_result_filename):
        """

        :param translations: translations list to save
        :param translated_filename: file name to save just the translations
        :param translated_full_result_filename: file to save whole translation payload from API
        :return:
        """
        with open(translated_filename, 'w') as file:
            payload = self.translation_api.build_translation_to_save(translations)
            file.write(payload)

        with open(translated_full_result_filename, 'w') as file:
            payload = self.translation_api.build_translations_response_to_save(translations)
            file.write(payload)

    def translate_and_save(self):
        filenames = self.get_files_to_translate()
        for source_filename in filenames:
            self.invoke_translate_api_and_save_results(source_filename)

            time.sleep(SLEEP)
