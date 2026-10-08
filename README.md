# Easier parameter scans with hmcdj&mdash;Analysis workflow

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23239277.svg)][zenodo]

The workflow in this repository performs
the analyses presented in the proceeding
[Easier parameter scans with hmcdj][paper].

## Requirements

- Conda, for example, installed from [Miniforge][miniforge]
- [Snakemake][snakemake], which may be installed using Conda
- LaTeX, for example, from [TeX Live][texlive]
- [hmcdj][hmcdj]

## Setup

1. Install the dependencies above.
2. Clone this repository
   (or download its Zenodo release and `unzip` it)
   and `cd` into it:

   ```shellsession
   git clone https://github.com/telos-collaboration/hmcdj-lattice2026
   cd hmcdj-lattice2026
   ```

3. Download the file `TwoFundamentalFermionsTrack.yaml` from [Zenodo][zenodo],
   and place it in the root of the repository.

4. Build [hmcdj][hmcdj],
   including the `TwoFundamentalFermions` deck.
   Place the deck into the root of this repository.

## Running the workflow

The workflow is run using Snakemake:

``` shellsession
snakemake --cores 1 --use-conda
```

where the number `1`
may be replaced by
the number of CPU cores you wish to allocate to the computation.

Snakemake will automatically download and install
all required Python packages.
This requires an Internet connection;
if you are running in an HPC environment where you would need
to run the workflow without Internet access,
details on how to preinstall the environment
can be found in the [Snakemake documentation][snakemake-conda].

The total process takes around eight minutes on a four-core i5-5250U CPU.

## Output

The output plot is placed in the `assets/plots` directory.

Intermediary data are placed in the `intermediary_data` directory.

## Reusability

This workflow is relatively tailored to the data
which it was originally written to analyse.
The `plot` rule should in principle work with any hmcdj log file,
but this has not been thoroughly tested.

[hmcdj]: https://github.com/telos-collaboration/hmcdj
[miniforge]: https://github.com/conda-forge/miniforge
[paper]: https://doi.org/10.48550/arXiv.TODO_ARXIV_ID
[snakemake]: https://snakemake.github.io
[snakemake-conda]: https://snakemake.readthedocs.io/en/stable/snakefiles/deployment.html
[texlive]: https://tug.org/texlive/
[zenodo]: https://doi.org/10.5281/zenodo.23239277
