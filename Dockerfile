# syntax=docker/dockerfile-upstream:master-labs
FROM ubuntu:jammy

# args
ARG PROJECT="neo84"
ARG PACKAGES="git mc htop neovim git"

ARG CONDADIR="/miniconda"
ARG CONDAENV="neo84"
ARG CONDA_PREFIX=${CONDADIR}/envs/${CONDAENV}
ARG CONDADEPS="requirements.yaml"
ARG CONDASETUP=Miniconda3-py310_23.1.0-1-Linux-x86_64.sh
ARG CONDAURL=https://repo.anaconda.com/miniconda/${CONDASETUP}

### setup env for using conda
ENV PATH="/miniconda/bin:${PATH}"
ENV LD_LIBRARY_PATH=${CONDA_PREFIX}/lib/:$LD_LIBRARY_PATH

### install packages
RUN apt update && apt install -y ${PACKAGES}

# install conda
ADD --checksum=sha256:32d73e1bc33fda089d7cd9ef4c1be542616bd8e437d1f77afeeaf7afdb019787 ${CONDAURL} /
RUN chmod a+x /${CONDASETUP}
RUN /bin/bash /${CONDASETUP} -b -p ${CONDADIR} # /bin/bash workaround for defect shellscript

## update conda if current version is not up-to-date
RUN conda update -n base -c defaults conda

### setup conda environment
COPY ${CONDADEPS} /root/
RUN ${CONDADIR}/bin/conda env create -n neo84 -f /root/${CONDADEPS}
RUN ${CONDADIR}/bin/conda init bash
# by default activate custom conda env
RUN echo "conda activate neo84" >> /root/.bashrc

# all following RUNs should run in a real login shell to mitigate conda env activation problem
SHELL [ "conda", "run", "-n", "neo84", "/bin/bash", "--login", "-c" ]

## add default container user
RUN groupadd -g 1000 vscode
RUN useradd -rm -d /home/vscode -s /bin/bash -g root -G sudo -u 1000 vscode

## create vscode extension folders
RUN mkdir /home/vscode/.vscode-server
RUN mkdir /home/vscode/.vscode-server-insiders
RUN chown vscode:vscode /home/vscode/.vscode-server
RUN chown vscode:vscode /home/vscode/.vscode-server-insiders

# setup default conda environment for vscode user
USER vscode
RUN ${CONDADIR}/bin/conda init bash
# by default activate custom conda env
RUN echo "conda activate neo84" >> /home/vscode/.bashrc

# switch back to root
USER root

# change workdir to make notebooks browsable in jupyter notebooks
WORKDIR /workspaces

## volumes
VOLUME [ "/notebooks" ]

# vscode workspace
VOLUME [ "/workspaces/${PROJECT}" ]

# vscode extensions
VOLUME [ "/home/vscode/.vscode-server"]
VOLUME [ "/home/vscode/.vscode-server-insiders"]

# document ports
EXPOSE 8888/tcp
EXPOSE 8889/tcp