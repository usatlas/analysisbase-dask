ARG BASE_IMAGE=gitlab-registry.cern.ch/atlas/athena/analysisbase:24.2.26
FROM ${BASE_IMAGE} as base

SHELL [ "/bin/bash", "-c" ]

USER root

COPY --chown=atlas docker/requirements.txt /docker/
COPY --chown=atlas docker/requirements.lock /docker/
COPY --chown=atlas analysis /analysis
WORKDIR /analysis

COPY --chown=atlas /docker/cmd.sh /cmd.sh
RUN chmod +x /cmd.sh

RUN printf '\n# Activate python virtual environment\nif [ -d /venv/bin ]; then\n    . /venv/bin/activate\nfi\n' >> /release_setup.sh && \
    bash <(curl -sL https://raw.githubusercontent.com/matthewfeickert/cvmfs-venv/v0.0.4/cvmfs-venv.sh) /venv && \
    chown -R atlas /venv && \
    . /release_setup.sh && \
    python -m pip --no-cache-dir install --upgrade pip setuptools wheel && \
    python -m pip --no-cache-dir install \
        --upgrade \
        --no-deps \
        --require-hashes \
        --requirement /docker/requirements.lock && \
    chown -R atlas /venv && \
    python --version --version && \
    python -m pip list && \
    root --version

USER atlas

CMD [ "/cmd.sh" ]
