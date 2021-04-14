import json
import argparse
import pandas as pd
from pathlib import Path
from src.utils import get_logger
from src.artsob import Artsob, ArtsobRecords
from src.ebird import EBirdRecord, Ebird

logger = get_logger(__name__)


def convert():
    # Parse the args
    parser = argparse.ArgumentParser()
    parser.add_argument("artsob_file", help="Your Artsob Excel or CSV record file")
    parser.add_argument("--format", help="csv or excel. Default is excel")
    args = parser.parse_args()

    if not args.artsob_file:
        print("You must specify the path of your Artsob excel or csv file")
        exit(1)

    if args.format is None:
        file_format = "excel"
    else:
        file_format = "csv"

    # the files
    artsob_file = Path() / args.artsob_file
    data_dir = Path() / "data"
    species_file = data_dir / "ebird-species-list.json"
    ebird_output_file = "ebird_observations.xlsx"

    species = parse_species_file(species_file)
    artsob_data = get_artsob_records(artsob_file, file_format)
    artsob_records = ArtsobRecords(artsob_data)

    # get a list of all translated ebird records
    # i.e. translate artsob to ebird
    ebird_records = [EBirdRecord(species, record) for record in artsob_records.records]

    # build initial dataframe
    ebird_excel = {}
    for heading in Ebird.headings:
        ebird_excel[heading] = []

    valid_ebird_records = [record for record in ebird_records if record.valid]

    for record in valid_ebird_records:
        for field, item in record.fields.items():
            ebird_excel[field].append(item)

    # write ebird_excel to file
    pandas_output = pd.DataFrame(ebird_excel)
    pandas_output.to_excel(ebird_output_file, index=False)
    print(f"Successfully created {ebird_output_file} from {artsob_file.name}")


def parse_species_file(file):
    species = {}
    with open(file) as json_file:
        data = json.load(json_file)
    for item in data:
        species[item["sciName"]] = item
    return species


def get_artsob_records(file, file_format):
    try:
        logger.info(f"Attempting to open {file_format} {file}")
        unique_ids = set()
        records = []
        if file_format == "csv":
            df = pd.read_csv(file)  # delimiter=";"
        else:
            df = pd.read_excel(file, dtype=str)

        for index, record in df.iterrows():
            artsob_record = Artsob(record)
            if artsob_record.id not in unique_ids:
                records.append(artsob_record)
                unique_ids.add(artsob_record.id)
            else:
                logger.error(
                    f"Duplicate Artsob record ID already imported: {artsob_record.id}. Ignoring this entry"
                )
        return records
    except FileNotFoundError:
        print(f"Artsob file {file} was not found. Please specify the correct file")
        exit(1)
    except pd.errors.ParserError:
        print(
            f"Couldn't read {file} as there was a problem reading its data. If this is a CSV, ensure that Excel as exported it as semi-colon separated. That is, using an ';' to seperate the data."
        )
        exit(1)
    # except ValueError:
    #     print(f"File {file} not recognised as a valid {file_format} file. Exiting")
    #     exit(1)


if __name__ == "__main__":
    convert()
