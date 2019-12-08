#!/usr/bin/env bash
# -*- coding: utf-8 -*-

export PROJECT_NAME=foottrial

export PYTHON_VERSION=2.7.9
export PYENV_NAME="${PROJECT_NAME}"

export GVM_NAME="${PROJECT_NAME}"
export GVM_PATHS_NAME=(
    "src"
    "pkg"
    "bin"
)

# Vars Dir
export ROOT_DIR
ROOT_DIR=$(pwd)
export RESOURCES_DIR="$ROOT_DIR/resources"
export RESOURCES_DB_DIR="$RESOURCES_DIR/db"
export REQUIREMENTS_DIR="${ROOT_DIR}/requirements/"
export SOURCE_DIR="${ROOT_DIR}/src/"
export STATIC_DIR="$SOURCE_DIR/staticfiles/"
