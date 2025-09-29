#!/bin/bash

set -e

git pull

STACK_NAME=soliso
TIMESTAMP=$(date +%Y%m%d%H%M%S)

VALID_COMPONENTS=("backend" "frontend" "admin" "proxy")

# Funzione per controllare se un elemento è in un array
function is_valid_component() {
    local input=$1
    for valid in "${VALID_COMPONENTS[@]}"; do
        if [[ "$input" == "$valid" ]]; then
            return 0
        fi
    done
    return 1
}

# Se non viene passato alcun argomento, builda e deploya tutto
if [ $# -eq 0 ]; then
    COMPONENTS=("${VALID_COMPONENTS[@]}")
else
    COMPONENTS=()
    for arg in "$@"; do
        if is_valid_component "$arg"; then
            COMPONENTS+=("$arg")
        else
            echo "❌ Errore: componente non valido '$arg'"
            echo "👉 I componenti validi sono: ${VALID_COMPONENTS[*]}"
            exit 1
        fi
    done
fi

for COMPONENT in "${COMPONENTS[@]}"; do
    IMAGE_TAG="soliso-$COMPONENT:$TIMESTAMP"
    echo "📦 Building $COMPONENT image..."
    docker build -t "$IMAGE_TAG" "./$COMPONENT"

    echo "🐳 Updating $COMPONENT service..."
    docker service update --image "$IMAGE_TAG" "${STACK_NAME}_$COMPONENT"
done

echo "✅ Deployment complete!"
