# Broken Link Hijacker (BLH)
[![Python3.x](https://img.shields.io/badge/python-3.x-FADA5E.svg?logo=python)](https://www.python.org/) [![PEP8](https://img.shields.io/badge/code%20style-pep8-red.svg)](https://www.python.org/dev/peps/pep-0008/)

Broken Link Hijacker (BLH) is a Fast Broken Link Hijacker Tool written in Python3. It searches for all the Broken Links and crawls the website on 3 different deepness to get all the links from it. It also helps to find all the Social Media or Social Engagement platforms links mentioned on the website.  It Searches for links in:
- `<a href>` tag
- `<img src>` tag

## Installation

```git clone https://github.com/CyberCommands/Broken-Link-Hijacker.git BLH/```

```cd BLH/```

```pip install -r requirements.txt```

```sudu python3 blh.py --help```

## Usage

Short Form    | Long Form     | Description
------------- | ------------- |-------------
url           | url           | A URL to scan 
-d            | Deepness      | Level of deepness to search.(Default=1)[Varies from 1-3]
-v            | --verbosity   | Set the Verbosity for Program
-o            | --output      | Weather to save the output in a file or not.(Default=False)
-h            | --help        | Displays help 


## Examples

- To Use the Tool in the default setting.\
`sudo python3 blh.py https://google.com` will give result.

- To Increase Deepness Use:

`sudo python3 blh.py https://google.com -d 2  ` This will set Deepness to 2.\
`sudo python3 blh.py https://google.com -d 3  ` This will set Deepness to 3 .

- To turn Verbosity Mode On or OFF:
 
  *By default Verbosity Mode is Set to True*.\
  `sudo python3 blh.py https://google.com -v False` . \
  `-v F or -v Flase ` |  `-v T or -v True`.

- To Save output To a file:

  *By default Output is Set to False. The output filename is set to `domain_links.txt` by default*.\
  `sudo python3 blh.py https://google.com -o True` . \
  `-o F or -o False ` | `-o T or -o True`.

### Note
- More details here https://edoverflow.com/2017/broken-link-hijacking/

### Disclaimer

This tool is for testing and educational purposes only. Do not use it for illegal purposes! It is the end user’s responsibility to obey all applicable local, state and federal laws. I am not responsible for any misuse or damage caused by this tool.

