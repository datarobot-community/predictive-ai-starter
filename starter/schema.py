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

from pydantic import BaseModel, ConfigDict, Field


class AppSettings(BaseModel):
    """Dynamic, data science settings needed by the application."""

    registered_model_version_id: str = Field(
        description=(
            "ID of the registered model version to be deployed for forecasting"
        )
    )
    registered_model_name: str
    use_case_id: str
    project_id: str
    model_id: str = Field(
        description="ID of the registered model to be deployed for forecasting"
    )
    target: str = Field(description="Name of the target column in the training dataset")
    training_dataset_id: str
    page_description: str
    page_title: str
    model_config = ConfigDict(protected_namespaces=())


class AppUrls(BaseModel):
    use_case: str
    project: str
    deployment: str
