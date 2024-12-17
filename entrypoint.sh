#!/bin/bash
# Navigate into the correct subdirectory and start the application
cd /srv/witoil-for-imagine || exit 1
exec deep-start "$@"