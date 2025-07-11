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

# type: ignore
import sys

import datarobot as dr
import streamlit as st

sys.path.append("..")

import helpers
from streamlit_theme import st_theme

from starter.api import (
    deployment_id,
    get_app_settings,
    get_app_urls,
    scoring_dataset_id,
)
from starter.i18n import gettext

app_settings = get_app_settings()


def render_header() -> None:
    with open("./style.css") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

    theme = st_theme()
    title_image = "./DataRobot_white.svg"
    if theme and theme.get("base") == "light":
        title_image = "./DataRobot_black.svg"

    with st.container(key="datarobot-logo"):
        logo, _ = st.columns([1, 2])
        logo.image(title_image, width=200)

    st.title(app_settings.page_title)
    st.write(app_settings.page_description)


def render_select_options() -> None:
    with st.form("Query parameters"):
        st.write(gettext("Select the deployment and scoring dataset to use:"))
        explanations, sample_rows = st.columns([1, 1])
        number_of_explanations = explanations.number_input(
            gettext("Number of explanations to generate"),
            min_value=1,
            value=3,
            max_value=10,
        )
        rows_to_sample = sample_rows.number_input(
            gettext("Number of rows to score on"),
            min_value=1,
            value=100,
            max_value=1000,
        )
        run_prediction = st.form_submit_button(gettext("Submit"))
        return number_of_explanations, rows_to_sample, run_prediction


def create_link(label: str, link: str) -> str:
    return f""":blue-background[{label}]  
            {link}"""


def render_sidebar() -> None:
    urls = get_app_urls()
    with st.sidebar:
        st.header(gettext("Project details:"))
        st.markdown(create_link(gettext("Use case:"), urls.use_case))
        st.markdown(create_link(gettext("Project:"), urls.project))
        st.markdown(create_link(gettext("Deployment:"), urls.deployment))


def main():
    client = dr.Client()
    client.headers["Connection"] = "close"
    deployment = dr.Deployment.get(deployment_id)
    with st.spinner(gettext("Retrieving scoring data...")):
        st.session_state["scoring_data"] = helpers.retrieve_scoring_data(
            scoring_dataset_id, app_settings.target
        )

    render_header()
    render_sidebar()

    with st.expander(gettext("Scoring data")):
        st.write(st.session_state["scoring_data"])
    n_explanations, rows_to_sample, run_prediction = render_select_options()

    if run_prediction:
        with st.spinner(gettext("Making predictions...")):
            predictions = helpers.make_predictions(
                deployment,
                st.session_state["scoring_data"],
                max_explanations=n_explanations,
                rows_to_sample=rows_to_sample,
            )
        st.session_state["predictions"] = predictions.dataframe

    if "predictions" in st.session_state:
        st.write(st.session_state["predictions"])


if __name__ == "__main__":
    st.set_page_config(
        page_title=app_settings.page_title,
        page_icon="./datarobot_favicon.png",
        initial_sidebar_state="collapsed",
    )
    main()
