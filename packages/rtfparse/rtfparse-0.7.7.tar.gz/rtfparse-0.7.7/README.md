# rtfparse

RTF Parser. So far it can only de-encapsulate HTML content from an RTF, but it properly parses the RTF structure and allows you to write your own custom RTF renderers. The HTML de-encapsulator provided with `rtfparse` is just one such custom renderer which liberates the HTML content from its RTF encapsulation and saves it in a given html file.

# Dependencies

```
argcomplete
extract-msg
compressed_rtf
```

# Installation

Install rtfparse from your local repository with pip:

    pip install rtfparse

Installation creates an executable file `rtfparse` in your python scripts folder which should be in your `$PATH`. 

# First Run

When you run `rtfparse` for the first time it will start a configuration wizard which will guide you through the process of creating a default configuration file and specifying the location of its folders. (These folders serve as locations for saving extracted rtf or html files.)

In the configuration wizard you can press `A` for care-free automatic configuration, which would look something like this:

```
$ rtfparse
Config file missing, creating new default config file

 ____ ____ __ _ ____ _ ____ _  _ ____ ____ ___ _ ____ __ _
 |___ [__] | \| |--- | |__, |__| |--< |--|  |  | [__] | \|
 _  _ _ ___  ____ ____ ___
 |/\| |  /__ |--| |--< |__>


◊ email_rtf (C:\Users\nagidal\rtfparse\email_rtf) does not exist!

(A) Automatically configure this and all remaining rtfparse settings
(C) Create this path automatically
(M) Manually input correct path to use or to create
(Q) Quit and edit `email_rtf` in rtfparse_configuration.ini

Created directory C:\Users\nagidal\rtfparse
Created directory C:\Users\nagidal\rtfparse\email_rtf
Created directory C:\Users\nagidal\rtfparse\html
```

`rtfparse` also creates the folder `.rtfparse` (beginning with a dot) in your home directory where it saves its default configuration and its log files.

# Usage From Command Line

Use the `rtfparse` executable from the command line. For example if you want to de-encapsulate the HTML from an RTF file, do it like this:

    rtfparse -f "path/to/rtf_file.rtf" -d

Or you can de-encapsulate the HTML from an MS Outlook message, thanks to [extract_msg](https://github.com/TeamMsgExtractor/msg-extractor) and [compressed_rtf](https://github.com/delimitry/compressed_rtf):

    rtfparse -m "path/to/email.msg" -d

The resulting html file will be saved to the `html` folder you set in the `rtfparse_configuration.ini`. Command reference is in `rtfparse --help`.

# Usage in python module

```
import pathlib
from rtfparse.parser import Rtf_Parser
from rtfparse.renderers import de_encapsulate_html


source_path = pathlib.Path(r"path/to/your/rtf/document.rtf")
target_path = pathlib.Path(r"path/to/your/html/de_encapsulated.html")


parser = Rtf_Parser(rtf_path=source_path)
parsed = parser.parse_file()


renderer = de_encapsulate_html.De_encapsulate_HTML()
with open(target_path, mode="w", encoding="utf-8") as html_file:
    renderer.render(parsed, html_file)
```

# RTF Specification Links

If you find a working official Microsoft link to the RTF specification and add it here, you'll be remembered fondly.

* [Swissmains Link to RTF Spec 1.9.1](https://manuals.swissmains.com/pages/viewpage.action?pageId=1376332&preview=%2F1376332%2F10620104%2FWord2007RTFSpec9.pdf)
* [Webarchive Link to RTF Spec 1.9.1](https://web.archive.org/web/20190708132914/http://www.kleinlercher.at/tools/Windows_Protocols/Word2007RTFSpec9.pdf)
* [RTF Extensions, MS-OXRTFEX](https://docs.microsoft.com/en-us/openspecs/exchange_server_protocols/ms-oxrtfex/411d0d58-49f7-496c-b8c3-5859b045f6cf)
