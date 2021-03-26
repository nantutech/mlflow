import requests
import logging
import os
import pickle
import base64
import json
from requests.exceptions import ConnectionError

_logger = logging.getLogger(__name__)

NTCORE_HOST = os.getenv('NTCORE_HOST') is not None or 'http://localhost:8180'
BASE_URL = '{ntcore_host}/dsp/api/v1/workspace/{workspace_id}/experiment'


def set_workspace_id(workspace_id):
    """
    Set global workspace id.
    """
    os.environ['NTCORE_WORKSPACE_ID'] = workspace_id
    _logger.info('NTCORE_WORKSPACE_ID={0}'.format(os.environ['NTCORE_WORKSPACE_ID']))
    

def _emit_model_to_ntcore(estimator, parameters, metrics):
    """
    Sends metrics to ntcore server.
    """
    workspace_id = os.environ['NTCORE_WORKSPACE_ID']
    endpoint = BASE_URL.format(ntcore_host=NTCORE_HOST, workspace_id=workspace_id)
    model_blob = pickle.dumps(estimator)
    payload = { "parameters": json.dumps(parameters),
                "metrics": json.dumps(metrics), 
                "model": base64.b64encode(model_blob) }
    try:
        requests.post(endpoint, data=payload)
    except ConnectionError as connectionError:
        _logger.warning('ntcore server is not up.')