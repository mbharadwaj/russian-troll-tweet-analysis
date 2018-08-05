import csv
import logging
from os import listdir, mkdir
from os.path import isfile, join, exists

SOURCE_DIR = "russian-troll-tweets"
TARGET_DIR = "categorized"

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def get_csv_files(dirname):
    return [join(dirname, f) for f in listdir(dirname) if f.endswith(".csv") and isfile(join(dirname, f))]


def process_tweet_csv_files(filenames):
    tweets_by_category = {}

    for filename in filenames:
        with open(filename) as file:
            logger.debug("processing ", filename)
            reader = csv.DictReader(file)
            for row in reader:
                language = row['language']
                language = language.replace(" ", "-").replace("(", "-").replace(")", "-")
                category = "%s_%s_%s" % (language, row['account_type'], row['account_category'])
                tweets_by_category.setdefault(category, [])
                tweets_by_category[category].append(row["content"])

    return tweets_by_category


def save_categorized_tweets(tweets_by_category):
    for category, tweets in tweets_by_category.items():
        category_filename = join(TARGET_DIR, "%s_%s.txt" % (category, len(tweets)))
        with open(category_filename, 'w') as file:
            payload = "\n".join(tweets)
            file.write(payload)


if __name__ == '__main__':
    filenames = get_csv_files(SOURCE_DIR)
    if not exists(TARGET_DIR):
        mkdir(TARGET_DIR)
    tweets_by_category = process_tweet_csv_files(filenames)
    save_categorized_tweets(tweets_by_category)
