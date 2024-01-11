#!/usr/bin/env bash
BASE_DIR=$(dirname $(dirname $0))
cd $BASE_DIR

echo 
echo "******************************************************"
echo "Initalizing submodule directory " 
echo "******************************************************"
echo 

mkdir -p libraries
mkdir -p repos
git submodule add ssh://git@github.com/kedifei/agile-ai-pyne repos/pynetest
git submodule update --init
echo
echo "******************************************************************"
echo "Make sure to mark directory 'repos' as 'excluded' in pycharm"
echo "******************************************************************"
echo

echo
echo "*****************************************"
echo "Installing pipenv dependencies (with dev)"
echo "*****************************************"
echo

pipenv install --dev

echo
echo "******************************************"
echo "Symlinking repo libraries to libraries    "
echo "******************************************"
echo

ln -sf $PWD/repos/pynetest/pynetest libraries/

echo
echo "**************************************************************************"
echo "Make sure to mark directory 'libraries' as 'sources root' in pycharm"
echo "**************************************************************************"
echo

pwd
export PYTHONPATH=.:libraries:$PYTHONPATH;
pipenv run python ./scripts/setup_cython.py
