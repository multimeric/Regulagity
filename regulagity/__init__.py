import tempfile
import sys
from os import path

import click
import pandas
from pandas.tseries import frequencies
from git import Repo


@click.command()
@click.argument(
    'location',
    default='.'
)
@click.option(
    '--period',
    default='M',
    help='Period of time to summarise commits over. This consists of an optional number followed by a letter code, e.g.'
         ' `2W` means two weeks, `3M` means 3 months, `Y` means 1 year etc. For a full reference on these string codes, '
         'refer to http://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases')
@click.option(
    '--stat',
    default='bool',
    type=click.Choice(['proportion', 'count']),
    help='The way we summarise each commit over the time period. '
         '`proportion` indicates that we should calculate what proportion of the time period has any commits (e.g. how '
         'many weeks on average have any activity) whereas `count` indicates that we should take the average number of '
         'commits in this time period (e.g. how many commits are on average made per week)'
)
# @click.option(
#     '--measure',
#     default='commits',
#     type=click.Choice(['commits', 'locs']),
#     help='The object to count. Either commits or lines of code (locs)'
# )
def main(location, period, stat):
    """
        Calculates summary statistics for the git repository located at LOCATION. LOCATION must be the path either
        to a local git repository or to a git remote, e.g. `/home/michael/Programming/Regulagity/` or
        `https://github.com/TMiguelT/Regulagity.git`
    """
    if path.exists(location):
        # If the user provided a filepath, that's the git repo
        print('Provided path was a real directory, checking for git repository...', file=sys.stderr)
        repo = Repo(location)
        tempd = None
    else:
        # Next, check if it's a git remote and try cloning it
        print('Provided path was a git remote, cloning...', file=sys.stderr)
        tempd = tempfile.TemporaryDirectory()
        repo = Repo.clone_from(location, tempd.name)

    offset = frequencies.to_offset(period)

    commits = pandas.Series(repo.iter_commits(), dtype=pandas.np.object_)
    dates = pandas.to_datetime(
        commits.apply(lambda commit: commit.committed_date),
        unit='s'
    )
    df = pandas.DataFrame({'commits': commits, 'dates': dates})
    counts = df.groupby(pandas.Grouper(freq=period, key='dates')).count()

    if stat == 'bool':
        result = counts['commits'].apply(lambda count: 0 if count == 0 else 1).mean()
        print('Calculating the proportion of each {} {} period with any git activity'.format(
            offset.n,
            type(offset).__name__.lower()
        ), file=sys.stderr)
    else:
        result = counts.mean()[0]
        print('Calculating average commits per {} {} period'.format(
            offset.n,
            type(offset).__name__.lower()
        ), file=sys.stderr)

    print(result)

    if tempd:
        tempd.cleanup()


if __name__ == "__main__":
    main()
