#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Start server
echo "Starting server..."
exec "$@" 