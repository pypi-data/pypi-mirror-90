from excel2meta_interface.utils import messages, helpers

from inspect import currentframe
from datetime import datetime
from glob import glob
from os import path, makedirs
import json
import csv

class JSON2EDCLineageFiles:
    code_version = "0.1.0"
    start_time = datetime.now()
    start_time_formatted = start_time.isoformat(timespec="microseconds").replace(":", "-")
    edc_lineage_column_header = [
        "Association",
        "From Connection",
        "To Connection",
        "From Object",
        "To Object",
    ]

    def __init__(self, configuration_file="resources/json2edc_config.json"):
        self.configuration_file = configuration_file
        self.result = messages.message["ok"]
        self.schema_directory = "schemas"
        self.json_directory = "jsons"
        self.output_directory = "out/"
        self.get_settings(configuration_file=configuration_file)
        self.helper = helpers.UtilsHelper()
        self.nr_entity_associations = 0
        self.nr_attribute_associations = 0

    def process_files(self):
        module = __name__ + "." + currentframe().f_code.co_name

        number_of_files = 0
        overall_result = messages.message["ok"]
        for file in glob(self.json_directory + "*.json"):
            number_of_files +=1
            data = self.helper.get_json(file)
            check_result = self.helper.check_schema(base_schema_folder=self.schema_directory, data=data)
            if check_result["code"] != "OK":
                file_result = check_result
                overall_result = file_result
            else:
                file_result = self.process_json_data(data)
                if file_result["code"] != "OK":
                    overall_result = file_result

            # register the outcome of the current file
            self.register_result(file, file_result)

        if overall_result["code"] == "OK":
            overall_result["info"] = \
                "#files processed: >%d<. #entity assocations: >%d<. #attribute assocications: >%d<" \
                % (number_of_files, self.nr_entity_associations, self.nr_attribute_associations)

        return overall_result

    def get_settings(self, configuration_file):
        try:
            with open(configuration_file) as config:
                data = json.load(config)
                self.schema_directory = data["schema_directory"]
                self.json_directory = data["json_directory"]
                self.output_directory = data["output_directory"]
        except FileNotFoundError or IOError as e:
            result = messages.message["main_config_not_found"]
            result["info"] = "configuration file used: >%s<" % configuration_file
            return result

    def process_json_data(self, data):
        result = messages.message["ok"]
        if data["meta"] == "physical_entity_association":
            self.nr_entity_associations += 1
            result = self.generate_dataset_lineage_entry(data)
        elif data["meta"] == "physical_attribute_association":
            self.nr_attribute_associations += 1
            result = self.generate_attribute_lineage_entry(data)

        return result

    def generate_dataset_lineage_entry(self, data):
        result = messages.message["ok"]

        for source_target_entity_link in data["source_target_entity_links"]:
            src = source_target_entity_link["from"]
            tgt = source_target_entity_link["to"]
            src_dataset = self.get_dataset(uuid=src)
            if src_dataset is None:
                result = messages.message["entity_uuid_not_found"]
                result["info"] = "source uuid: %s" % src
                return result
            tgt_dataset = self.get_dataset(uuid=tgt)
            if tgt_dataset is None:
                result = messages.message["entity_uuid_not_found"]
                result["info"] = "target uuid: %s" % src
                return result
            item = self.create_dataset_item(source_name=src_dataset["name"], target_name=tgt_dataset["name"])
            self.write_lineage_entry(item)

        return result

    def get_dataset(self, uuid):
        for file in glob(self.json_directory + "*.json"):
            with open(file) as f:
                data = json.load(f)
                if "meta" not in data:
                    continue
                meta = data["meta"]
                if meta == "physical_entity":
                    if data["uid"] == uuid:
                        return data
        return None

    def create_dataset_item(self, source_name, target_name):
        # get info from REF files, generated out of the Excel by excel2references
        src_ref = self.get_dataset_ref("source", source_name)
        if src_ref is None:
            src_path = "NONE://" + source_name
        else:
            src_edc_datasource = src_ref["src_zone"].split("/", 4)[2]
            src_path = src_edc_datasource + "://" + src_ref["src_zone"] + "/" + source_name
        tgt_ref = self.get_dataset_ref("target", target_name)
        if tgt_ref is None:
            tgt_path = "NONE://" + target_name
        else:
            tgt_edc_datasource = tgt_ref["tgt_zone"].split("/", 4)[2]
            tgt_path = tgt_edc_datasource + "://" + tgt_ref["tgt_zone"]  + "/" + target_name

        item = ["core.DataSetDataFlow", "", "", src_path, tgt_path]
        return item

    def get_dataset_ref(self, src_or_tgt, dataset_name):
        file = self.find_latest_ref_file(src_or_tgt)
        if file is None:
            print("Could not find a REF file for >%s<" % src_or_tgt)
            return None
        # print("Using ref file:", file)
        data = None
        with open(file, "r") as the_file:
            data = json.load(the_file)
        if src_or_tgt == "source":
            for source in data:
                if source["dataset"] == dataset_name:
                    return source
        elif src_or_tgt == "target":
            for entry in data:
                if entry["dataset"] == dataset_name:
                    return entry
        else:
            print("Incorrect src_or_tgt:", src_or_tgt)
        return None

    def find_latest_ref_file(self, src_or_tgt):
        search_for_files = self.output_directory + "20*--REF_-_data-sources-" + src_or_tgt + "*dataset.json"
        # print("Looking for REF files with search >%s<" % search_for_files)
        list_of_files = glob(search_for_files)
        if list_of_files is not None:
            latest_file = max(list_of_files, key=path.getctime)
        else:
            latest_file = None
        return latest_file

    def generate_attribute_lineage_entry(self, data):
        result = messages.message["ok"]

        return result

    def write_lineage_entry(self, entry):
        filename = self.output_directory + "lineage-" + self.start_time_formatted + ".csv"
        if path.exists(filename):
            append_or_write = "a"
            write_header = False
        else:
            append_or_write = "w"
            write_header = True

        with open(filename, append_or_write) as out:
            col_writer = csv.writer(out)
            if write_header:
                col_writer.writerow(self.edc_lineage_column_header)
            col_writer.writerow(entry)

    def register_result(self, file, result):
        filename = self.output_directory + self.start_time_formatted + "-" + __name__ + "-results.txt"
        if path.exists(filename):
            append_or_write = "a"
        else:
            append_or_write = "w"
        with open(filename, append_or_write) as out:
            out.write(file + ": " + json.dumps(result) + "\n")
