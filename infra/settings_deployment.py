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


import pulumi_datarobot as datarobot

from .common.schema import (
    DeploymentArgs,
)
from .settings_main import project_name

deployment_args = DeploymentArgs(
    resource_name=f"Predictive AI Starter Deployment [{project_name}]",
    label=f"Predictive AI Starter Deployment [{project_name}]",
    predictions_settings=(
        datarobot.DeploymentPredictionsSettingsArgs(min_computes=0, max_computes=1)
    ),
    predictions_data_collection_settings=datarobot.DeploymentPredictionsDataCollectionSettingsArgs(
        enabled=True
    ),
    drift_tracking_settings=datarobot.DeploymentDriftTrackingSettingsArgs(
        feature_drift_enabled=True, target_drift_enabled=True
    ),
)
