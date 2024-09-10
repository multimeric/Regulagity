import tempfile
import sys
from os import path

import pandas
from pandas.tseries import frequencies
from pandas import Series, date_range
from git import Repo
from datetime import datetime
from typer import Option, Argument, Typer
from typing import Annotated
from enum import Enum

class StatChoice(Enum):
    proportion = "proportion"
    count = "count"

app = Typer()

@app.command()
def main(
    location: Annotated[str, Argument(help="The path either to a local git repository or to a git remote, e.g. `/home/michael/Programming/Regulagity/` or `https://github.com/TMiguelT/Regulagity.git`")] = ".",
    period: Annotated[str, Option(help='Period of time to summarise commits over. This consists of an optional number followed by a letter code, e.g. `2W` means two weeks, `3M` means 3 months, `Y` means 1 year etc. For a full reference on these string codes, refer to http://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases')] = "W",
    stat: Annotated[StatChoice, Option(help = 'The way we summarise each commit over the time period. `proportion` indicates that we should calculate what proportion of the time period has any commits (e.g. how many weeks on average have any activity) whereas `count` indicates that we should take the average number of commits in this time period (e.g. how many commits are on average made per week)')] = StatChoice.proportion
):
    """
    Calculates commit frequency statistics for a git repository. 
    """
    if path.exists(location):
        # If the user provided a filepath, that's the git repo
        print('Provided path was a real directory, checking for git repository...',
              file=sys.stderr)
        repo = Repo(location)
        tempd = None
    else:
        # Next, check if it's a git remote and try cloning it
        print('Provided path was a git remote, cloning...', file=sys.stderr)
        tempd = tempfile.TemporaryDirectory()
        repo = Repo.clone_from(location, tempd.name)

    # Get the offset object for making a human readable message
    offset = frequencies.to_offset(period)
    if offset is None:
        raise Exception(f"Invalid offset {offset}")

    # Extract a series of commit dates from the repo, and then group them by the provided
    # period
    commits = Series(repo.iter_commits(), dtype=object)
    dates = pandas.to_datetime(
        commits.apply(lambda commit: commit.committed_date),
        unit='s'
    )
    df = pandas.DataFrame({'commits': commits, 'dates': dates})
    counts = df.groupby(pandas.Grouper(freq=period, key='dates')).count()

    # Extend the counts to present day
    counts = counts.reindex(counts.index.union(date_range(
        start=counts.index.min(),
        end=datetime.today(),
        freq=period
    )), fill_value=0)

    if stat == StatChoice.proportion:
        result = counts['commits'].apply(lambda count: 0 if count == 0 else 1).mean()
        print(
            'Calculating the proportion of each {} {} period with any git activity'.format(
                offset.n,
                type(offset).__name__.lower()
            ), file=sys.stderr)
    elif stat == StatChoice.count:
        result = counts.mean()[0]
        print('Calculating average commits per {} {} period'.format(
            offset.n,
            type(offset).__name__.lower()
        ), file=sys.stderr)

    print(result)

    if tempd:
        tempd.cleanup()
