import requests
import logging
import os
import pickle
import base64
import json
from requests.exceptions import ConnectionError
from pathlib import Path

_logger = logging.getLogger(__name__)

NTCORE_WORKSPACE_ID = 'NTCORE_WORKSPACE_ID'
NTCORE_HOST = os.getenv('NTCORE_HOST') if os.getenv('NTCORE_HOST') is not None else 'http://localhost:8180'
BASE_URL = '{ntcore_host}/dsp/api/v1/workspace/{workspace_id}/experiment'
VAR_SEPARATOR = '='


def set_workspace_id(workspace_id):
    """
    Sets global workspace id.
    """
    os.environ[NTCORE_WORKSPACE_ID] = workspace_id
    

def print_workspace_id():
    """
    Prints the current workspace id.
    """
    print(_get_workspace_id())


def _get_workspace_id():
    """
    Retrieves workspace id.
    """
    try:
        workspace_id = os.environ[NTCORE_WORKSPACE_ID]
        return workspace_id
    except Exception as e:
        pass
    
    try:
        var_file_path = os.path.join(Path.home(), '.ntcorevar')
        var_list = map(lambda l: l.split(VAR_SEPARATOR, 1), filter(lambda l: VAR_SEPARATOR in l, open(var_file_path)))
        var_map = { t[0].strip(): t[1].strip() for t in var_list }
        return var_map[NTCORE_WORKSPACE_ID] if NTCORE_WORKSPACE_ID in var_map else None
    except Exception as e:
        _logger.warning('Unable to parse ntcore vars: {0}.'.format(e))
        return


def _get_runtime_version():
    """
    Retrieves runtime version.
    """
    try:
        runtime_version = os.environ["DSP_RUNTIME_VERSION"]
        return runtime_version
    except Exception as e:
        _logger.warning("Please set env variable 'DSP_RUNTIME_VERSION'. Acceptable values are 'python-3.7', 'python-3.8' and 'python-3.9'.")
        return


def _emit_model_to_ntcore(estimator, framework, parameters, metrics):
    """
    Sends metrics to ntcore server.
    """
    workspace_id = _get_workspace_id()
    if workspace_id is None:
        _logger.warning('This experiment is not logged because no workspace id is found. You can use mflow.set_workspace_id(...) to set the workspace id.')
        return

    endpoint = BASE_URL.format(ntcore_host=NTCORE_HOST, workspace_id=workspace_id)
    model_blob = pickle.dumps(estimator)
    payload = { "runtime": _get_runtime_version(),
                "framework": framework,
                "parameters": json.dumps(parameters),
                "metrics": json.dumps(metrics), 
                "model": base64.b64encode(model_blob) }
    try:
        requests.post(endpoint, data=payload)
    except ConnectionError as connectionError:
        _logger.warning('This experiment is not logged in ntcore server because ntcore server is not running.')