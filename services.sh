#!/bin/bash

# Default values
SERVICE=""
EXECUTING_METHOD="run"
FRONT_VERSION=""
MAIN_API_VERSION=""
LIVE_API_VERSION=""
VIDEO_API_VERSION=""
SCANNER_API_VERSION=""

# Function to display usage information
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "Available options:"
    echo "  --service, -s       <value>  Set the service name"
    echo "  --ex-method, -exm   <value>  Set the executing method (run, stop, or restart) (Default: run)"
    echo "  --front-version     <value>  Set the front-end version"
    echo "  --main-api          <value>  Set the main API version"
    echo "  --live-api          <value>  Set the live API version"
    echo "  --video-api         <value>  Set the video API version"
    echo "  --scanner-api       <value>  Set the scanner API version"
    echo ""
    echo "Example:"
    echo "  $0 --service front --ex-method restart --front-version 1.2.3"
    exit 1
}

# Function to check and set default service versions
check_version() {
    [ -z "$FRONT_VERSION" ] && FRONT_VERSION="v1"
    [ -z "$MAIN_API_VERSION" ] && MAIN_API_VERSION="v1"
    [ -z "$LIVE_API_VERSION" ] && LIVE_API_VERSION="v1"
    [ -z "$VIDEO_API_VERSION" ] && VIDEO_API_VERSION="v1"
    [ -z "$SCANNER_API_VERSION" ] && SCANNER_API_VERSION="v1"
}

# Function to run services
run_services() {
    if [ "$SERVICE" = "front" ]; then
        echo "Building frontend..."
        cd frontend || exit 1
        docker build -t watchman:front-"$FRONT_VERSION" .

        echo "Running frontend..."
        docker run -itd --rm --name watchman-frontend -p 3500:3500 watchman:front-"$FRONT_VERSION"

    elif [ "$SERVICE" = "back" ]; then
        echo "Running backend..."

    elif [ "$SERVICE" = "full" ]; then
        echo "Running full stack..."
    fi
}

# Function to stop services
stop_services() {
    if [ "$SERVICE" = "front" ]; then
        echo "Stopping frontend..."
        docker stop watchman-frontend 2>/dev/null || true
        docker rm watchman-frontend 2>/dev/null || true

        echo "Removing old image..."
        docker rmi watchman:front-"$FRONT_VERSION" 2>/dev/null || true

    elif [ "$SERVICE" = "back" ]; then
        echo "Stopping backend..."

    elif [ "$SERVICE" = "full" ]; then
        echo "Stopping full stack..."
    fi
}

# Check if no arguments are provided
if [ "$#" -eq 0 ]; then
    usage
fi

# Parse command-line arguments
while [ "$#" -gt 0 ]; do
    case "$1" in
        --service|-s)
            SERVICE="$2"
            shift 2
            ;;
        --ex-method|-exm)
            EXECUTING_METHOD="$2"
            shift 2
            ;;
        --front-version)
            FRONT_VERSION="$2"
            shift 2
            ;;
        --main-api)
            MAIN_API_VERSION="$2"
            shift 2
            ;;
        --live-api)
            LIVE_API_VERSION="$2"
            shift 2
            ;;
        --video-api)
            VIDEO_API_VERSION="$2"
            shift 2
            ;;
        --scanner-api)
            SCANNER_API_VERSION="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            usage
            ;;
    esac
done

# Check versions and execute service management
check_version

case "$EXECUTING_METHOD" in
    run)
        stop_services
        run_services
        ;;
    stop)
        stop_services
        ;;
    restart)
        stop_services
        run_services
        ;;
    *)
        echo "Invalid execution method: $EXECUTING_METHOD"
        usage
        ;;
esac
