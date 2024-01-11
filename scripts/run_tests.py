#!/usr/bin/env bash
import os
from pathlib import Path

from pynetest import cli
import sys

base_directory = str(Path(__file__).parent.parent)
os.chdir(base_directory)
sys.argv.append("agile_ai_tests")
cli.main()
