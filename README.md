# Regulagity
## Introduction
Regulagity (reh-gew-la-git-ee) is a command-line tool for measuring activity in a git repo, ultimately producing a single number that summarises a repo.

For example, you can ask "how many commits per year does this repo have?" or "what proportion of months does this repo have new commits?". Both of these are good summaries of how *active* a repo is.

## Installation
Run:
```bash
pip install regulagity
```

## Usage
```bash
Usage: regulagity [OPTIONS] [LOCATION]

  Calculates summary statistics for the git repository located at LOCATION.
  LOCATION must be the path either to a local git repository or to a git
  remote, e.g. `/home/michael/Programming/Regulagity/` or
  `https://github.com/TMiguelT/Regulagity.git`

Options:
  --period TEXT              Period of time to summarise commits over. This
                             consists of an optional number followed by a
                             letter code, e.g. `2W` means two weeks, `3M`
                             means 3 months, `Y` means 1 year etc. For a full
                             reference on these string codes, refer to
                             http://pandas.pydata.org/pandas-
                             docs/stable/user_guide/timeseries.html#offset-
                             aliases
  --stat [proportion|count]  The way we summarise each commit over the time
                             period. `proportion` indicates that we should
                             calculate what proportion of the time period has
                             any commits (e.g. how many weeks on average have
                             any activity) whereas `count` indicates that we
                             should take the average number of commits in this
                             time period (e.g. how many commits are on average
                             made per week)
  --help                     Show this message and exit.
```
