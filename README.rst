=======================================================
nantutech/MLFlow: A Machine Learning Lifecycle Platform
=======================================================
This repository decorates the MLFlow library with a set of utilities to maintain machine leanring models in the NTCORE platform.

Installing
----------
Clone this repository via ``git clone https://github.com/nantutech/mlflow.git mlflow-nantu``

Install MLflow from PyPI via ``pip3 install mlflow-nantu/``

Launching the Tracking UI (Optional)
------------------------------------
Prerequisite
------------
Follow this [instruction](https://docs.docker.com/get-started/#download-and-install-docker) to download and install the Docker engine.

Cloning this repository
-----------------------
Clone this repository via ``git clone https://github.com/dsp-columbus/ntcore.git``

Building frontend assets 
------------------------
    cd webapp/
    npm install
    npm run build

Starting ntcore server
----------------------
    cd ../
    npm install
    npm run dev

Training a model 
----------------
Follow the below example to train a machine learning/AI model::

    import numpy as np
    from sklearn.linear_model import LinearRegression
    import mlflow

    # This step is required if you need to log the experiment in the ntcore server.
    # The workspace id can be found after creating a workspace via the ntcore UI.
    mlflow.set_workspace_id(id)
    # enable autologging
    mlflow.sklearn.autolog()

    # prepare training data
    X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
    y = np.dot(X, np.array([1, 2])) + 3

    # train a model
    model = LinearRegression()
    with mlflow.start_run() as run:
        model.fit(X, y)

Saving and Serving Models
-------------------------
Login your ntcore server in your web browser at localhost:8180 (default), select an experiment version in the workspace and deploy the model via UI.
