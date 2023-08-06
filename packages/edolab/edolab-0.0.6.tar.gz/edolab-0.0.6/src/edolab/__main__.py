""" The main script. """

import os
import pathlib
import tarfile

import click
import dask
import pandas as pd
import tqdm
from dask.diagnostics import ProgressBar

from .run import get_experiment_parameters, run_single_trial
from .summarise import (
    get_distributions,
    get_representative_idxs,
    get_trial_summary,
    write_representatives,
)
from .version import __version__


def _get_root_from_experiment(experiment):
    """Get the root directory from an experiment. If there isn't one, set the
    root to be adjacent to the experiment script."""

    root = get_experiment_parameters(experiment).pop("root")
    root = experiment.parent if root is None else root

    return root


@click.group(invoke_without_command=True)
@click.option(
    "--version", is_flag=True, default=False, help="The current version."
)
def main(version):
    """ Run and summarise experiments with `edo`. """

    if version:
        click.echo(__version__)


@main.command()
@click.argument("experiment", type=click.Path(exists=True))
@click.option(
    "--cores", default=None, type=int, help="The number of cores to use."
)
@click.option("--seeds", default=1, help="The number of trials to run.")
def run(experiment, cores, seeds):
    """ Run a series of trials using the `experiment` script. """

    experiment = pathlib.Path(experiment).resolve()
    name = experiment.stem

    click.echo(f"Running experiment: {name}")

    root = _get_root_from_experiment(experiment)
    out = pathlib.Path(root) / name / "data"
    out.mkdir(exist_ok=True, parents=True)

    click.echo(f"Writing to: {out}")

    tasks = (run_single_trial(experiment, out, seed) for seed in range(seeds))

    with ProgressBar():
        if cores is None:
            dask.compute(*tasks, scheduler="single-threaded")
        else:
            dask.compute(*tasks, num_workers=cores, scheduler="processes")

    click.echo("Experiment complete")


@main.command()
@click.option(
    "--tarball/--no-tarball",
    default=False,
    help="Tarball the data and delete original, or don't.",
)
@click.argument("experiment", type=click.Path(exists=True))
@click.argument("quantiles", nargs=-1, type=float, required=False)
def summarise(tarball, experiment, quantiles):
    """Summarise the EDO data from an experiment.

    Here, `experiment` should be a path to an experiment script of the form
    `/path/to/experiment/<experiment-name>.py`.

    To specify quantiles (between 0 and 1), list them at the end separated by
    spaces. Defaults to the minimum, median and maximum."""

    if not quantiles:
        quantiles = (0, 0.5, 1)

    experiment = pathlib.Path(experiment)
    root = _get_root_from_experiment(experiment)
    out = pathlib.Path(root) / experiment.stem
    data = out / "data"
    summary_path = out / "summary"
    summary_path.mkdir(exist_ok=True)

    click.echo(f"Summarising data at {out}")

    distributions = get_distributions(experiment)
    trials = [
        path
        for path in data.iterdir()
        if path.is_dir() and path.stem != "subtypes"
    ]
    summaries = []
    for trial in tqdm.tqdm(trials):
        summaries.append(get_trial_summary(trial, distributions))

    summary = pd.concat(summaries)
    summary = summary.sort_values(["generation", "individual", "seed"])
    summary.to_csv(summary_path / "main.csv", index=False)

    click.echo("Getting representative individuals")

    idxs = get_representative_idxs(summary, quantiles)
    write_representatives(summary, idxs, data, summary_path)

    if tarball:
        click.echo("Making tarball")

        with tarfile.open(str(data) + ".tar.gz", "w:gz") as tar:
            tar.add(data, arcname=data.stem)

        os.system(f"rm -r {data}")

    click.echo("Summary complete")


if __name__ == "__main__":  # pragma: no cover
    main()
