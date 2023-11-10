#!/bin/bash

# Source the .env file to load the environment variables
if [ -f ".env" ]; then
    source .env
else
    echo ".env file not found. Make sure it's in the same directory as this script."
    exit 1
fi

docker compose up -d

# Use environment variables to set ports and core name
SOLR_PORT="${SOLR_PORT:-8983}"  # Default to 8983 if not set in .env

# Split the list into an array
IFS=',' read -ra cores <<< "$CORES"
IFS=',' read -ra schemas <<< "$SCHEMA_FILES"
IFS=',' read -ra files <<< "$DATA_FILES"

for ((i = 0; i < ${#cores[@]}; i++)); do
    core="${cores[i]}"
    schema="${schemas[i]}"
    file="${files[i]}"

    # Delete core
    curl -X DELETE "http://localhost:$SOLR_PORT/solr/admin/cores?action=UNLOAD&core=$core&deleteDataDir=true&deleteIndex=true&deleteInstanceDir=true"

    # Create core
    docker exec my_solr solr create_core -c $core 
    
    # Post schema
    curl -X POST -H 'Content-type:application/json' \
        --data-binary "@./json/$schema" \
        "http://localhost:$SOLR_PORT/solr/$core/schema"

    # Post data
    curl -X POST -H 'Content-type:application/json' \
        --data-binary "@./json/$file" \
        http://localhost:$SOLR_PORT/solr/$core/update?commit=true
done

