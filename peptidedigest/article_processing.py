"""
Functions to process and analyze articles using the model.
"""

import sciencedirect as scraper

from .article_db import insert_article
from .model_prompts import (
    summarize_article_segments,
    summarize_article_meta,
    score_texts_peptide_research,
)
from .clean_text import (
    split_into_chunks,
    extract_metadata,
)


def process_scidir_article(
    database, tokenizer, model, api_key, doi=None, pii=None, url=None, chunk_size=4200
):
    """
    Process a ScienceDirect article, summarize the article using the model, and store the information in the database.

    Parameters
    ----------
    database : str
        The database to store the processed article information.
    tokenizer : transformers.PreTrainedTokenizer
        The tokenizer to use for the model.
    model : transformers.PreTrainedModel
        The model to use to process the article.
    api_key : str
        The API key for the ScienceDirect API. API keys can be obtained by creating an account at https://dev.elsevier.com/.
    doi : str, optional
        The DOI of the article to be processed.
    pii : str, optional
        The PII of the article to be processed.
    url : str, optional
        The URL of the article to be processed.
    chunk_size : int, optional
        The size of the chunks to split the full text into. Default is 4200.

    Returns
    -------
    None
        The processed article information is stored in the database.

    """
    article_info = scraper.get_scidir_article_info(
        api_key, doi=doi, pii=pii, url=url, chunk_size=chunk_size
    )
    article_info["scidir/pmc"] = "scidir"

    # Check if the article has an abstract
    if article_info["abstract"] == "Abstract not found in article.":
        abstract_discussion = article_info["full_text"]

    else:
        abstract_discussion = (
            article_info["abstract"]
            + " "
            + str(article_info["keywords"])
            + " "
            + article_info["methods"]
            + " "
            + article_info["discussion"]
        )
        abstract_discussion = split_into_chunks(abstract_discussion, chunk_size)

    bullet_points, summary = summarize_article_segments(
        abstract_discussion, tokenizer, model
    )
    metadata = summarize_article_meta(abstract_discussion, tokenizer, model)
    extracted_data = extract_metadata(metadata)
    score_justification, score_range, score = score_texts_peptide_research(
        abstract_discussion, summary, bullet_points, metadata, tokenizer, model
    )

    model_output = {
        "summary": summary,
        "bullet_points": bullet_points,
        "metadata": metadata,
        "peptides": extracted_data["peptides"],
        "proteins": extracted_data["proteins"],
        "domains": extracted_data["domains"],
        "chemistry": extracted_data["chemistry"],
        "biology": extracted_data["biology"],
        "computational_methods": extracted_data["computational_methods"],
        "score": score,
        "score_justification": score_justification,
    }

    insert_article(database, article_info, model_output)


def process_multiple_scidir_articles(
    database,
    tokenizer,
    model,
    api_key,
    dois=None,
    piis=None,
    urls=None,
    chunk_size=4200,
):
    """
    Process multiple ScienceDirect articles, summarize the articles using the model, and store the information in the database.

    Parameters
    ----------
    database : str
        The database to store the processed articles information.
    tokenizer : transformers.PreTrainedTokenizer
        The tokenizer to use for the model.
    model : transformers.PreTrainedModel
        The model to use to process the articles.
    api_key : str
        The API key for the ScienceDirect API. API keys can be obtained by creating an account at https://dev.elsevier.com/.
    dois : list of str, optional
        The DOIs of the articles to be processed.
    piis : list of str, optional
        The PIIs of the articles to be processed.
    urls : list of str, optional
        The URLs of the articles to be processed.
    chunk_size : int, optional
        The size of the chunks to split the full text into. Default is 4200.

    Returns
    -------
    None
        The processed articles information is stored in the database.

    """
    for doi in dois:
        process_scidir_article(
            database, tokenizer, model, api_key, doi=doi, chunk_size=chunk_size
        )

    for pii in piis:
        process_scidir_article(
            database, tokenizer, model, api_key, pii=pii, chunk_size=chunk_size
        )

    for url in urls:
        process_scidir_article(
            database, tokenizer, model, api_key, url=url, chunk_size=chunk_size
        )


def process_pmc_article(database, tokenizer, model, pmc_id, chunk_size=4200):
    """
    Process a PubMed Central article, summarize the article using the model, and store the information in the database.

    Parameters
    ----------
    database : str
        The database to store the processed article information.
    tokenizer : transformers.PreTrainedTokenizer
        The tokenizer to use for the model.
    model : transformers.PreTrainedModel
        The model to use to process the article.
    pmc_id : str
        The PMC ID of the article to be processed.
    chunk_size : int, optional
        The size of the chunks to split the full text into. Default is 4200.

    Returns
    -------
    None
        The processed article information is stored in the database.

    """
    article_info = scraper.get_pmc_article_info(pmc_id, chunk_size=chunk_size)
    article_info["scidir/pmc"] = "pmc"

    if (
        article_info["abstract"] == ""
        or article_info["methods"] == ""
        or article_info["discussion"] == ""
    ):
        model_input = article_info["full_text"]

    else:
        abstract_discussion = (
            article_info["abstract"]
            + " "
            + str(article_info["keywords"])
            + " "
            + article_info["methods"]
            + " "
            + article_info["discussion"]
        )
        model_input = split_into_chunks(abstract_discussion, chunk_size)

    bullet_points, summary = summarize_article_segments(model_input, tokenizer, model)
    metadata = summarize_article_meta(model_input, tokenizer, model)
    extracted_data = extract_metadata(metadata)
    score_justification, score_range, score = score_texts_peptide_research(
        model_input, summary, bullet_points, metadata, tokenizer, model
    )

    model_output = {
        "model_summary": summary,
        "model_bullet_points": bullet_points,
        "model_metadata": metadata,
        "peptides": extracted_data["peptides"],
        "proteins": extracted_data["proteins"],
        "domains": extracted_data["domains"],
        "chemistry": extracted_data["chemistry"],
        "biology": extracted_data["biology"],
        "computational_methods": extracted_data["computational_methods"],
        "model_score": score,
        "model_score_justification": score_justification,
    }

    insert_article(database, article_info, model_output)


def process_multiple_pmc_articles(database, tokenizer, model, pmc_ids, chunk_size=4200):
    """
    Process multiple PubMed Central articles, summarize the articles using the model, and store the information in the database.

    Parameters
    ----------
    database : str
        The database to store the processed articles information.
    tokenizer : transformers.PreTrainedTokenizer
        The tokenizer to use for the model.
    model : transformers.PreTrainedModel
        The model to use to process the articles.
    pmc_ids : list of str
        The PMC IDs of the articles to be processed.
    chunk_size : int, optional
        The size of the chunks to split the full text into. Default is 4200.

    Returns
    -------
    None
        The processed articles information is stored in the database.

    """
    for pmc_id in pmc_ids:
        process_pmc_article(database, tokenizer, model, pmc_id, chunk_size=chunk_size)
