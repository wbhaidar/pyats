"""
proj2_job.py

pyATS job file to execute the Project 2 test script.
"""

import os
from pyats.easypy import run

def main(runtime):
    """
    Job file entry point.
    This function runs the test script defined in `tests/proj2.py`.
    """

    # Dynamically compute the path to the test script
    test_script_path = os.path.join(os.path.dirname(__file__), '..', 'tests', 'proj2.py')
    test_script_path = os.path.abspath(test_script_path)

    run(
        testscript=test_script_path,
        runtime=runtime
    )
