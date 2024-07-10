import csv
import os

DATA_FILE = os.path.join(os.environ.get("DATA_PATH", "../data"), "jugadores.csv")


def _file_reader() -> list[str]:
    file = open(DATA_FILE)
    reader = csv.reader(file, delimiter = ',')

    return reader

def _object_from_row(header: list[str], row: list[str]) -> dict[str, str]:
    return {header[i].lower(): row[i] for i in range(len(header))}

def _row_from_object(header: list[str], row: dict[str, str]) -> list[str]:
    return [row[key.lower()] for key in header]


def get_all_players() -> list[dict[str, str]]:
    reader = _file_reader()

    header = next(reader)
    return list(map(lambda row: _object_from_row(header, row), reader))

