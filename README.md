# Predictive AI Starter

This application template outlines a basic Predictive AI deployment workflow in DataRobot. It is a good starter for making a new recipe. DataRobot recommends modifying this README to include information about the template you are creating.
You should include a **summary** of your template as well as some **examples** of pipeline changes.

> [!WARNING]
> Application templates are intended to be starting points that provide guidance on how to develop, serve, and maintain AI applications.
> They require a developer or data scientist to adapt and modify them to meet business requirements before being put into production.

![Using Predictive AI Starter](https://s3.us-east-1.amazonaws.com/datarobot_public/drx/recipe_gifs/predictiveai.gif)

## Table of Contents
1. [Setup](#setup)
2. [Architecture overview](#architecture-overview)
3. [Why build AI Apps with DataRobot app templates?](#why-build-ai-apps-with-datarobot-app-templates)
4. [Make changes](#make-changes)
   - [Change the data and how the model is trained](#change-the-data-and-how-the-model-is-trained)
   - [Change the front-end](#change-the-front-end)
   - [Change the language in the front-end](#change-the-language-in-the-front-end)
5. [Share results](#share-results)
6. [Delete all resources](#delete-all-provisioned-resources)
7. [Setup for advanced users](#setup-for-advanced-users)
8. [Data privacy](#data-privacy)

## Setup

### Quickstart with DataRobot CLI

#### 1. Install the DataRobot CLI

If you haven't already, install the DataRobot CLI by following the installation instructions at:  
https://github.com/datarobot-oss/cli?tab=readme-ov-file#installation

#### 2. Start the Application

Run the following command to start the local development environment. An interactive wizard will guide you through the selection of configuration options, including creating a `.env` file in the root directory and populating it with environment variables you specify during the wizard.

```sh
dr start
```

The DataRobot CLI (`dr`) will:
- Guide you through configuration setup
- Create and populate your `.env` file with the necessary environment variables
- Deploy your application to DataRobot
- Display a link to your running application when complete

When deployment completes, the terminal will display a link to your running application.  
👉 **Click the link to open and start using your app!**

### Manual Setup (Alternative)

If you prefer to set up manually without the CLI wizard, follow these steps:

> [!IMPORTANT]
> If you are running this template in a DataRobot codespace, `pulumi` is already configured and the repository is automatically cloned;
> skip to **Step 3**.

1. If `pulumi` is not already installed, install the CLI following instructions [here](https://www.pulumi.com/docs/iac/download-install/).
   After installing `pulumi` for the first time, restart your terminal and run:

   ```sh
   pulumi login --local  # omit --local to use Pulumi Cloud (requires separate account)
   ```

2. Clone the template repository.

   ```sh
   git clone https://github.com/datarobot-community/predictive-ai-starter
   cd predictive-ai-starter
   ```

3. Rename the file `.env.template` to `.env` in the root directory of the repo and populate your credentials.

   ```sh
   DATAROBOT_API_TOKEN=...
   DATAROBOT_ENDPOINT=...  # e.g. https://app.datarobot.com/api/v2
   PULUMI_CONFIG_PASSPHRASE=...  # required, choose an alphanumeric passphrase to be used for encrypting pulumi config
   ```
   Use the following resources to locate the required credentials:
   - **DataRobot API Token**: Refer to the *Create a DataRobot API Key* section of the [DataRobot API Quickstart docs](https://docs.datarobot.com/en/docs/api/api-quickstart/index.html#create-a-datarobot-api-key).
   - **DataRobot Endpoint**: Refer to the *Retrieve the API Endpoint* section of the [DataRobot API Quickstart docs](https://docs.datarobot.com/en/docs/api/api-quickstart/index.html#retrieve-the-api-endpoint).

4. In a terminal, run the following command:

   ```sh
   python quickstart.py YOUR_PROJECT_NAME  # Windows users may have to use `py` instead of `python`
   ```
   Python 3.9+ is required.

Advanced users who want to control virtual environment creation, dependency installation, environment variable setup
and `pulumi` invocation, see [the advanced setup instructions](#setup-for-advanced-users).

## Architecture overview

![Guarded RAG architecture](https://s3.amazonaws.com/datarobot_public/drx/recipe_gifs/recipe-template.svg)

App Templates contain three families of complementary logic. For this template, you can [opt-in](#make-changes) to fully 
custom AI logic and a fully custom front-end or utilize DataRobot's off-the-shelf offerings:

- **AI logic**: Necessary to service AI requests, generate predictions, and manage predictive models.

  ```
  notebooks/  # Model training logic
  ```
- **App logic**: Necessary for user consumption, whether via a hosted front-end or integrating into an external consumption layer.
  ```
  frontend/  # Streamlit frontend
  ```
- **Operational logic**: Necessary to turn on all DataRobot assets.
  ```
  infra/  # Settings for resources and assets to be created in DataRobot
  infra/__main__.py  # Pulumi program for configuring DataRobot to serve and monitor AI and App logic
  ```

## Why build AI Apps with DataRobot app templates?

App templates transform your AI projects from notebooks to production-ready applications. Too often, getting models into production means rewriting code, juggling credentials, and coordinating with multiple tools and teams just to make simple changes. DataRobot's composable AI apps framework eliminates these bottlenecks, letting you spend more time experimenting with your ML and app logic and less time wrestling with plumbing and deployment.

- Start building in minutes: Deploy complete AI applications instantly, then customize AI logic or front-end independently - no architectural rewrites needed.
- Keep working your way: Data scientists keep working in notebooks, developers in IDEs, and configs stay isolated - update any piece without breaking others.
- Iterate with confidence: Make changes locally and deploy with confidence - spend less time writing and troubleshooting plumbing, more time improving your app.

Each template provides an end-to-end AI architecture, from raw inputs to deployed application, while remaining highly customizable for specific business requirements.

## Make changes

### Change the data and how the model is trained

1. Edit the following notebook:
   - `notebooks/train_model.ipynb`: Handles training data ingest and preparation and model training settings.

   The last cell of the notebook is required, as it writes outputs needed for the rest of the pipeline.
2. Run the revised notebook.
3. Run `pulumi up` to update your stack with these changes.

   ```sh
   source set_env.sh  # On windows use `set_env.bat`
   pulumi up
   ```

### Change the front-end

1. Ensure you have already run `pulumi up` at least once (to provision the time series deployment).
2. Streamlit assets are in `frontend/` and can be edited. After provisioning the stack
   at least once, you can also test the front-end locally using `streamlit run app.py` from the
   `frontend/` directory (don't forget to initialize your environment using `source set_env.sh`).
3. Run `pulumi up` again to update your stack with the changes.

   ```sh
   source set_env.sh  # On windows use `set_env.bat`
   pulumi up
   ```

#### Change the language in the front-end

Optionally, you can set the application locale in `meta_template/i18n.py`, e.g. `APP_LOCALE = LanguageCode.JA`. Supported locales are Japanese and English, with English set as the default.

## Share results

1. Log into the DataRobot application.
2. Navigate to **Registry > Applications**.
3. Navigate to the application you want to share, open the actions menu, and select **Share** from the dropdown.

## Delete all provisioned resources

```sh
pulumi down
```

Then run the jupyter notebook `notebooks/delete_non_pulumi_assets.ipynb`.

## Setup for advanced users

For manual control over the setup process, adapt the following steps for MacOS/Linux to your environent:

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
source set_env.sh
pulumi stack init YOUR_PROJECT_NAME
pulumi up 
```

e.g., for Windows/conda/cmd.exe the previous example would change to the following:

```sh
conda create --prefix .venv pip
conda activate .\.venv
pip install -r requirements.txt
set_env.bat
pulumi stack init YOUR_PROJECT_NAME
pulumi up 
```

For projects that will be maintained, DataRobot recommends forking the repo so upstream fixes and improvements can be merged in the future.

## Data privacy

Your data privacy is important to DataRobot. Data handling is governed by the DataRobot [Privacy Policy](https://www.datarobot.com/privacy/). Review the policy before using your own data with DataRobot.

