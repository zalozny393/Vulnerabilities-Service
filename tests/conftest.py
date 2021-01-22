import json
from pathlib import Path

import boto3
import pytest


@pytest.fixture
def json_loader():
    def _loader(filename):
        base_path = Path(__file__).parent
        file_path = (base_path / 'events' / filename).resolve()
        with open(file_path, 'r') as f:
            return json.load(f)
    return _loader


@pytest.fixture
def env_variables(monkeypatch):
    monkeypatch.setenv('STAGE', 'test')
    monkeypatch.setenv('BUCKET_NAME', 'local-bucket')
    monkeypatch.setenv('OBJECT_KEY', 'vulnerabilities.csv')
