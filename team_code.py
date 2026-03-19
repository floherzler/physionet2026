#!/usr/bin/env python

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(SCRIPT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from physionet2026.challenge_pipeline import (  # noqa: E402
    load_challenge_model,
    predict_record,
    train_challenge_model,
)


def train_model(data_folder, model_folder, verbose):
    train_challenge_model(data_folder, model_folder, verbose)


def load_model(model_folder, verbose):
    return load_challenge_model(model_folder, verbose)


def run_model(model, record, data_folder, verbose):
    return predict_record(model, record, data_folder, verbose)
