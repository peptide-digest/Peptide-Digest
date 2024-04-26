SQLite database
================

The database is a SQLite database with the following schema:

.. image:: ../_static/schema.png 
    :align: center


The database stores the article information, the model output, and has consists of tables pertaining to 
specific metadata. The DOI of an article is used to link the tables together, as the DOI is unique to each article.

Creating the database
---------------------

The database is created using the :func:`peptidedigest.create_database` function.

This function takes in the path to the database file and creates a new database at that location.
It will not overwrite an existing database, so if you want to create a new database, you will need to use a new file path or name.

.. tab-set-code::

    .. code-block:: python

        db_path = "path/to/article_database.db"
        pd.create_database(db_path)

This will create a new database called ``article_database.db`` at the specified path.


Retrieving an article from the database
---------------------------------------

To retrieve an article from the database, you can use the :func:`peptidedigest.get_article` function.

.. tab-set-code::

    .. code-block:: python

        doi = "10.1074/jbc.M117.805499"
        article = pd.get_article(database, doi=doi, pmc_id=None)


And to retrieve all of them, you can use the :func:`peptidedigest.get_articles` function.

.. tab-set-code::

    .. code-block:: python

        articles = pd.get_articles(database)



Deleting articles from the database
-----------------------------------

To delete an article from the database, you can use the :func:`peptidedigest.delete_article` function.

.. tab-set-code::

    .. code-block:: python

        doi = "10.1074/jbc.M117.805499"
        pd.delete_article(database, doi=doi, pmc_id=None):