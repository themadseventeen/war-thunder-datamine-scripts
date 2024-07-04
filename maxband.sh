#/bin/bash

# Returns the biggest radar band current RWRs can detect

cd "$1"
rg --no-filename "band[0-9]+\": true" | tr -d ' ' | tr -d ',' | sort | uniq | sed -e 's/\"//g' | sed -e 's/band//g' | sed -e 's/:true//' | sort -g | tail -n 1