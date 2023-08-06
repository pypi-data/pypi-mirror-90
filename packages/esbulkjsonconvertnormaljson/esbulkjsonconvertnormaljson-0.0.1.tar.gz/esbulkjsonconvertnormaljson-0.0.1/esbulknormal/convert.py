import json


class ConvertFile:
    def convert_file(self, bulk_file):
        bulk_file_name = bulk_file.split(".")
        normal_file = bulk_file_name[0] + 'normal' + '.' + bulk_file_name[1]
        with open(bulk_file, "r") as es_file:
            lines = es_file.readlines()
        with open(normal_file, "w") as es_file:
            for line_number, line in enumerate(lines):
                if (line_number % 2 != 0):
                    es_file.write(line)
