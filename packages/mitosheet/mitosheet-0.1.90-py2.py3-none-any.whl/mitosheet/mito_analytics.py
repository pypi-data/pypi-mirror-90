#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Contains analytics objects; exported here to avoid
circular references!
"""
from typing import List
import analytics
import getpass
import pandas as pd
import os
import sys
from mitosheet._version import __version__

# Write key taken from segement.com
analytics.write_key = '6I7ptc5wcIGC4WZ0N1t0NXvvAbjRGUgX' 
# We case depending on if they are on old or new infrastructure
if getpass.getuser() == 'jovyan': # 'joyvan' is the name of the account on Kuberentes JupyterHub
    static_user_id = os.getenv('JUPYTERHUB_USER')
else:
    static_user_id = getpass.getuser()


def is_local_deployment():
    """
    Helper function for figuring out if this a local deployment or a
    mito server deployment
    """
    user = getpass.getuser()
    on_kuberentes_mito = user == 'jovyan'
    on_tljh_mito = user.startswith('jupyter-')

    return not on_kuberentes_mito and not on_tljh_mito


analytics.identify(static_user_id, {
    'location': __file__,
    'python_version': sys.version_info,
    'mito_version': __version__
}) #TODO: get information to store as traits?


def log(event, properties=None):
    if properties == None:
        properties = {}

    analytics.track(
        static_user_id, 
        event, 
        dict(
            {
               'python_version': sys.version_info,
                'mito_version': __version__ 
            }, 
            **properties
        )
    )


def log_dfs_metadata(dfs: List[pd.DataFrame]):
    """
    A helper function to log metadata about a list of dataframes, 
    that does not pass any sensitive information of the dataframe
    elsewhere.
    """
    try:
        df_shapes = {f'df_{idx}_shape': {'row': df.shape[0], 'col': df.shape[1]} for idx, df in enumerate(dfs)}
        df_headers = {f'df_{idx}_headers': list(df.keys()) for idx, df in enumerate(dfs)}
        df_dtypes = {f'df_{idx}_dtypes': {key: str(df[key].dtype) for key in df.keys()} for idx, df in enumerate(dfs)}

        log('df_metadata_log_event', dict(
            {'df_count': len(dfs)},
            **df_shapes,
            **df_headers,
            **df_dtypes
        ))
    except:
        # We don't mind if logging fails
        pass
