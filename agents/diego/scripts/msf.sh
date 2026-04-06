#!/bin/bash
# Diego's Metasploit Launcher
# Usage: ./msf.sh [command]
# Or interactively: ./msf.sh

if [ "$1" ]; then
    # Execute single command
    docker run --rm --entrypoint /usr/src/metasploit-framework/msfconsole \
        metasploitframework/metasploit-framework \
        -q -x "$1; exit"
else
    # Interactive mode
    docker run -it --rm \
        --entrypoint /usr/src/metasploit-framework/msfconsole \
        metasploitframework/metasploit-framework
fi
