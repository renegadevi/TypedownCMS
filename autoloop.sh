#!/bin/sh

# autoloop.sh
#
# A simple portable shell-script wrapper in order to keep the python application
# or script alive. If something happens, the child-process will be restarted
# which does not affect this parent-process.
#
# This is also a simple deployment-solution where you do not have to setup
# system-wide/specific solutions such as nginx, daemons etc.
#

while true; do

    # Notify each time it loops
    echo "+-------------------------------------------------------------+"
    echo "|              +++    STARTING SERVER    +++                  |"
    echo "+-------------------------------------------------------------+"

    # Execute python application
    python3 main.py

done
