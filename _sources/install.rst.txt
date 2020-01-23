Installation
============

To install ``pubmed_parser``, you can install directly from the repository as follows

.. code-block:: bash
    
    pip install git+git://github.com/titipata/pubmed_parser.git


or clone the repository and install using ``pip``

.. code-block:: bash

    git clone https://github.com/titipata/pubmed_parser
    pip install ./pubmed_parser


You can test your installation by running 

.. code-block:: bash

    pytest --cov=pubmed_parser tests/ --verbose


To build a documentation page, change directory to ``docs`` folder and then run


.. code-block:: bash

    make html


This will build a page in ``_build/html`` which you can open via regular browser.
You need ``sphinx`` and ``sphinx-gallery`` to build a documentation page.