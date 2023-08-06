#!/usr/bin/python
#
# Copyright 2020 A.L.I Technologies
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# -*- coding: utf-8 -*-

import setuptools
import sys

if sys.version_info[:2] < (3, 6):
    raise RuntimeError("Python version >= 3.6 required.")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycosmosapi",
    version="0.0.2",
    author="A.L.I Technologies",
    author_email="benjamin.ioller@ali.jp",
    description="Telemetry helper for Cosmos API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://dmtest.cosmos.ali.jp/docapi",
    packages=setuptools.find_packages(),
    license='Apache 2.0',
    keywords=['cosmos', 'pycosmos'],
    python_requires='>=3.6',
    install_requires=[
       "requests>=2.23.0",
   ],
)