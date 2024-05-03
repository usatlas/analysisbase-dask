# analysisbase-dask

Docker image with ATLAS AnalysisBase 24.2.X, Dask, and Scikit-HEP tools

## Run

### UChicago Analysis Facility

A version of this image is available for use at the [US ATLAS Analysis Facility at UChicago](https://af.uchicago.edu/) through the [JupyterHub service](https://af.uchicago.edu/jupyterlab).
When [configuring](https://af.uchicago.edu/jupyterlab/configure) the Jupyter Lab instance for your session select the image from the "Image" drop-down menu.

### Locally

``` bash
docker pull sslhep/analysis-dask-base:latest
```

``` bash
docker run --rm -ti --publish 8888:8888 --volume $PWD:/analysis sslhep/analysis-dask-base:latest
```

(as using Jupytext right click `.py` files to open as a Jupyter notebook)

#### Without using the JupyterLab environment

``` bash
docker run --rm -ti --publish 8888:8888 --volume $PWD:/analysis sslhep/analysis-dask-base:latest /bin/bash
```

## AnalysisBase images

Lists of all AnalysisBase releases that could be used as base images are provided on the ATLAS Twikis:

* [Release 24.2.X series](https://twiki.cern.ch/twiki/bin/view/AtlasProtected/AnalysisBaseReleaseNotes24pt2)
* [Release 21.2.X series](https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/AnalysisBaseReleaseNotes21_2)

More easily though, you can just use [`crane`](https://github.com/google/go-containerregistry/blob/v0.14.0/cmd/crane/) to get a listing of all images from the command line

``` bash
crane ls gitlab-registry.cern.ch/atlas/athena/analysisbase
```

## Updating image dependencies

All the Python dependencies installed into the default Python virtual environment in the container image are installed from a lock file.
To update the dependencies and the lock file:

1. Make a new branch.
2. Figure out what the version of the dependency you want to install is with

    ``` bash
    python -m pip index versions <dependency name>
    ```

3. Add this dependency and version to the `docker/requirements.txt` with the version pinned.

    Example:

    ```
    dask-labextension==7.0.0
    ```

4. Rebuild the lock file with `make lock` (this also verifies that the environment can be installed).
5. Add and commit the updated `docker/requirements.txt` and `docker/requirements.lock`.
6. Open a PR with the changes and wait for the CI to verify the build passes.

## Triggering image rebuilds in CI

To trigger an image rebuild use the workflow dispatch feature of the [`base_builder` workflow](https://github.com/usatlas/analysisbase-dask/actions/workflows/base_builder.yaml).

1. Visit the [`base_builder` workflow GitHub Actions page](https://github.com/usatlas/analysisbase-dask/actions/workflows/base_builder.yaml).
2. Select the "Run workflow" button on the top right side of the workflow runs table.
3. Select which branch you would like to build from in the "Use workflow from" drop down menu.
4. Click the "Run workflow" button.
