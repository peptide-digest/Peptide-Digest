"""
Functions to clean text data.
"""

import re


def split_into_chunks(text, chunk_size):
    """
    Splits a given text into chunks of approximately 'chunk_size' words.

    Parameters
    ----------
    text : str
        The text to split into chunks.
    chunk_size : int
        The approximate number of words to include in each chunk.

    Returns
    -------
    chunks : list of str
        A list of text chunks, each containing approximately 'chunk_size' words.
    """
    words = text.split()  # Split the text into words
    chunks = [
        " ".join(words[i : i + chunk_size]) for i in range(0, len(words), chunk_size)
    ]
    return chunks


def clean_summary(text):
    """
    Cleans a summary text by removing unwanted patterns and phrases.

    Parameters
    ----------
    text : str
        The summary text to clean.

    Returns
    -------
    cleaned_text : str
        The cleaned summary text.
    """
    # Extended patterns and exact phrases to remove
    patterns = [
        r"Sure, here is a summary of the provided text in \d+ sentences:",
        r"Sure, here is a \d+-sentence summary of the portion of the scientific article you provided:",
        r"Sure, here is a summary of the scientific article in \d+ sentences:",
        r"## Summary of the Scientific Article in \d+ Sentences",
        r"Sure, here is a \d+-sentence summary of the provided text:",
        r"Sure. Here is the summary in bullet form:",
        r"Sure, here is a summary of the text in \d+ sentences",
        r"Here is a summary of the text in \d+ sentences:",
        r"Sure, here is a summary of the text you provided in a single paragraph:",
    ]

    # Remove patterns and exact phrases
    for pattern in patterns:
        if "## Summary of the Scientific Article in 5 Sentences" in text:
            text = text.replace(
                "## Summary of the Scientific Article in 5 Sentences", ""
            ).strip()
        else:
            text = re.sub(pattern, "", text, flags=re.IGNORECASE).strip()

    return text


import re

def extract_metadata(metadata_text):
    """
    Extract peptides, proteins, domains of interest, chemistry discussed,
    biology discussed, and computational methods discussed from the model metadata text.

    Parameters
    ----------
    metadata_text : str
        The model metadata text to be parsed.

    Returns
    -------
    dict
        A dictionary containing the extracted metadata as lists.
    """
    metadata_dict = {
        "peptides": None,
        "proteins": None,
        "domains": None,
        "chemistry": None,
        "biology": None,
        "computational_methods": None
    }

    # Extract peptides
    peptides_match = re.search(
        r"\*\*Peptides discussed:\*\*\n(.*?)(\n\n|\Z)", metadata_text, re.S
    )
    if peptides_match:
        peptides_text = peptides_match.group(1).strip()
        if all(keyword not in peptides_text.lower() for keyword in ["not", "any", "n/a", "none", "null"]):
            peptides_list = [p.strip() for p in peptides_text.split("\n- ")]
            metadata_dict["peptides"] = peptides_list
            metadata_dict["peptides"][0] = metadata_dict["peptides"][0].lstrip("- ")

    # Extract proteins/targets
    proteins_match = re.search(
        r"\*\*Proteins/targets discussed:\*\*\n(.*?)(\n\n|\Z)", metadata_text, re.S
    )
    if proteins_match:
        proteins_text = proteins_match.group(1).strip()
        if all(keyword not in proteins_text.lower() for keyword in ["not", "any", "n/a", "none", "null"]):
            proteins_list = [p.strip() for p in proteins_text.split("\n- ")]
            metadata_dict["proteins"] = proteins_list
            metadata_dict["proteins"][0] = metadata_dict["proteins"][0].lstrip("- ")

    # Extract domains of interest
    domains_match = re.search(
        r"\*\*Domains of interest:\*\*\n(.*?)(\n\n|\Z)", metadata_text, re.S
    )
    if domains_match:
        domains = domains_match.group(1).strip()
        if all(keyword not in domains.lower() for keyword in ["not", "any", "n/a", "none", "null"]):
            domains_list = [d.strip() for d in domains.split("\n- ")]
            metadata_dict["domains"] = domains_list
            metadata_dict["domains"][0] = metadata_dict["domains"][0].lstrip("- ")

    # Extract chemistry discussed
    chemistry_match = re.search(
        r"\*\*Chemical matter/chemistry discussed:\*\*\n(.*?)(\n\n|\Z)", metadata_text, re.S
    )
    if chemistry_match:
        chemistry = chemistry_match.group(1).strip()
        if all(keyword not in chemistry.lower() for keyword in ["not", "any", "n/a", "none", "null"]):
            chemistry_list = [c.strip() for c in chemistry.split("\n- ")]
            metadata_dict["chemistry"] = chemistry_list
            metadata_dict["chemistry"][0] = metadata_dict["chemistry"][0].lstrip("- ")

    # Extract biology discussed
    biology_match = re.search(
        r"\*\*Biological matter/biology discussed:\*\*\n(.*?)(\n\n|\Z)", metadata_text, re.S
    )
    if biology_match:
        biology = biology_match.group(1).strip()
        if all(keyword not in biology.lower() for keyword in ["not", "any", "n/a", "none", "null"]):
            biology_list = [b.strip() for b in biology.split("\n- ")]
            metadata_dict["biology"] = biology_list
            metadata_dict["biology"][0] = metadata_dict["biology"][0].lstrip("- ")

    # Extract computational methods discussed
    computational_match = re.search(
        r"\*\*Computational methods:\*\*\n(.*?)(\n\n|\Z)", metadata_text, re.S
    )
    if computational_match:
        computational = computational_match.group(1).strip()
        if all(keyword not in computational.lower() for keyword in ["not", "any", "n/a", "none", "null"]):
            computational_list = [c.strip() for c in computational.split("\n- ")]
            metadata_dict["computational_methods"] = computational_list
            metadata_dict["computational_methods"][0] = metadata_dict["computational_methods"][0].lstrip("- ")

    return metadata_dict
