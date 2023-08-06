#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
import os, sys, ast, json, glob, platform
import syst3m

# source.
ALIAS = "encrypti0n"
SOURCE_NAME = "encrypti0n"
VERSION = "v1"
SOURCE_PATH = syst3m.defaults.get_source_path(__file__, back=4)
BASE = syst3m.defaults.get_source_path(SOURCE_PATH)
OS = syst3m.defaults.check_operating_system(supported=["linux", "osx"])
syst3m.defaults.check_alias(alias=ALIAS, executable=f"{SOURCE_PATH}/{VERSION}/")

# file settings.
ADMINISTRATOR = "administrator"
OWNER = os.environ.get("USER")
GROUP = "root"
if OS in ["osx"]: GROUP = "wheel"
SUDO = True
ADMIN_PERMISSION = 700
READ_PERMISSION = 750
WRITE_PERMISSION = 770

