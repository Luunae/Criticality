#!/usr/bin/env bash
setup_env() {
  local poetry_env=$(realpath "$(dirname "$(poetry run which python)")/../")
  echo "Activating $poetry_env"
  source "$poetry_env/Scripts/activate"
}

setup_env
