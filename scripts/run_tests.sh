#!/usr/bin/env bash
export PYTHONPATH=$PYTHONPATH:.:./libraries
pipenv run python libraries/pynetest/cli.py agile_ai_tests
