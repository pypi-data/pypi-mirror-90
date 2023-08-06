Perform SOAP, REST and UI / Feature tests


Installation
============
You can download and install the latest version of this software from the Python package index (PyPI) as follows::

    pip install --upgrade testly

Usage
=====
    python -m testly --help=

    python -m testly --command <command> [Options]
or

`python -m artify -c <command> [Options]`

**Params**

Available commands  &nbsp; &nbsp; &nbsp; &nbsp; http

Test HTTP URL
=============

     python -m testly -c http -h <your_host>

**Params**

-h, --host &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; The Http host that you desire to test.

**Optional Params**

--proxy &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp;  Sets Http proxy

--proxysec  &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Sets Https proxy