lock:
	docker pull gitlab-registry.cern.ch/atlas/athena/analysisbase:24.2.26
	docker build \
		--file docker/Dockerfile.lockfile-builder \
		--build-arg BASE_IMAGE=gitlab-registry.cern.ch/atlas/athena/analysisbase:24.2.26 \
		--tag tmp/analysisbase:rel24-lockfile-builder \
		docker
	docker run \
		--rm \
		-ti \
		--user 1000:1000 \
		--volume $(shell pwd)/docker:/workdir \
		tmp/analysisbase:rel24-lockfile-builder \
		bash -c 'bash <(curl -sL https://raw.githubusercontent.com/matthewfeickert/cvmfs-venv/v0.0.4/cvmfs-venv.sh) && \
			. venv/bin/activate && \
			python -m pip --no-cache-dir install --upgrade pip-tools && \
			pip-compile --generate-hashes --output-file=requirements.lock requirements.txt && \
			deactivate && \
			rm -r venv'

build:
	docker pull gitlab-registry.cern.ch/atlas/athena/analysisbase:24.2.26
	docker build \
		--file docker/Dockerfile \
		--build-arg BASE_IMAGE=gitlab-registry.cern.ch/atlas/athena/analysisbase:24.2.26 \
		--tag example/analysisbase-dask:24.2.26 \
		.

tag:
	docker tag example/analysisbase-dask:24.2.26 matthewfeickert/analysisbase-dask:24.2.26
