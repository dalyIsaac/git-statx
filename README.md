# git-statx

Generates a CSV which looks like:

| File                | Statistic      | File extension | 2018 February | 2018 March | 2018 April | ... | Dir1 | Dir2   | ... |
| ------------------- | -------------- | -------------- | ------------- | ---------- | ---------- | --- | ---- | ------ | --- |
| .gitignore          | lines added    | gitignore      | 29            | 0          | 0          | 2   |      |        |     |
| .gitignore          | lines deleted  | gitignore      | 6             | 0          | 0          | 0   |      |        |     |
| .gitignore          | number commits | gitignore      | 3             | 0          | 0          | 1   |      |        |     |
| src/Program.cs      | lines added    | cs             | 102           | 23         | 56         | 123 | src  |        |     |
| ...                 | ...            | ...            | ...           | ...        | ...        | ... |      |        |     |
| ...                 | ...            | ...            | ...           | ...        | ...        | ... |      |        |     |
| src/Thingy/class.cs | ...            | cs             | ...           | ...        | ...        | ... | src  | Thingy |     |

## Requirements

* [Python 3](https://www.python.org/) (tested on Python 3.7)
* [git](https://git-scm.com/)

## Usage

### Windows

Assumes that Python 3 is on the PATH.

``` shell
python git-statx.py
```

### Linux

``` shell
python3 git-statx.py
```

To make an executable:

1. Type the following to make `git-statx.py` executable
   ``` shell
   chmod +x git-statx.py
   ```
2. Move `git-statx.py` to your `bin` directory, and it will be runnable from anywhere as `git-statx.py`
