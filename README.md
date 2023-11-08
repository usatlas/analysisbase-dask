# analysisbase-dask
Docker image with ATLAS AnalysisBase 24.2.X, Dask, and Scikit-HEP tools

## Run

### UChicago Analysis Facility

A version of this image is available for use at the [US ATLAS Analysis Facility at UChicago](https://af.uchicago.edu/) through the [JupyterHub service](https://af.uchicago.edu/jupyterlab).
When [configuring](https://af.uchicago.edu/jupyterlab/configure) the Jupyter Lab instance for your session select the image from the "Image" drop-down menu.

### Locally

```
docker pull matthewfeickert/analysisbase-dask:24.2.26
```

```
docker run --rm -ti --publish 8888:8888 --volume $PWD:/analysis matthewfeickert/analysisbase-dask:24.2.26
```

(as using Jupytext right click `.py` files to open as a Jupyter notebook)

#### Without using the JupyterLab environment

```
docker run --rm -ti --publish 8888:8888 --volume $PWD:/analysis matthewfeickert/analysisbase-dask:24.2.26 /bin/bash
```

## AnalysisBase images

Lists of all AnalysisBase releases that could be used as base images are provided on the ATLAS Twikis:

* [Release 24.2.X series](https://twiki.cern.ch/twiki/bin/view/AtlasProtected/AnalysisBaseReleaseNotes24pt2)
* [Release 21.2.X series](https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/AnalysisBaseReleaseNotes21_2)

More easily though, you can just use [`crane`](https://github.com/google/go-containerregistry/blob/v0.14.0/cmd/crane/) to get a listing of all images from the command line

```
crane ls gitlab-registry.cern.ch/atlas/athena/analysisbase
```
