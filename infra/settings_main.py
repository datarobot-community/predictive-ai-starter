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
from pathlib import Path

from datarobot_pulumi_utils.pulumi.stack import get_stack
from datarobot_pulumi_utils.schema.common import UseCaseArgs
from datarobot_pulumi_utils.schema.custom_models import (
    PredictionEnvironmentArgs,
    PredictionEnvironmentPlatforms,
)

project_name = get_stack()

prediction_environment_args = PredictionEnvironmentArgs(
    resource_name=f"Predictive AI Starter Prediction Environment [{project_name}]",
    platform=PredictionEnvironmentPlatforms.DATAROBOT_SERVERLESS,
).model_dump(mode="json", exclude_none=True)


use_case_args = UseCaseArgs(
    resource_name=f"Predictive AI Starter Use Case [{project_name}]",
    description="Use Case for Predictive AI Starter application",
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent.absolute()

application_path_str = str(PROJECT_ROOT / "frontend")
runtime_parameters_spec_template = "metadata.yaml.jinja"
runtime_parameters_spec = "metadata.yaml"

model_training_nb_name = "train_model.ipynb"
model_training_nb_path = PROJECT_ROOT / "notebooks" / model_training_nb_name
model_training_nb_output_name = "train_model_output.yaml"
model_training_output_name = f"train_model_output.{project_name}.yaml"
model_training_output_path_str = f"{application_path_str}/{model_training_output_name}"
model_training_output_path = Path(model_training_output_path_str)
