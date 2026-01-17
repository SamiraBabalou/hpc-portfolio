#!/usr/bin/env python3
# ----------------------------------------------------------------------
# Unit test for plot_metrics.py
# Author: Samira Babalou
# Purpose: Verify that plot_metrics.py runs without errors and generates PNG files
# ----------------------------------------------------------------------

import os
import subprocess


def test_plot_metrics_runs():
    # Run the script
    subprocess.run(["python3", "../plot_metrics.py"], check=True)

    # Check that expected plots exist
    figures = ["runtime_vs_np.png", "speedup_vs_np.png", "efficiency_vs_np.png"]
    for fig in figures:
        path = f"../reports/figures/{fig}"
        assert os.path.exists(path), f"{fig} was not generated"
