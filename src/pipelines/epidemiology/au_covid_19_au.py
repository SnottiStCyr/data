from typing import Any, Dict, List
from pandas import DataFrame, concat, merge
from lib.time import datetime_isoformat
from lib.utils import grouped_diff
from .pipeline import EpidemiologyPipeline


class Covid19AuPipeline(EpidemiologyPipeline):
    data_urls: List[str] = [
        'https://raw.github.com/covid-19-au/covid-19-au.github.io/prod/src/data/state.json'
    ]

    def parse_dataframes(self, dataframes: List[DataFrame], **parse_opts):
        data = dataframes[0].transpose()

        # Transform the data from non-tabulated format to record format
        records = []
        for idx, row in data.iterrows():
            for code in data.columns:
                subset = row[code]
                record = {
                    'date': idx.date().isoformat(),
                    'country_code': 'AU',
                    'subregion_1_code': code,
                    'confirmed': subset[0],
                }
                if len(subset) > 1:
                    record['deceased'] = subset[1]
                if len(subset) > 2:
                    record['recovered'] = subset[2]
                if len(subset) > 3:
                    record['tested'] = subset[3]
                records.append(record)

        data = DataFrame.from_records(records)
        return grouped_diff(data, ['country_code', 'subregion_1_code', 'date'])
