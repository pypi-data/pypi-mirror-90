#!/usr/bin/env bash
# This file is part of QLKNN-fortran
# You should have received the QLKNN-fortran LICENSE in the root of the project
set -e

export TOOLCHAIN=gcc
export BUILD=debug
export TUBSCFG_MPI=0
export TUBSCFG_MKL=0
export HOSTFULL=docker-debian
export VERBOSE=1
CLEAN=1

MKLS="0 1"
MPIS="0 1"
TOOLCHAINS="gcc intel"

for TOOLCHAIN in $TOOLCHAINS; do
  for TUBSCFG_MKL in $MKLS; do
    for TUBSCFG_MPI in $MPIS; do
      export TOOLCHAIN
      export TUBSCFG_MKL
      export TUBSCFG_MPI
      #env TOOLCHAIN=gcc BUILD=debug TUBSCFG_MPI=0 TUBSCFG_MKL=0 HOSTFULL=docker-debian VERBOSE=1 ./lib/src/fruitsh/fruit.shtests/test_regression.f90
      echo
      echo -------------------------------------------------------------------------------
      echo Building TOOLCHAIN=$TOOLCHAIN TUBSCFG_MKL=$TUBSCFG_MKL TUBSCFG_MPI=$TUBSCFG_MPI
      echo -------------------------------------------------------------------------------
      echo
      if [ $CLEAN == 1 ]; then
        make clean
      fi
      make
      #./lib/src/fruitsh/fruit.sh tests/test_regression.f90
    done
  done
done

#env TOOLCHAIN=gcc BUILD=debug TUBSCFG_MPI=0 TUBSCFG_MKL=0 HOSTFULL=docker-debian VERBOSE=1 ./lib/src/fruitsh/fruit.shtests/test_regression.f90
