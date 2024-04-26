Generating Summaries
====================

ScienceDirect
-------------

Let's start with a ScienceDirect article. 


API Key
~~~~~~~

To scrape from ScienceDirect, it is necessary to have an API Key. This can be obtained by creating 
an account on the `ScienceDirect website <https://dev.elsevier.com/>`_ and requesting an API Key. 
The API Key is then used to authenticate the user and access the ScienceDirect database.


Process Specific article
~~~~~~~~~~~~~~~~~~~~~~~~

The following code snippet demonstrates how to scrape a ScienceDirect article using the API Key and one 
of the article identifiers: DOI, PII, or URL. To retrieve the article from the database, 
the function :func:`peptidedigest.get_article` is used with the article's DOI.

.. tab-set-code::

    .. code-block:: python

        import peptidedigest as pd

        api_key = 'your_api_key'
        article_doi = '10.1074/jbc.M117.805499'

        # Generate model output and save article information and output to the database
        pd.process_scidir_article("path/articles_database", tokenizer, model, api_key, doi=article_doi)

        article = pd.get_article("path/articles_database", article_doi)

    .. code-block:: python

        import peptidedigest as pd

        api_key = 'your_api_key'
        url = 'https://www.sciencedirect.com/science/article/pii/S0021925820403904'
        doi = '10.1074/jbc.M117.805499'

        # Generate model output and save article information and output to the database
        pd.process_scidir_article("path/articles_database", tokenizer, model, api_key, url=url)

        article = pd.get_article("path/articles_database", doi)

    .. code-block:: python

        import peptidedigest as pd

        api_key = 'your_api_key'
        pii = 'S0021925820403904'
        doi = '10.1074/jbc.M117.805499'

        # Generate model output and save article information and output to the database
        pd.process_scidir_article("path/articles_database", tokenizer, model, api_key, pii=pii)

        article = pd.get_article("path/articles_database", doi)

    .. code-block:: output 

        {'title': 'Computational antimicrobial peptide design and evaluation against multidrug-resistant clinical isolates of bacteria',
        'authors': 'Deepesh Nagarajan, Tushar Nagarajan, Natasha Roy, Omkar Kulkarni, Sathyabaarathi Ravichandran, Madhulika Mishra, Dipshikha Chakravortty, Nagasuma Chandra',
        'journal': 'antibiotic resistance, antimicrobial peptide (AMP), computational biology, drug design, drug resistance, LSTM',
        'publisher': 'by The American Society for Biochemistry and Molecular Biology, Inc.',
        'date': '2018-03-11',
        'url': 'https://www.sciencedirect.com/science/article/pii/S0021925820403904',
        'doi': '10.1074/jbc.M117.805499',
        'keywords': 'antibiotic resistance, antimicrobial peptide (AMP), computational biology, drug design, drug resistance, LSTM',
        'scidir/pmc': 'scidir',
        'pmc_id': None,
        'bullet_points': '- The LSTM model effectively decipherED the grammar underlying antimicrobial sequences and designed 2 effective antimicrobial peptidess...
        'summary': 'The text describes the design and efficacy of antimicrobial peptides generated using an LSTM language model. The model successfully deciphered...
        .
        .
        .
        }

Process Multiple Articles 
~~~~~~~~~~~~~~~~~~~~~~~~~

Let's search for some interesting articles on ScienceDirect about cancer to process. First, we need to
use the ``ScienceScraper`` package to search for articles. The ``search_scidir`` function searches 
for articles and results a list of DOIs that we can use. 

.. tab-set-code::

    .. code-block:: python

        import sciencescraper as ss

        query = 'cancer' 
        api_key = 'your_api_key'

        # Search for articles on ScienceDirect
        search_results = ss.search_scidir(api_key, query, max_results=10, offset=0)

    .. code-block:: output

        ['10.1016/j.jncc.2023.11.004',
        '10.1016/j.ebiom.2024.104991',
        '10.1016/j.radmp.2024.02.003',
        '10.1016/j.jncc.2023.07.005',
        '10.1016/j.lana.2024.100690',
        '10.1016/j.annonc.2024.02.008',
        '10.1016/j.jncc.2023.12.001',
        '10.1016/j.canep.2023.102481',
        '10.1053/j.gastro.2024.04.014',
        '10.1016/j.tranon.2023.101709']


We can specify the number of results that are returned using the ``max_results`` parameter. The maximum number of results
that can be returned at once is 100. To see the results after the first 100, you can use the ``offset`` parameter and start from
101 to get the next 100 results.


Now to process the articles that were found, let's use the :func:`peptidedigest.process_multiple_scidir_articles` function.

.. tab-set-code::

    .. code-block:: python

        pd.process_multiple_scidir_articles("path/articles_database", tokenizer, model, api_key, dois=search_results, chunk_size=4200)


This function will process all the articles in the list of DOIs and save the information and output to the database, so it might 
take some time to complete. The ``chunk_size`` parameter specifies the number of words to split the article full text into.
We recommend **4200** as a good value for this parameter.

To see all of the articles that were processed, you can use the :func:`peptidedigest.get_articles` function.

.. tab-set-code::

    .. code-block:: python

        articles = pd.get_articles("path/articles_database")


PMC
---

PMC articles can be processed in a similar way to ScienceDirect articles. The only difference is that PMC articles do not require an API Key to access the database.

Process Specific article
~~~~~~~~~~~~~~~~~~~~~~~~

The function to use for processing a PMC article is :func:`peptidedigest.process_pmc_article`. This function requires the article's PMC ID to retrieve the article from the database.


.. tab-set-code::

    .. code-block:: python

        import peptidedigest as pd

        pmc_id = "PMC8185074"

        # Generate model output and save article information and output to the database
        pd.process_pmc_article("path/articles_database", tokenizer, model, pmc_id)

        article = pd.get_article("path/articles_database", pmc_id)


Process Multiple Articles
~~~~~~~~~~~~~~~~~~~~~~~~~

To search for articles on PMC, we can use the ``search_pmc`` function from the ``sciencescraper`` package. This function returns a list of PMC IDs that can be used to process the articles.

.. tab-set-code::

    .. code-block:: python

        import sciencescraper as ss

        query = 'cancer'

        # Search for articles on PMC
        search_results = ss.search_pmc(query, retmax=5, retstart=0)


``retmax`` specifies the number of results to return, and ``retstart`` specifies the starting index for the search results. 

Now to process the articles that were found, let's use the :func:`peptidedigest.process_multiple_pmc_articles` function.

.. tab-set-code::

    .. code-block:: python

        pd.process_multiple_pmc_articles("path/articles_database", tokenizer, model, pmc_ids=search_results, chunk_size=4200)

This function will process all the articles in the list of PMC IDs and save the information and output to the database, so it might take some time to complete. The ``chunk_size`` parameter specifies the number of words to split the article full text into.

To see all of the articles that were processed, you can use the :func:`peptidedigest.get_articles` function.

.. tab-set-code::

    .. code-block:: python

        articles = pd.get_articles("path/articles_database")