#######
srtools
#######

.. image:: https://gitlab.com/andrejr/srtools/badges/master/pipeline.svg
   :alt: pipeline status
   :target: https://gitlab.com/andrejr/srtools/pipelines
.. image:: https://gitlab.com/andrejr/srtools/badges/master/coverage.svg
   :alt: coverage report
   :target: https://andrejr.gitlab.io/srtools/coverage/index.html

Srtools provides a CLI utility (``srts``) and a Python 3 (``^3.7``) package 
that helps you transliterate Serbian texts between Cyrillic and Latin.

Here's a demonstration of the CLI utility:

.. code-block:: console

   $ echo "Đače, uštedu plaćaj žaljenjem zbog džinovskih cifara." | srts --lc
   Ђаче, уштеду плаћај жаљењем због џиновских цифара.
   $ echo "Ђаче, уштеду плаћај жаљењем због џиновских цифара." | srts --cl
   Đače, uštedu plaćaj žaljenjem zbog džinovskih cifara.

Here's how you use the Python package:

.. code-block:: python

   from srtools import cyrillic_to_latin, latin_to_cyrillic

   assert (
       latin_to_cyrillic("Đače, uštedu plaćaj žaljenjem zbog džinovskih cifara.")
       == "Ђаче, уштеду плаћај жаљењем због џиновских цифара."
   )

   assert (
       cyrillic_to_latin("Ђаче, уштеду плаћај жаљењем због џиновских цифара.")
       == "Đače, uštedu plaćaj žaljenjem zbog džinovskih cifara."
   )


Motivation
==========

I needed a simple commandline utility I can use to pipe in some text and change
its script.

I also use this tool to transliterate strings in Serbian LaTeX localization 
packages. That way I don't have to maintain individual sets of localization 
strings for Cyrillic and Latin.

Documentation
=============

Documentation (Sphinx) can be viewed on
`GitLab pages for this package <https://andrejr.gitlab.io/srtools/>`_.

Changelog
=========

The changelog can be found within the documentation, 
`here <https://andrejr.gitlab.io/srtools/changes.html>`_.
