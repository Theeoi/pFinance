# pFinance

Visualize your spending with python and pandas.

## General Information

Current personal finance apps are not cutting it. They either require a
subscription, are unintuitive to use or both. pFinance is meant as a minimal
solution to categorize and visualize your income and spending over time.

### Technologies

* Python 3.10<
* Pandas 1.5<

### Features

* Categorize and store your transaction history in a personal SQLite database.
* View your aggregate database.
* More features coming. See [Project Status](#project-status)

## Setup

pFinance is built entirely on python and related packages all available through
pip.

1. Clone the repo: `git clone https://github.com/Theeoi/pFinance.git`
2. cd into the directory: `cd pFinance`
3. Install requirements: `pip install -r requirements.txt`
4. Install package: `pip install .`

### Usage

See `pfinance -h` for help.

### Contributing

Feel free to raise an issue or make a pull request! <3

The project is built with python 3.10 typehinting in mind and should be
formatted according to PEP8. I personally use mypy and autopep8 to check my
code.

## Project Status

This project is in progress but is sporadically worked on during spare time.

### Roadmap

To do:
- [x] Store input data in SQLite database.
- [x] Identify overlap between database and input data. Only add new transactions
  to the database.
- [ ] Add categorization to input data using some sort of mapping.
- [ ] Visualize the database with a graph.
- [ ] Add a way to select a date-span to visualize.

Room for improvement:
- Add proper testing with pytest.
- Expand available input data options. Currently only Handelsbanken .ods
  files.
- Add way to revert/clear database of recent/all loads.
- Develop a TUI/GUI to complement the CLI.

## Contact

Created by [@theodorblom](https://www.theodorblom.com) - feel free to contact
me!
