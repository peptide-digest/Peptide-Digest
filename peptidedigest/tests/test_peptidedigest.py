"""
Unit and regression test for the peptidedigest package.
"""

# Import package, test suite, and other packages as needed
import sys

import pytest

import peptidedigest

import os
import sqlite3


def test_peptidedigest_imported():
    """Sample test, will always pass so long as import statement worked."""
    assert "peptidedigest" in sys.modules

# Constants for testing
TEST_DB_NAME = "test_database"

@pytest.fixture(scope="module")
def test_database():
    create_database(TEST_DB_NAME)
    yield TEST_DB_NAME
    os.remove(TEST_DB_NAME + ".db")

def test_create_database():
    assert os.path.exists(TEST_DB_NAME + ".db")

def test_insert_article(test_database):
    article_info = {
        "title": "Test Article",
        "authors": ["Author1", "Author2"],
        "journal": "Test Journal",
        "publisher": "Test Publisher",
        "date": "2024-04-23",
        "url": "http://test.com",
        "doi": "test_doi",
        "keywords": ["Keyword1", "Keyword2"],
        "scidir/pmc": "TestPMC",
    }
    
    insert_article(test_database, article_info, model_responses)
    retrieved_article = get_article(test_database, "test_doi")
    assert retrieved_article == {
        **article_info,
    }

def test_update_article(test_database):
    article_info = {
        "title": "Test Article",
        "authors": ["Author1", "Author2"],
        "journal": "Test Journal",
        "publisher": "Test Publisher",
        "date": "2024-04-23",
        "url": "http://test.com",
        "doi": "test_doi",
        "keywords": ["Keyword1", "Keyword2"],
        "scidir/pmc": "TestPMC",
    }
   
    insert_article(test_database, article_info)
    update_article(test_database, "test_doi", model_responses)
    retrieved_article = get_article(test_database, "test_doi")
    assert retrieved_article == {
        **article_info,
    }

def test_get_article_nonexistent(test_database):
    with pytest.raises(FileNotFoundError):
        get_article(test_database, "nonexistent_doi")

def test_get_article_invalid_database():
    with pytest.raises(FileNotFoundError):
        get_article("nonexistent_database", "test_doi")

def test_get_articles(test_database):
    articles = get_articles(test_database)
    assert isinstance(articles, list)

def test_get_articles_invalid_database():
    with pytest.raises(FileNotFoundError):
        get_articles("nonexistent_database")
