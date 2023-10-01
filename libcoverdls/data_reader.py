import json

import ijson  # type: ignore


class DataReader:
    """Class to hold information on where to get data and provides methods to access it.

    This is then passed around to any code that wants access to data.

    This is done so that later we can add a get_iterator() function here
    that returns statements in a memory efficient way and code that can use
    an iterator (like Python Checks) can call get_iterator() and not get_all_data()
    """

    def __init__(
        self,
        filename,
        sample_mode=False,
        sample_mode_max_row_count=50,
    ):
        self._filename = filename
        self._sample_mode = sample_mode
        self._sample_mode_max_row_count = sample_mode_max_row_count

    def get_all_data(self):
        # Which mode?
        if self._sample_mode:

            # Sample Mode
            sample_data = []
            count = 0

            with open(self._filename, "rb") as fp:
                for statement in ijson.items(fp, "datasets.item"):
                    sample_data.append(statement)
                    count += 1
                    if not count < self._sample_mode_max_row_count:
                        break

            return sample_data

        else:

            # Full Mode
            with open(self._filename) as fp:
                json_data = json.load(fp)
                if "datasets" in json_data:
                    return json_data["datasets"]
                else:
                    return None
