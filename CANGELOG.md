v. 0.9.13
''''''''''

- Create directory if dose not exists when writing file.

v. 0.9.12
''''''''''

- fix parsers not have been initialized

v. 0.9.11
''''''''''

- fix incorrect reading requirements.txt

v. 0.9.10
''''''''''

Now we can use alternative parser classes to parse links

Default class parsers.re_parser.Parser
Alternative class parsers.lxml_parser.Parser. Required to install lxml and cssselect packages
You can set Your alternative Parser class, inherited from parsers.base.BaseParser

v. 0.9.8
''''''''

- new **exlude_urls** parameter for pysitemap.crowler
- Crawler. **exclude_urls** parameter.
    System checks for current url not contains each substring from exclude_urls.
    Default value is empty list
- Crawler. **set_exclude_url** method.

v. 0.9.2
''''''''

-  todo queue and done list backends
-  created very slowest sqlite backend for todo queue and done lists (1000 url writing for 3 minutes)
-  tests for sqlite_todo backend

v. 0.9.1
''''''''

-  extended readme
-  docstrings and code commentaries

v. 0.9.0
''''''''

-  since this version package supports only python version >=3.7
-  all functions recreated but api saved. If You use this package, then
   just update it, install requirements and run process
-  all requests works asynchronously

Version 0.5.1

Fixed:
    - UnicodeEncodeError: 'ascii' codec can't encode character