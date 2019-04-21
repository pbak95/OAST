#!/bin/bash
find . -iname "*.py" | xargs pylint --disable=C0111
