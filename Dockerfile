FROM python:3.8.2-slim-buster

ARG GDAL_VERSION=3.0.4
ARG SOURCE_DIR=/usr/local/src/python-gdal

RUN \
# Install runtime dependencies
    apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        wget \
        automake libtool pkg-config libsqlite3-dev sqlite3 \
        libpq-dev \
        libcurl4-gnutls-dev \
        libproj-dev \
        libxml2-dev \
        libgeos-dev \
        libnetcdf-dev \
        libpoppler-dev \
        libspatialite-dev \
        libhdf4-alt-dev \
        libhdf5-serial-dev \
        libopenjp2-7-dev \
    && rm -rf /var/lib/apt/lists/* \
    \
# Build against PROJ master (which will be released as PROJ 6.0)
    && wget "http://download.osgeo.org/proj/proj-6.0.0.tar.gz" \
    && tar -xzf "proj-6.0.0.tar.gz" \
    && mv proj-6.0.0 proj \
    && echo "#!/bin/sh" > proj/autogen.sh \
    && chmod +x proj/autogen.sh \
    && cd proj \
    && ./autogen.sh \
    && CXXFLAGS='-DPROJ_RENAME_SYMBOLS' CFLAGS='-DPROJ_RENAME_SYMBOLS' ./configure --disable-static --prefix=/usr/local \
    && make -j"$(nproc)" \
    && make -j"$(nproc)" install \
    # Rename the library to libinternalproj
    && mv /usr/local/lib/libproj.so.15.0.0 /usr/local/lib/libinternalproj.so.15.0.0 \
    && rm /usr/local/lib/libproj.so* \
    && rm /usr/local/lib/libproj.la \
    && ln -s libinternalproj.so.15.0.0 /usr/local/lib/libinternalproj.so.15 \
    && ln -s libinternalproj.so.15.0.0 /usr/local/lib/libinternalproj.so \
    \
# Get latest GDAL source
    && mkdir -p "${SOURCE_DIR}" \
    && cd "${SOURCE_DIR}" \
    && wget "http://download.osgeo.org/gdal/${GDAL_VERSION}/gdal-${GDAL_VERSION}.tar.gz" \
    && tar -xvf "gdal-${GDAL_VERSION}.tar.gz" \
    \
# Compile and install GDAL
    && cd "gdal-${GDAL_VERSION}" \
    && export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH \
    && ./configure \
            --with-python \
            --with-curl \
            --with-openjpeg \
            --without-libtool \
            --with-proj=/usr/local \
    && make -j"$(nproc)" \
    && make install \
    && ldconfig \
    \
    && cd /usr/local \
    \
# Clean up
    && apt-get update -y \
    && apt-get remove -y --purge build-essential wget \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf "${SOURCE_DIR}"


ARG BUIILD_PACKAGES="vim bzip2 unzip make gcc g++ git libglib2.0-0 libsm6 libxrender1"

RUN apt-get update && \
  apt-get install -y $BUIILD_PACKAGES && \
  apt-get install -y grass grass-doc && \
  rm -rf /var/lib/apt/lists/*

ADD setup.py setup.py
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip uninstall gdal -y
RUN pip install GDAL==$(gdal-config --version) --global-option=build_ext --global-option="-I/usr/include/gdal"
ENV GDAL_DATA=/usr/share/gdal/

COPY . /code
WORKDIR /code

RUN grass --text -c EPSG:4326 grass_data/LatLon/

ENV PYTHONPATH /code

ENTRYPOINT ["/code/docker_entrypoint.sh"]