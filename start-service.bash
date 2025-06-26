#! /usr/bin/env bash

# <<<< pyenv <<<<
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init - bash)"
# >>>> pyenv >>>>
cd /var/www/tax.each.do/back
exec /usr/bin/pipenv run gunicorn wsgi:app -b '[::]:8082'
