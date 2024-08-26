#!/bin/bash

eval "$(conda shell.bash hook)"
conda activate atari
python scripts/play.py
