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
import sys

import papermill as pm
import pulumi
import pulumi_datarobot as datarobot
import yaml

sys.path.append("..")

from infra import (
    settings_app,
    settings_main,
)
from infra.settings_deployment import (
    deployment_args,
)
from infra.settings_main import model_training_nb_path, model_training_output_path
from starter.i18n import LocaleSettings
from starter.resources import (
    app_env_name,
    app_locale,
    deployment_env_name,
    scoring_dataset_env_name,
)
from starter.schema import AppSettings

LocaleSettings().setup_locale()

if not model_training_output_path.exists():
    pulumi.info("Executing model training notebook...")
    pm.execute_notebook(
        model_training_nb_path,
        output_path=None,
        cwd=model_training_nb_path.parent,
        log_output=False,
        progress_bar=False,
        stderr_file=sys.stderr,
        stdout_file=sys.stdout,
    )
else:
    pulumi.info(
        f"Using existing model training outputs in '{model_training_output_path}'"
    )
with open(model_training_output_path) as f:
    model_training_output = AppSettings(**yaml.safe_load(f))

prediction_environment = datarobot.PredictionEnvironment(
    **settings_main.prediction_environment_args,
)

deployment = datarobot.Deployment(
    prediction_environment_id=prediction_environment.id,
    registered_model_version_id=model_training_output.registered_model_version_id,
    **deployment_args.model_dump(),
    use_case_ids=[model_training_output.use_case_id],
)

app_runtime_parameters = [
    datarobot.ApplicationSourceRuntimeParameterValueArgs(
        key=deployment_env_name,
        type="deployment",
        value=deployment.id,
    ),
    datarobot.ApplicationSourceRuntimeParameterValueArgs(
        key=scoring_dataset_env_name,
        type="string",
        value=model_training_output.training_dataset_id,
    ),
    datarobot.ApplicationSourceRuntimeParameterValueArgs(
        key=app_locale, type="string", value=LocaleSettings().app_locale
    ),
]

application_source = datarobot.ApplicationSource(
    files=settings_app.get_app_files(app_runtime_parameters),
    runtime_parameter_values=app_runtime_parameters,
    **settings_app.app_source_args,
)

app = datarobot.CustomApplication(
    resource_name=settings_app.app_resource_name,
    source_version_id=application_source.version_id,
    use_case_ids=[model_training_output.use_case_id],
)

app.id.apply(settings_app.ensure_app_settings)


pulumi.export(scoring_dataset_env_name, model_training_output.training_dataset_id)
pulumi.export(deployment_env_name, deployment.id)
pulumi.export(app_env_name, app.id)
pulumi.export(settings_app.app_resource_name, app.application_url)
