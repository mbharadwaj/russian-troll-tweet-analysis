import csv
from os import listdir
from os.path import join, isfile

categories = ['Commercial', 'Featmonger', 'HashtagGamer', 'NewsFeed', 'LeftTroll', 'RightTroll', 'Unknown']

class Prep(object):
    def __init__(self, source_dir, source_language, target_dir, number_of_samples):
        self.number_of_samples = number_of_samples
        self.target_dir = target_dir
        self.source_language = source_language
        self.source_dir = source_dir

    def get_categorized_files(self):
        return [join(self.source_dir, file) for file in listdir(self.source_dir) if
                isfile(join(self.source_dir, file)) and self.meets_criteria(file)]

    def meets_criteria(self, file):
        parts = file.split("_")
        return parts[0] == self.source_language and parts[2] in categories

    def prep(self):
        files = self.get_categorized_files()
        target_filename = join(self.target_dir, "training_data.csv")

        category_samples = {}
        for file in files:
            parts = file.split("_")
            category = parts[2]
            category_samples.setdefault(category, [])
            with open(file, "r") as input_file:
                readlines = input_file.readlines()
                category_samples[category].extend(readlines[:self.number_of_samples * 2])


        with open(target_filename, 'w', newline='') as csvfile:
            fieldnames = ['text', 'label']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            rows = []
            for category, samples in category_samples.items():
                for sample in list(set(samples))[:self.number_of_samples]:
                    rows.append({"text": sample.strip(), "label": category})

            writer.writerows(rows)


if __name__ == '__main__':
    prep = Prep("categorized", "English", "cloud_ml", 250)
    prep.prep()