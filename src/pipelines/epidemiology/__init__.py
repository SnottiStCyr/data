from pandas import DataFrame

from lib.utils import combine_tables, output_table
from lib.default_pipeline import DefaultPipeline

from .pipeline import EpidemiologyPipeline
from .au_covid_19_au import Covid19AuPipeline
from .br_covid19_brazil_timeseries import Covid19BrazilTimeseriesPipeline
from .ca_authority import CanadaPipeline
from .ch_openzh import OpenZHPipeline
from .de_covid_19_germany_gae import Covid19GermanyPipeline
from .es_authority import ISCIIIPipeline
from .es_datadista import DatadistaPipeline
from .fr_france_covid_19 import FranceCovid19Pipeline
from .id_catchmeup import CatchmeupPipeline
from .xx_dxy import DXYPipeline
from .xx_ecdc import ECDCPipeline
from .xx_wikipedia import WikipediaPipeline


def run(aux: DataFrame, **pipeline_opts) -> DataFrame:
    wiki_base_url = 'https://en.wikipedia.org/wiki/Template:2019–20_coronavirus_pandemic_data'

    # Define a chain of pipeline-options tuples
    pipeline_chain = [
        # Data sources for all level 1
        (ECDCPipeline(), {}),

        # Data sources for ES levels 1 and 2
        # (DatadistaPipeline(), {}),
        (ISCIIIPipeline(), {}),

        # Data sources for AR level 2
        (WikipediaPipeline('{}/Argentina_medical_cases'.format(wiki_base_url)),
         {'parse_opts': {'date_format': '%d %b', 'country': 'AR', 'skiprows': 1, 'cumsum': True}}),

        # Data sources for AU level 2
        (Covid19AuPipeline(), {}),
        (WikipediaPipeline('{}/Australia_medical_cases'.format(wiki_base_url)),
         {'parse_opts': {'date_format': '%d %B', 'country': 'AU', 'cumsum': True}}),

        # Data sources for BO level 2
        (WikipediaPipeline('{}/Bolivia_medical_cases'.format(wiki_base_url)),
         {'parse_opts': {'date_format': '%b %d', 'country': 'BO', 'skiprows': 1, 'droprows': 'Date(2020)'}}),

        # Data sources for BR level 2
         (Covid19BrazilTimeseriesPipeline(), {}),

        # Data sources for CA level 2
        (CanadaPipeline(), {}),

        # Data sources for CH level 2
        (OpenZHPipeline(), {}),

        # Data sources for CL level 2
        (WikipediaPipeline('{}/Chile_medical_cases'.format(wiki_base_url)),
         {'parse_opts': {'date_format': '%Y-%m-%d', 'country': 'CL', 'skiprows': 1}}),

        # Data sources for CN level 2
        (DXYPipeline(), {'parse_opts': {'country_name': 'China'}}),

        # Data sources for DE level 2
        (Covid19GermanyPipeline(), {}),

        # Data sources for FR level 2
        # (WikipediaPipeline('{}/France_medical_cases'.format(wiki_base_url)),
        #  {'parse_opts': {'date_format': '%Y-%m-%d', 'country': 'FR', 'skiprows': 1}}),
        (FranceCovid19Pipeline(), {}),

        # Data sources for ID level 2
        (CatchmeupPipeline(), {}),

        # Data sources for IN level 2
        (WikipediaPipeline('https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_India'),
         {'parse_opts': {'date_format': '%b-%d', 'country': 'IN', 'skiprows': 1}}),

        # Data sources for JP level 2
        (WikipediaPipeline('{}/Japan_medical_cases'.format(wiki_base_url)),
         {'parse_opts': {'date_format': '%Y/%m/%d', 'country': 'JP', 'skiprows': 2}}),

        # Data sources for KR level 2
        (WikipediaPipeline('{}/South_Korea_medical_cases'.format(wiki_base_url)),
         {'parse_opts': {'date_format': '%Y-%m-%d', 'country': 'KR', 'skiprows': 1}}),

        # Data sources for MY level 2
        (WikipediaPipeline('https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Malaysia'),
         {'parse_opts': {'date_format': '%d/%m', 'country': 'MY', 'cumsum': True, 'drop_column': 'deceased'}}),

        # Data sources for PE level 2
        (WikipediaPipeline('https://es.wikipedia.org/wiki/Pandemia_de_enfermedad_por_coronavirus_de_2020_en_Per%C3%BA'),
         {'parse_opts': {'date_format': '%d de %B', 'country': 'PE', 'locale': 'es_ES', 'skiprows': 1}}),

        # Data sources for PK level 2
        (WikipediaPipeline('{}/Pakistan_medical_cases'.format(wiki_base_url)),
         {'parse_opts': {'date_format': '%b %d', 'country': 'PK', 'skiprows': 1, 'cumsum': True}}),

        # Data sources for RU level 2
        (WikipediaPipeline('{}/Russia_medical_cases'.format(wiki_base_url)),
         {'parse_opts': {'date_format': '%d %b', 'country': 'RU', 'skiprows': 1}}),

    ]

    # Get all the pipeline outputs
    # TODO: parallelize this operation (but keep ordering)
    pipeline_data = [
        pipeline.run(aux, **{**opts, **pipeline_opts}) for pipeline, opts in pipeline_chain
    ]

    # Combine all pipeline outputs into a single DataFrame
    data = combine_tables(pipeline_data, ['date', 'key'])

    # Return data using the pipeline's output parameters
    return output_table(EpidemiologyPipeline.schema, data)
