## PA193 parser


**Usage**

```
python3 main.py -h
usage: main.py [-h] [--verbose] [--all] [--title] [--bibliography] [--versions] FILE.TXT

Parse Common Criteria certificates. Input has to be plain txt file. You can define what part to parse using arguments. Use --all to parse entire file.

positional arguments:
  FILE.TXT        file to parse

optional arguments:
  -h, --help      show this help message and exit
  --verbose       sum the integers (default: find the max)
  --all           Parse the entire file
  --title         Parse the title
  --bibliography  Parse the bibliography
  --versions      Parse versions
```


**Tests**

Tests using dataset:
```
cd tests/dataset/
bash test.sh
```

Provided output shows score [0, 100] for each file. If value is missing, the scoring script failed.



**Used language:** Python

**Authors**

* Miriam Gáliková, 500327
* Jan Jelínek, 445416
* Šimon Berka, 433498


