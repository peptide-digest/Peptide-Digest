"""LLM for summarization of scientific articles related to computational peptides."""

# Add imports here
from . import article_processing
from . import clean_text
from . import article_db
from . import model_prompts

# Add functions here
from .article_db import create_database
from .article_db import get_article
from .article_db import get_articles
from .article_db import check_article_exists
from .article_db import delete_article
from .article_db import insert_article
from .article_db import update_article

from .article_processing import process_scidir_article
from .article_processing import process_multiple_scidir_articles
from .article_processing import process_pmc_article
from .article_processing import process_multiple_pmc_articles

from .model_prompts import summarize_article_segments
from .model_prompts import summarize_article_meta
from .model_prompts import score_texts_peptide_research

from ._version import __version__

