"""
This file includes global test configuration.

In particular, it defines the location where test data is available.
"""
from pathlib import Path

import pytest

from psipy.data import sample_data

test_data_dir = (Path(__file__) / '..' / '..' / 'data').resolve()


@pytest.fixture(scope="module", params=['mas_helio', 'mas_hdf5'])
def mas_directory(request):
    if request.param == 'mas_helio':
        # Check for and download data if not present
        directory = sample_data.mas_helio()
    else:
        # Directories with MAS outputs
        directory = test_data_dir / request.param
    if not directory.exists():
        pytest.xfail(f'Could not find MAS data directory at {directory}')

    return directory


@pytest.fixture(scope="module")
def pluto_directory():
    # Directories with PLUTO outputs
    directory = test_data_dir / 'pluto'
    if not directory.exists():
        pytest.xfail(f'Could not find PLUTO data directory at {directory}')

    return directory
