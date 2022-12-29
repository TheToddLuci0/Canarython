# syntax=docker/dockerfile:1
FROM debian:latest AS builder
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /root/
#https://docs.docker.com/engine/reference/builder/#run---mounttypecache
RUN rm -f /etc/apt/apt.conf.d/docker-clean; echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt update && apt install -y python3 python3-pip python3-venv 
COPY src pyproject.toml ./
RUN python3 -m pip install --upgrade build && \
    python3 -m build 


# Deployment container
# We use debian rather than python:latest to avaid issues with python3-gpg binding to the propper python
FROM debian:latest
ENTRYPOINT canarython
COPY --from=builder /root/dist/*.whl /tmp/
ENV DEBIAN_FRONTEND=noninteractive
#https://docs.docker.com/engine/reference/builder/#run---mounttypecache
RUN rm -f /etc/apt/apt.conf.d/docker-clean; echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt update && \
    apt install -y python3 python3-pip python3-gpg
    # apt install -y libassuan-dev bzip2 g++ make autoconf libgpg-error-dev wget swig python3-dev file python3 python3-pip gpg-agent gpgsm gpg gpgconf
#TODO: Move the GpgME install stuff to the build container... somehow
# RUN wget -q 'https://gnupg.org/ftp/gcrypt/gpgme/gpgme-1.18.0.tar.bz2' -O /tmp/gpgme.tar.bz2 && \
#     mkdir /opt/gpgme && \
#     tar -xf /tmp/gpgme.tar.bz2 -C /opt/gpgme --strip-components=1 && \ 
#     cd /opt/gpgme && ./configure -q && make -j$(nproc) -s && make install -j$(nproc) -s && \ 
RUN pip3 install /tmp/*.whl

# Reset this incase someone wants to manually install packages or something
ENV DEBIAN_FRONTEND=dialog