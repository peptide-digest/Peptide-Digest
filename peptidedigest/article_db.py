"""
Functions for creating and managing a SQLite database for storing articles and their model responses.
"""

import sqlite3
import os

def create_database(name):
    """
    Create a SQLite database with the given name.

    Parameters
    ----------
    name : str
        The name of the database to create.

    Returns
    -------
    None
        The database is created in the current working directory.
    """
    database = name + ".db"
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS article_info (
                    id INTEGER PRIMARY KEY,
                    title TEXT,
                    authors TEXT,
                    journal TEXT,
                    publisher TEXT,
                    date DATE,
                    url TEXT UNIQUE,
                    doi TEXT UNIQUE,
                    keywords TEXT,
                    scidir_pmc TEXT,
                    pmc_id TEXT UNIQUE
                )""")

    c.execute("""CREATE TABLE IF NOT EXISTS model_responses (
                    id INTEGER PRIMARY KEY,
                    doi TEXT UNIQUE,
                    bullet_points TEXT,
                    summary TEXT,
                    metadata TEXT,
                    score REAL,
                    score_justification TEXT,
                    FOREIGN KEY(doi) REFERENCES article_info(doi)
                )""")

    c.execute("""CREATE TABLE IF NOT EXISTS peptides (
                    id INTEGER PRIMARY KEY,
                    doi TEXT,
                    peptide TEXT,
                    FOREIGN KEY(doi) REFERENCES article_info(doi)
                )""")

    c.execute("""CREATE TABLE IF NOT EXISTS proteins (
                    id INTEGER PRIMARY KEY,
                    doi TEXT,
                    protein TEXT,
                    FOREIGN KEY(doi) REFERENCES article_info(doi)
                )""")

    c.execute("""CREATE TABLE IF NOT EXISTS domains (
                    id INTEGER PRIMARY KEY,
                    doi TEXT,
                    domain TEXT,
                    FOREIGN KEY(doi) REFERENCES article_info(doi)
                )""")

    c.execute("""CREATE TABLE IF NOT EXISTS chemistry_topics (
                    id INTEGER PRIMARY KEY,
                    doi TEXT,
                    chemistry TEXT,
                    FOREIGN KEY(doi) REFERENCES article_info(doi)
                )""")

    c.execute("""CREATE TABLE IF NOT EXISTS biology_topics (
                    id INTEGER PRIMARY KEY,
                    doi TEXT,
                    biology TEXT,
                    FOREIGN KEY(doi) REFERENCES article_info(doi)
                )""")

    c.execute("""CREATE TABLE IF NOT EXISTS computational_methods (
                    id INTEGER PRIMARY KEY,
                    doi TEXT,
                    computational_method TEXT,
                    FOREIGN KEY(doi) REFERENCES article_info(doi)
                )""")

    conn.commit()
    conn.close()


def insert_article(database, article_info, model_responses=None):
    """
    Insert an article and its model responses into the database.

    Parameters
    ----------
    database : str
        The name of the database to insert the article into.
    article_info : dict
        A dictionary containing the article information.
    model_responses : dict
        A dictionary containing the model responses for the article.

    Returns
    -------
    None
        The article and model responses are inserted into the database.
    """
    database = database + ".db"

    # check if the database exists
    if not os.path.exists(database):
        raise FileNotFoundError(f"Database {database} does not exist.")

    conn = sqlite3.connect(database)
    c = conn.cursor()

    # Insert article information
    c.execute(
        """INSERT OR IGNORE INTO article_info (title, authors, journal, publisher, date, url, doi, keywords, scidir_pmc, pmc_id)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            article_info["title"],
            ", ".join(article_info["authors"]),
            ", ".join(article_info["keywords"]),
            article_info["publisher"],
            article_info["date"],
            article_info["url"],
            article_info["doi"],
            ", ".join(article_info["keywords"]),
            article_info["scidir/pmc"],
            article_info["pmc_id"]
        ),
    )

    # Insert model responses
    if model_responses is None:
        conn.commit()
        conn.close()
        return

    c.execute(
        """INSERT OR IGNORE INTO model_responses (doi, bullet_points, summary, metadata, score, score_justification) 
                 VALUES (?, ?, ?, ?, ?, ?)""",
        (
            article_info["doi"],
            model_responses["bullet_points"],
            model_responses["summary"],
            model_responses["metadata"],
            model_responses["score"],
            model_responses["score_justification"],
        ),
    )

    # test

    for peptide in model_responses["peptides"]:
        c.execute(
            """INSERT OR IGNORE INTO peptides (doi, peptide) 
                 VALUES (?, ?)""",
            (
                article_info["doi"], 
                peptide
            )
        )

    for protein in model_responses["proteins"]:
        c.execute(
            """INSERT OR IGNORE INTO proteins (doi, protein) 
                 VALUES (?, ?)""",
            (
                article_info["doi"], 
                protein
            )
        )

    for domain in model_responses["domains"]:
        c.execute(
            """INSERT OR IGNORE INTO domains (doi, domain) 
                 VALUES (?, ?)""",
            (
                article_info["doi"], 
                domain
            )
        )

    for topic in model_responses["chemistry"]:
        c.execute(
            """INSERT OR IGNORE INTO chemistry_topics (doi, chemistry) 
                 VALUES (?, ?)""",
            (
                article_info["doi"], 
                topic
            )
        )

    for topic in model_responses["biology"]:
        c.execute(
            """INSERT OR IGNORE INTO biology_topics (doi, biology) 
                 VALUES (?, ?)""",
            (
                article_info["doi"], 
                topic
            )
        )

    for method in model_responses["computational_methods"]:
        c.execute(
            """INSERT OR IGNORE INTO computational_methods (doi, computational_method) 
                 VALUES (?, ?)""",
            (
                article_info["doi"], 
                method
            )
        )

    conn.commit()
    conn.close()


def get_article(database, doi= None, pmc_id=None):
    """
    Get the article information and model responses for a given DOI.

    Parameters
    ----------
    database : str
        The name of the database to retrieve the article from.
    doi : str
        The DOI of the article to retrieve.
    pmc_id : str
        The PMC ID of the article to retrieve.

    Returns
    -------
    dict
        A dictionary containing the article information and model responses.
    """
    if doi is None and pmc_id is None:
        raise ValueError("Either DOI or PMC ID must be provided.")
    
    if doi is not None and pmc_id is not None:
        raise ValueError("Only one of DOI or PMC ID should be provided.")
    
    if doi is not None:
        if not check_article_exists(database, doi, "doi"):
            raise ValueError(f"Article with DOI {doi} does not exist in the database.")
        
    if pmc_id is not None:
        if not check_article_exists(database, pmc_id, "pmc_id"):
            raise ValueError(f"Article with PMC ID {pmc_id} does not exist in the database.")
    
    database = database + ".db"
    conn = sqlite3.connect(database)
    c = conn.cursor()

    if doi is not None:
        c.execute(
            """SELECT * FROM article_info WHERE doi = ?""",
            (doi,),
        )
        article_info = c.fetchone()

        c.execute(
            """SELECT * FROM model_responses WHERE doi = ?""",
            (doi,),
        )
        model_responses = c.fetchone()

        c.execute(
            """SELECT peptide FROM peptides WHERE doi = ?""",
            (doi,),
        )
        peptides = c.fetchall()

        c.execute(
            """SELECT protein FROM proteins WHERE doi = ?""",
            (doi,),
        )
        proteins = c.fetchall()

        c.execute(
            """SELECT domain FROM domains WHERE doi = ?""",
            (doi,),
        )
        domains = c.fetchall()

        c.execute(
            """SELECT chemistry FROM chemistry_topics WHERE doi = ?""",
            (doi,),
        )
        chemistry_topics = c.fetchall()

        c.execute(
            """SELECT biology FROM biology_topics WHERE doi = ?""",
            (doi,),
        )
        biology_topics = c.fetchall()

        c.execute(
            """SELECT computational_method FROM computational_methods WHERE doi = ?""",
            (doi,),
        )
        computational_methods = c.fetchall()

        conn.close()
    
    elif pmc_id is not None:
        c.execute(
            """SELECT * FROM article_info WHERE pmc_id = ?""",
            (pmc_id,),
        )
        article_info = c.fetchone()

        c.execute(
            """SELECT * FROM model_responses WHERE doi = ?""",
            (pmc_id,),
        )
        model_responses = c.fetchone()

        c.execute(
            """SELECT peptide FROM peptides WHERE doi = ?""",
            (pmc_id,),
        )
        peptides = c.fetchall()

        c.execute(
            """SELECT protein FROM proteins WHERE doi = ?""",
            (pmc_id,),
        )
        proteins = c.fetchall()

        c.execute(
            """SELECT domain FROM domains WHERE doi = ?""",
            (pmc_id,),
        )
        domains = c.fetchall()

        c.execute(
            """SELECT chemistry FROM chemistry_topics WHERE doi = ?""",
            (pmc_id,),
        )
        chemistry_topics = c.fetchall()

        c.execute(
            """SELECT biology FROM biology_topics WHERE doi = ?""",
            (pmc_id,),
        )
        biology_topics = c.fetchall()

        c.execute(
            """SELECT computational_method FROM computational_methods WHERE doi = ?""",
            (pmc_id,),
        )
        computational_methods = c.fetchall()

        conn.close()

    article = {
        "title": article_info[1],
        "authors": article_info[2],
        "journal": article_info[3],
        "publisher": article_info[4],
        "date": article_info[5],
        "url": article_info[6],
        "doi": article_info[7],
        "keywords": article_info[8],
        "scidir/pmc": article_info[9],  
        "pmc_id": article_info[10],  
        "bullet_points": model_responses[2],
        "summary": model_responses[3],
        "metadata": model_responses[4],
        "score": model_responses[5],
        "score_justification": model_responses[6],
        "peptides": [peptide[0] for peptide in peptides],
        "proteins": [protein[0] for protein in proteins],
        "domains": [domain[0] for domain in domains],
        "chemistry_topics": [chemistry[0] for chemistry in chemistry_topics],
        "biology_topics": [biology[0] for biology in biology_topics],
        "computational_methods": [method[0] for method in computational_methods],
    }

    return article


def get_articles(database):
    """
    Get all articles from the database.

    Parameters
    ----------
    database : str
        The name of the database to retrieve the articles from.

    Returns
    -------
    list
        A list of dictionaries containing the article information and model responses.
    """
    database = database + ".db"

    # check if the database exists
    if not os.path.exists(database):
        raise FileNotFoundError(f"Database {database} does not exist.")
    
    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute(
        """SELECT * FROM article_info""",
    )
    articles = c.fetchall()

    articles_list = []
    for article in articles:
        c.execute(
            """SELECT * FROM model_responses WHERE doi = ?""",
            (article[7],),
        )
        model_responses = c.fetchone()

        c.execute(
            """SELECT peptide FROM peptides WHERE doi = ?""",
            (article[7],),
        )
        peptides = c.fetchall()

        c.execute(
            """SELECT protein FROM proteins WHERE doi = ?""",
            (article[7],),
        )
        proteins = c.fetchall()

        c.execute(
            """SELECT domain FROM domains WHERE doi = ?""",
            (article[7],),
        )
        domains = c.fetchall()

        c.execute(
            """SELECT chemistry FROM chemistry_topics WHERE doi = ?""",
            (article[7],),
        )
        chemistry_topics = c.fetchall()

        c.execute(
            """SELECT biology FROM biology_topics WHERE doi = ?""",
            (article[7],),
        )
        biology_topics = c.fetchall()

        c.execute(
            """SELECT computational_method FROM computational_methods WHERE doi = ?""",
            (article[7],),
        )
        computational_methods = c.fetchall()

        article_dict = {
            "title": article[1],
            "authors": article[2],
            "journal": article[3],
            "publisher": article[4],
            "date": article[5],
            "url": article[6],
            "doi": article[7],
            "keywords": article[8],
            "scidir/pmc": article[9],
            "pmc_id": article[10],
            "bullet_points": model_responses[2],
            "summary": model_responses[3],
            "metadata": model_responses[4],
            "score": model_responses[5],
            "score_justification": model_responses[6],
            "peptides": [peptide[0] for peptide in peptides],
            "proteins": [protein[0] for protein in proteins],
            "domains": [domain[0] for domain in domains],
            "chemistry_topics": [chemistry[0] for chemistry in chemistry_topics],
            "biology_topics": [biology[0] for biology in biology_topics],
            "computational_methods": [method[0] for method in computational_methods],
        }
        articles_list.append(article_dict)

    conn.close()
    return articles_list


def update_article(database, doi, model_responses):
    """
    Update the model responses for an article in the database.

    Parameters
    ----------
    database : str
        The name of the database to update the article in.
    doi : str
        The DOI of the article to update.
    model_responses : dict
        A dictionary containing the updated model responses.

    Returns
    -------
    None
        The model responses for the article are updated in the database.
    """
    database = database + ".db"

    # check if the database exists
    if not os.path.exists(database):
        raise FileNotFoundError(f"Database {database} does not exist.")
    
    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute(
        """UPDATE model_responses SET bullet_points = ?, summary = ?, metadata = ?, score = ?, score_justification = ? 
                 WHERE doi = ?""",
        (
            model_responses["bullet_points"],
            model_responses["summary"],
            model_responses["metadata"],
            model_responses["score"],
            model_responses["score_justification"],
            doi,
        ),
    )

    c.execute(
        """DELETE FROM peptides WHERE doi = ?""",
        (doi,),
    )
    for peptide in model_responses["peptides"]:
        c.execute(
            """INSERT OR IGNORE INTO peptides (doi, peptide) 
                 VALUES (?, ?)""",
            (
                doi,
                peptide
            )
        )

    c.execute(
        """DELETE FROM proteins WHERE doi = ?""",
        (doi,),
    )
    for protein in model_responses["proteins"]:
        c.execute(
            """INSERT OR IGNORE INTO proteins (doi, protein) 
                 VALUES (?, ?)""",
            (
                doi,
                protein
            )
        )

    c.execute(
        """DELETE FROM domains WHERE doi = ?""",
        (doi,),
    )
    for domain in model_responses["domains"]:
        c.execute(
            """INSERT OR IGNORE INTO domains (doi, domain) 
                 VALUES (?, ?)""",
            (
                doi,
                domain
            )
        )
    

    c.execute(
        """DELETE FROM chemistry_topics WHERE doi = ?""",
        (doi,),
    )
    for chemistry in model_responses["chemistry"]:
        c.execute(
            """INSERT OR IGNORE INTO chemistry_topics (doi, chemistry) 
                 VALUES (?, ?)""",
            (
                doi,
                chemistry
            )
        )

    c.execute(
        """DELETE FROM biology_topics WHERE doi = ?""",
        (doi,),
    )
    for biology in model_responses["biology"]:
        c.execute(
            """INSERT OR IGNORE INTO biology_topics (doi, biology) 
                 VALUES (?, ?)""",
            (
                doi,
                biology
            )
        )

    c.execute(
        """DELETE FROM computational_methods WHERE doi = ?""",
        (doi,),
    )
    for method in model_responses["computational_methods"]:
        c.execute(
            """INSERT OR IGNORE INTO computational_methods (doi, computational_method) 
                 VALUES (?, ?)""",
            (
                doi,
                method
            )
        )

    conn.commit()
    conn.close()


def check_article_exists(database, value, column):
    """
    Check if an article with the given value in the specified column exists in the database.

    Parameters
    ----------
    database : str
        The name of the database to check for the article.
    value : str
        The value to check for in the specified column.
    column : str
        The column to check for the value.

    Returns
    -------
    bool
        True if the article exists, False otherwise.
    """
    database = database + ".db"

    # check if the database exists
    if not os.path.exists(database):
        raise FileNotFoundError(f"Database {database} does not exist.")
    
    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute(
        f"""SELECT * FROM article_info WHERE {column} = ?""",
        (value,),
    )
    article = c.fetchone()

    conn.close()

    if article is not None:
        return True
    else:
        return False
    

def delete_article(database, doi=None, pmc_id=None):
    """
    Delete an article and its model responses from the database.

    Parameters
    ----------
    database : str
        The name of the database to delete the article from.
    doi : str
        The DOI of the article to delete.
    pmc_id : str
        The PMC ID of the article to delete.

    Returns
    -------
    None
        The article and model responses are deleted from the database.
    """
    database = database + ".db"

    # check if the database exists
    if not os.path.exists(database):
        raise FileNotFoundError(f"Database {database} does not exist.")
    
    conn = sqlite3.connect(database)
    c = conn.cursor()

    if doi is not None:
        c.execute(
            """DELETE FROM article_info WHERE doi = ?""",
            (doi,),
        )
        c.execute(
            """DELETE FROM model_responses WHERE doi = ?""",
            (doi,),
        )
        c.execute(
            """DELETE FROM peptides WHERE doi = ?""",
            (doi,),
        )
        c.execute(
            """DELETE FROM proteins WHERE doi = ?""",
            (doi,),
        )
        c.execute(
            """DELETE FROM domains WHERE doi = ?""",
            (doi,),
        )
        c.execute(
            """DELETE FROM chemistry_topics WHERE doi = ?""",
            (doi,),
        )
        c.execute(
            """DELETE FROM biology_topics WHERE doi = ?""",
            (doi,),
        )
        c.execute(
            """DELETE FROM computational_methods WHERE doi = ?""",
            (doi,),
        )

    if pmc_id is not None:
        c.execute(
            """DELETE FROM article_info WHERE pmc_id = ?""",
            (pmc_id,),
        )
        c.execute(
            """DELETE FROM model_responses WHERE doi = ?""",
            (pmc_id,),
        )
        c.execute(
            """DELETE FROM peptides WHERE doi = ?""",
            (pmc_id,),
        )
        c.execute(
            """DELETE FROM proteins WHERE doi = ?""",
            (pmc_id,),
        )
        c.execute(
            """DELETE FROM domains WHERE doi = ?""",
            (pmc_id,),
        )
        c.execute(
            """DELETE FROM chemistry_topics WHERE doi = ?""",
            (pmc_id,),
        )
        c.execute(
            """DELETE FROM biology_topics WHERE doi = ?""",
            (pmc_id,),
        )
        c.execute(
            """DELETE FROM computational_methods WHERE doi = ?""",
            (pmc_id,),
        )

    conn.commit()
    conn.close()