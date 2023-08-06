Commandline Interface (CLI)
===========================

Srtools provides a commandline utility for transliterating Serbian text from 
Cyrillic to Latin and vice versa.

The utility operates on ``STDIN`` and outputs to ``STDOUT`` if no arguments are 
provided.
You can also explicitly specify you're reading from ``STDIN`` in the standard 
way (``srts -cl --``).

You *must* provide either ``--cl`` (Cyrillic → Latin) or ``--lc`` (Latin → 
Cyrillic) to specify the transliteration direction.

The utility currently only supports UTF-8 input and output.
I might include commandline options for picking an encoding like YUSCII (JUS 
I.B1.002), Cyrillic YUSCII (JUS_I.B1.003-serb), Windows-1250, Windows-1251, 
ISO-8859-5, ISO/IEC 8859-2 in the future.
Until then, you may pipe the input and output into ``iconv``.

.. argparse::
   :filename: ../bin/srts
   :func: create_parser
   :prog: srts
   :nodefault:
   :nodescription:
