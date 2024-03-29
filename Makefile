lock:
	docker pull gitlab-registry.cern.ch/atlas/athena/analysisbase:25.2.2
	docker build \
		--file docker/Dockerfile.lockfile-builder \
		--build-arg BASE_IMAGE=gitlab-registry.cern.ch/atlas/athena/analysisbase:25.2.2 \
		--tag tmp/analysisbase:rel25-lockfile-builder \
		docker
	docker run \
		--rm \
		-ti \
		--user 1000:1000 \
		--volume $(shell pwd)/docker:/workdir \
		tmp/analysisbase:rel25-lockfile-builder \
		bash -c 'bash <(curl -sL https://raw.githubusercontent.com/matthewfeickert/cvmfs-venv/v0.0.5/cvmfs-venv.sh) && \
			. venv/bin/activate && \
			python -m pip --no-cache-dir install --upgrade uv && \
			uv pip compile --generate-hashes --output-file=requirements.lock requirements.txt && \
			deactivate && \
			rm -r venv'

build:
	docker pull gitlab-registry.cern.ch/atlas/athena/analysisbase:25.2.2
	docker build \
		--file docker/Dockerfile \
		--build-arg BASE_IMAGE=gitlab-registry.cern.ch/atlas/athena/analysisbase:25.2.2 \
		--tag sslhep/analysis-dask-base:debug \
		.

tag:
	docker tag sslhep/analysis-dask-base:debug sslhep/analysis-dask-base:latest
