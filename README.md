# git-statx

Generates a CSV which looks like:

| File name | File extension | Statistic      | 2018 February | 2018 March | 2018 April | ... | Dir1 | Dir2      | Dir 3  | ... |
| --------- | -------------- | -------------- | ------------- | ---------- | ---------- | --- | ---- | --------- | ------ | --- |
| main      | py             | lines added    | 29            | 0          | 2          | ... | src  |           |        | ... |
| main      | py             | lines deleted  | 6             | 0          | 0          | ... | src  |           |        | ... |
| main      | py             | number commits | 3             | 0          | 1          | ... | src  |           |        | ... |
| filename  | py             | lines added    | ...           | ...        | ...        | ... | src  | directory | thingy | ... |
| ...       | ...            | ...            | ...           | ...        | ...        | ... |      |           |        | ... |
| ...       | ...            | ...            | ...           | ...        | ...        | ... |      |           |        | ... |

The last file shown above would have the path `src/directory/thingy/filename.py`.

The CSV file retrieves data from:

``` shell
git log --numstat
```

## Requirements

* [Python](https://www.python.org/) (tested on Python 3.7.1 and 2.7.15)
* [git](https://git-scm.com/)

This program assumes that your computer uses a locale which uses the datetime format of en_US:

For example,

``` shell
Tue Aug 16 21:30:00 1988
```

## Usage

To download the repository, ensure git is installed, then in the desired directory:

``` shell
git clone https://github.com/dalyIsaac/git-statx.git
```

### Windows

Assuming that Python 3 is on the PATH:

``` shell
python git-statx.py
```

### Linux

To make an executable:

1. Type the following to make `git-statx.py` executable:
   ``` shell
   chmod +x git-statx.py
   ```
2. Move `git-statx.py` to your `bin` directory, and it will be runnable from anywhere as `git-statx.py`

#### Python 2

``` shell
python git-statx.py
```

#### Python 3


``` shell
python3 git-statx.py
```

## Performance

The [Visual Studio Code](https://github.com/microsoft/vscode) repository on 26 November 2018 had around 42,700 commits over about 36 months. `git-statx` ran in about 55 seconds.
