#!/usr/bin/env bash
# -*- coding: utf-8 -*-

# shellcheck source=/dev/null
[ -r "script/bootstrap.sh" ] && source "script/bootstrap.sh"

cd "${SOURCE_DIR}" || exit

echo "execute $1"

python manage.py runserver "${DJANGO_IP}:${DJANGO_PORT}"
