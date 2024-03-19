ARG BASE_IMAGE=gitlab-registry.cern.ch/atlas/athena/analysisbase:25.2.2
FROM ${BASE_IMAGE} as base

SHELL [ "/bin/bash", "-c" ]

USER root

# needed for dasklab extension.
RUN yum install -y \
        nodejs \
        graphviz && \
    yum clean all

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
    bash <(curl -sL https://raw.githubusercontent.com/matthewfeickert/cvmfs-venv/v0.0.5/cvmfs-venv.sh) /venv && \
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

# Need to use an additonal directory beyond /usr/AnalysisBase to install
# given how ATLAS CMake works.
# c.f. https://gitlab.cern.ch/gstark/pycolumnarprototype/-/issues/2
RUN . /release_setup.sh && \
    cd /tmp && \
    git clone \
        --recurse-submodules \
        --branch py_el_tool_test \
    https://gitlab.cern.ch/gstark/pycolumnarprototype.git && \
    cd pycolumnarprototype && \
    cmake \
        -S src \
        -B build && \
    cmake build -LH && \
    cmake \
        --build build \
        --clean-first \
        --parallel "$(nproc --ignore=1)" && \
    DESTDIR=/usr/tools cmake --install build && \
    cd /tmp && \
    rm -rf pycolumnarprototype && \
    echo -e "\n# Set up the PyColumnarPrototype tool:" >> /release_setup.sh && \
    echo -e ". $(find /usr/tools -type f -iname 'setup.sh')" >> /release_setup.sh && \
    echo -e 'echo "Configured PyColumnarPrototype from: ${PyColumnarPrototypeDemo_DIR}"' >> /release_setup.sh && \
    . /release_setup.sh && \
    cvmfs-venv-rebase && \
    python -c 'import PyColumnarPrototype; print(f"{PyColumnarPrototype.column_maker()=}")'

# Always have this be the last edit to /release_setup.sh
RUN echo -e "\n# Ensure that the virtual environment is always at the HEAD of PYTHONPATH\ncvmfs-venv-rebase" >> /release_setup.sh

USER atlas

# Setup environment for default user 'atlas'
RUN echo -e '\n# Activate AnalysisBase environment on login shell\n. /release_setup.sh\n' >> /home/atlas/.bashrc && \
    . /release_setup.sh && \
    mkdir -p $(jupyter --config)

# $(jupyter --config) should be /home/atlas/.jupyter/
COPY --chown=atlas docker/jupyter_lab_config.py /home/atlas/.jupyter/

ENTRYPOINT ["/tini", "-g", "--", "/entrypoint.sh"]

CMD [ "/cmd.sh" ]
