# Copyright 2024 DataRobot, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import annotations

import datarobot as dr
import numpy as np
import pandas as pd
import streamlit as st
from datarobot_predict.deployment import PredictionResult, predict


@st.cache_data(show_spinner=False)
def retrieve_scoring_data(dataset_id: str, target: str) -> pd.DataFrame:
    return dr.Dataset.get(dataset_id).get_as_dataframe().drop(columns=[target])


@st.cache_data(show_spinner=False)
def make_predictions(
    _deployment: dr.Deployment,
    dataset: pd.DataFrame,
    max_explanations: int = 5,
    rows_to_sample: int = 100,
    random_seed: int = 42,
) -> PredictionResult:
    """Make predictions using the specified deployment and dataset."""
    np.random.seed(random_seed)
    scoring_data = dataset.sample(n=rows_to_sample)
    return predict(
        deployment=_deployment,
        data_frame=scoring_data,
        max_explanations=max_explanations,
    )
