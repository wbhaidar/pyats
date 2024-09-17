"""
proj2_job.py
<PYATS_JOBFILE>

Description of this job.
"""

import os
from pyats.easypy import run

# compute the script path from this location
SCRIPT_PATH = os.path.dirname(__file__)

def main(runtime):
    '''job file entrypoint'''
    
    # run script
    run(testscript= os.path.join(SCRIPT_PATH, 
                                 'proj2.py'),
        runtime = runtime)
