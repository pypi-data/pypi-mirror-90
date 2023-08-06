Developer Interface (API)
=========================

.. module:: srtools

.. role:: pycode(code)
    :language: python


Srtools provides both CLI functionality (``srts`` utility) and a Python package 
you can use from your own code.
The API intended for external use is documented in this file.

Transliteration functions
-------------------------

Two simple transliteration functions are provided by the package.

.. autofunction:: srtools.cyrillic_to_latin

.. autofunction:: srtools.latin_to_cyrillic


Translation tables and dictionaries
-----------------------------------

The dictionaries and :meth:`str.translate` translation tables used internally 
are also provided as a part of the public API.
You're unlikely to need these, since the mechanism for
transliteration provided in this package is decent enough for most uses.

.. autodata:: srtools.character_dictionaries.CYR_TO_LAT_DICT
   :annotation:

.. autodata:: srtools.character_dictionaries.CYR_TO_LAT_TTABLE
   :annotation:

.. autodata:: srtools.character_dictionaries.LAT_TO_CYR_DICT
   :annotation:

.. autodata:: srtools.character_dictionaries.LAT_TO_CYR_DIGRAPHS_DICT
   :annotation:

.. autodata:: srtools.character_dictionaries.LAT_TO_CYR_TTABLE
   :annotation:
