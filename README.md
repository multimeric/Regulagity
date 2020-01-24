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

## Examples
* What proportion of months have had any commit activity since this repo was created?
    `regulagity --period M --stat proportion https://github.com/TMiguelT/Regulagity.git`
* What is the average commits per fortnight in this repo?
    ` regulagity --period 2W --stat count /home/michael/Programming/Regulargity`
    
## Motivation
There are numerous other tools that summarise git activity, for example:

* <http://gitstats.sourceforge.net/>
* <https://www.npmjs.com/package/git-stats>
* <https://github.com/src-d/hercules>
* <https://github.com/ejwa/gitinspector>

However, when comparing repos, perhaps because you want to use the best supported and 
maintained option, you really only want a single number you can use to easily compare 
them. For this reason, `regulagity` only ever outputs a single number for a repo, not
a plot or a table.

The reason `regulagity` supports analyses like "what proportion of months have had any
activity" is because it avoids any biases you might get by asking "what is the average
number of commits" or "average lines changed". These can be biased by a repo that has
a million commits over a single month, because it will still has a high number of commits 
per month on average, even if it's been abandoned since 2015. The same issue is 
encountered for lines-of-code. Asking only if there has been *any* activity of a given 
period allows you to better compare repos, and allows you to be certain that a high number
means a better amount of support. You can even use this same statistic to compare open 
source repos to commercial products, because you can also ask "what proportion of months
have a new update to this software?".

## Roadmap
Planned features:

* Allow calculation of average lines-of-code, not just commit numbers
* Allow custom date-ranges for the query, e.g. "in the last year" rather than "for the 
    entire commit history"