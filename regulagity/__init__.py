import tempfile
from os import path

import click
import pandas
from git import Repo


@click.command()
@click.argument('location', default='.')
@click.argument('period', default='M')
@click.option(
    '--stat',
    default='bool',
    type=click.Choice(['bool', 'count']),
    help='The way we summarise each commit over the time period. Either using boolean "some commits" vs "no commits" (bool), or the raw count of commits'
)
# @click.option(
#     '--measure',
#     default='commits',
#     type=click.Choice(['commits', 'locs']),
#     help='The object to count. Either commits or lines of code (locs)'
# )
def main(location, period, stat):
    if path.exists(location):
        # If the user provided a filepath, that's the git repo
        repo = Repo(location)
        tempd = None
    else:
        # Next, check if it's a git remote and try cloning it
        tempd = tempfile.TemporaryDirectory()
        repo = Repo.clone_from(location, tempd)

    commits = pandas.Series(repo.iter_commits(), dtype=pandas.np.object_)
    dates = pandas.to_datetime(commits.apply(lambda commit: commit.committed_date),
                               unit='s')
    df = pandas.DataFrame({'commits': commits, 'dates': dates})
    counts = df.groupby(pandas.Grouper(freq=period, key='dates')).count()

    if stat == 'bool':
        counts = counts['commits'].apply(lambda count: 0 if count == 0 else 1)

    mean = counts.mean()
    print(mean)

    if tempd:
        tempd.cleanup()


if __name__ == "__main__":
    main()
