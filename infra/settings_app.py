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
import textwrap
from pathlib import Path
from typing import List, Tuple

import datarobot as dr
import pulumi
import pulumi_datarobot as datarobot
from datarobot_pulumi_utils.schema.apps import ApplicationSourceArgs
from datarobot_pulumi_utils.schema.exec_envs import RuntimeEnvironments

from infra.settings_main import (
    PROJECT_ROOT,
    application_path_str,
    model_training_nb_output_name,
    model_training_output_path_str,
    project_name,
    runtime_parameters_spec,
    runtime_parameters_spec_template,
)
from starter.i18n import LanguageCode, LocaleSettings

application_path = Path(application_path_str)

app_source_args = ApplicationSourceArgs(
    resource_name=f"Predictive AI Starter App Source [{project_name}]",
    base_environment_id=RuntimeEnvironments.PYTHON_312_APPLICATION_BASE.value.id,
).model_dump(mode="json", exclude_none=True)

app_resource_name: str = f"Predictive AI Starter Application [{project_name}]"
application_locale = LocaleSettings().app_locale


def ensure_app_settings(app_id: str) -> None:
    try:
        dr.client.get_client().patch(
            f"customApplications/{app_id}/",
            json={"allowAutoStopping": True},
            timeout=60,
        )
    except Exception:
        pulumi.warn("Could not enable autostopping for the Application")


def _prep_metadata_yaml(
    runtime_parameter_values: List[
        datarobot.ApplicationSourceRuntimeParameterValueArgs
    ],
) -> None:
    from jinja2 import BaseLoader, Environment

    runtime_parameter_specs = "\n".join(
        [
            textwrap.dedent(
                f"""\
            - fieldName: {param.key}
              type: {param.type}
        """
            )
            for param in runtime_parameter_values
        ]
    )
    with open(application_path / runtime_parameters_spec_template) as f:
        template = Environment(loader=BaseLoader()).from_string(f.read())
    (application_path / runtime_parameters_spec).write_text(
        template.render(
            additional_params=runtime_parameter_specs,
        )
    )


def get_app_files(
    runtime_parameter_values: List[
        datarobot.ApplicationSourceRuntimeParameterValueArgs
    ],
) -> List[Tuple[str, str]]:
    _prep_metadata_yaml(runtime_parameter_values)

    starter_path = PROJECT_ROOT / "starter"

    source_files = [
        (str(f), str(f.relative_to(application_path)))
        for f in application_path.glob("**/*")
        if f.is_file()
        and f.name != runtime_parameters_spec_template
        and model_training_nb_output_name not in f.name
    ] + [
        (str(starter_path / "schema.py"), "starter/schema.py"),
        (str(starter_path / "api.py"), "starter/api.py"),
        (str(starter_path / "resources.py"), "starter/resources.py"),
        (str(starter_path / "i18n.py"), "starter/i18n.py"),
        (
            model_training_output_path_str,
            model_training_nb_output_name,
        ),
    ]

    if application_locale != LanguageCode.EN:
        source_files.append(
            (
                str(
                    starter_path
                    / "locale"
                    / application_locale
                    / "LC_MESSAGES"
                    / "base.mo"
                ),
                f"starter/locale/{application_locale}/LC_MESSAGES/base.mo",
            )
        )

    return source_files
