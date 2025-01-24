ARG BASE_IMAGE=gitlab-registry.cern.ch/feickert/columnar-athena-containers:analysisbase-25.2.30-latest
FROM ${BASE_IMAGE} AS base

SHELL [ "/bin/bash", "-c" ]

USER root

# needed for dasklab extension.
# c.f. https://github.com/git-lfs/git-lfs/blob/main/INSTALLING.md
RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.rpm.sh | sudo bash && \
    yum install -y \
        nodejs \
        git-lfs \
        graphviz && \
    yum clean all && \
    git lfs install && \
    git lfs version

# Add Tini
ENV TINI_VERSION=v0.19.0
ADD --chown=atlas https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini

COPY --chown=atlas docker/requirements.txt /docker/
COPY --chown=atlas docker/requirements.lock /docker/
COPY --chown=atlas analysis /analysis
WORKDIR /analysis

COPY --chown=atlas /docker/entrypoint.sh /entrypoint.sh
COPY --chown=atlas /docker/cmd.sh /cmd.sh

RUN echo -e '\n# Activate python virtual environment\nif [ -d /venv/bin ]; then\n    . /venv/bin/activate\nfi' >> /release_setup.sh && \
    bash <(curl -sL https://raw.githubusercontent.com/matthewfeickert/cvmfs-venv/v0.0.7/cvmfs-venv.sh) /venv && \
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

RUN chmod +x /tini && \
    chmod +x /entrypoint.sh && \
    chmod +x /cmd.sh && \
    chmod +x /release_setup.sh

# Always have this be the last edit to /release_setup.sh
RUN echo -e "\n# Ensure that the virtual environment is always at the HEAD of PYTHONPATH\ncvmfs-venv-rebase" >> /release_setup.sh

USER atlas

# Setup environment for default user 'atlas'
# Install https://github.com/astral-sh/uv for users editing environment later
RUN echo -e '\n# Activate AnalysisBase environment on login shell\n. /release_setup.sh\n' >> /home/atlas/.bashrc && \
    . /release_setup.sh && \
    mkdir -p $(jupyter --config) && \
    curl -LsSf https://astral.sh/uv/install.sh | sh

# $(jupyter --config) should be /home/atlas/.jupyter/
COPY --chown=atlas docker/jupyter_lab_config.py /home/atlas/.jupyter/

ENTRYPOINT ["/tini", "-g", "--", "/entrypoint.sh"]

CMD [ "/cmd.sh" ]
