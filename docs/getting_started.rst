Getting Started
===============

This page details how to get started with PeptideDigest. PeptideDigest is a Python package that
prompts an LLM to summarize scientific articles related to computational peptide research and extract 
relevant metadata. 

Installation
------------

To install PeptideDigest, you will need to be in an environment with:

* Python 3.9 or higher.

To install PeptideDigest, first clone the repository from GitHub:

.. tab-set-code::

    .. code-block:: shell
        
        git clone https://github.com/peptide-digest/PeptideDigest


Next, let's install the package onto your system. Navigate to the root directory of the repository and run the following command:

.. tab-set-code::

    .. code-block:: shell

        pip install -e .

This will install the package in editable mode, meaning that you can make changes to the package and see the changes reflected in your environment without having to reinstall the package.
Installation is now complete!


Initializing the LLM
--------------------

To use PeptideDigest, you will first need access to the large language model and GPU resources. 

If the LLM is downloaded locally, you simply need the path to the model. 


.. tab-set-code::

    .. code-block:: python

        from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
        import torch

        model_path = "path/to/model"
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForCausalLM.from_pretrained(model_path, config=BitsAndBytesConfig())
        model = model.to("cuda")

.. note::

    The Torch and Transformers libraries are required to use the LLM. Please make sure that your version of Torch is compabitle with CUDA. 
    Take a look at the `Pytorch website <https://pytorch.org/get-started/locally/>`_ for more information on how to install Pytorch with CUDA support.

