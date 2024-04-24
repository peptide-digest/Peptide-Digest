PeptideDigest
==============================
[//]: # (Badges)
[![GitHub Actions Build Status](https://github.com/peptide-digest/PeptideDigest/workflows/CI/badge.svg)](https://github.com/peptide-digest/PeptideDigest/actions?query=workflow%3ACI)
[![codecov](https://codecov.io/gh/peptide-digest/PeptideDigest/branch/main/graph/badge.svg)](https://codecov.io/gh/peptide-digest/PeptideDigest/branch/main)


PeptideDigest is a Python package for interacting with a Gemma model from Google that has been customized to summarize and extract metadata from scientific publications related to computational peptide research. 


## Features

- Summarize scientific publications into bullet points as well as paragraph form
- Extract metadata from scientific publications related to computational peptide research
- Give a score and a justification for this score to each publication based on its relevance to computational peptide research 
- Save results to a SQLite database and retrieve them later

## Installation

You can install PeptideDigest using pip. Make sure you have cloned the repository and are in the root directory of the project. Then, run the following command:

```bash
pip install -e .
```

This will install the package in editable mode, so you can make changes to the code and see the changes reflected in the package.

### Copyright

Copyright (c) 2024, Joshua Blomgren, Elizabeth Gilson, Jeffrey Jacob


#### Acknowledgements
 
Project based on the 
[Computational Molecular Science Python Cookiecutter](https://github.com/molssi/cookiecutter-cms) version 1.1.
