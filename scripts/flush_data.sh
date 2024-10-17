#!/usr/bin/bash

apps=(
    "../apps/config"
    "../apps/contas"
    "../apps/controle_portao"
    "../apps/dispositivos"
    "../apps/historico"
    "../apps/recados"
)

rm -rf ../db.sqlite3

for app in "${apps[@]}"; do
    rm -rf "$app"/migrations/*
    touch "$app"/migrations/__init__.py
done
