#! /usr/bin/env bash

git pull
pipenv install
systemctl restart tax-back
