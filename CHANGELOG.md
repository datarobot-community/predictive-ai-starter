# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

## [0.3.0] - 2026-01-13

### Added

- Integration with DataRobot CLI for streamlined setup and deployment workflow
- CLI configuration files (`.datarobot/cli/base.yml` and `.datarobot/cli/versions.yaml`)
- Task runner configuration with Taskfile.yaml for streamlined tasks (start, install, lint, dev)
- Frontend-specific Taskfile for modular task management
- CLI-first quickstart instructions in README.md
- Integration with DataRobot Python client 3.9.1 `CustomApplication` and `CustomApplicationSource` entities.
- Dynamic resource fetching from CustomApplicationSource when creating CustomApplications.

### Changed

- Updated quickstart.py to make stack_name optional with interactive prompt
- Modularized task runner configuration with frontend-specific taskfile

## [0.2.0] - 2025-07-14

### New release

## [0.1.6] - 2025-07-11

### Fixed

- Fixed pydantic-settings due for compatibility in 2.9.0
- Fix `tests/e2e` Dockerfile security issues
- Fix prompt column issue by upgrading pulumi-datarobot to 0.10.8

### Changed

- Updated pydantic-settings requirement to >=2.5.2,<2.10
- Improved base Foundational Application template

## [0.1.5] - 2025-04-07

### Added

- Installed [the datarobot-pulumi-utils library](https://github.com/datarobot-oss/datarobot-pulumi-utils) to incorporate majority of reused logic in the `infra.*` subpackages.

### Fixed
- Fix DataRobot URLs for on-premises environments

## [0.1.4] - 2025-03-06

### Fixed
- "Already Registered to Use Case" error fixed by bumping pulumi-datarobot version

## [0.1.3] - 2025-01-15

### Fixed
- Codespace python env no longer broken by quickstart

### Changed

- Move pulumi entrypoint to the infra directory

## [0.1.2] - 2025-01-06

### Changed
- Added python 3.9 requirement to readme

### Added
- Update safe_dump to support unicode

## [0.1.1] - 2024-12-12

### Fixed
- Fix comment handling in quickstart
- quickstart.py now supports multiline values correctly

### Changed
- add 3.9 compatibility check to mypy
- update pulumi-datarobot to >=0.4.5
- quickstart now asks you to change the default project name
- quickstart now prints the application URL

### Added

- Changelog file to keep track of changes in the project
- add context tracing to this recipe.
