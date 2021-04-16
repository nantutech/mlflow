import requests
import logging
import os
import pickle
import base64
import json
from requests.exceptions import ConnectionError

_logger = logging.getLogger(__name__)

NTCORE_HOST = os.getenv('NTCORE_HOST') if os.getenv('NTCORE_HOST') is not None else 'http://localhost:8180'
BASE_URL = '{ntcore_host}/dsp/api/v1/workspace/{workspace_id}/experiment'


def set_workspace_id(workspace_id):
    """
    Set global workspace id.
    """
    os.environ['NTCORE_WORKSPACE_ID'] = workspace_id
    

def _emit_model_to_ntcore(estimator, parameters, metrics):
    """
    Sends metrics to ntcore server.
    """
    try:
        workspace_id = os.environ['NTCORE_WORKSPACE_ID']
    except Exception as envError:
        _logger.warning('This experiment is not logged in ntcore server because no workspace id is found. You can use mflow.set_workspace_id(...) to set the workspace id.')
        return

    endpoint = BASE_URL.format(ntcore_host=NTCORE_HOST, workspace_id=workspace_id)
    model_blob = pickle.dumps(estimator)
    payload = { "parameters": json.dumps(parameters),
                "metrics": json.dumps(metrics), 
                "model": base64.b64encode(model_blob) }
    try:
        requests.post(endpoint, data=payload)
    except ConnectionError as connectionError:
        _logger.warning('This experiment is not logged in ntcore server because ntcore server is not running.')