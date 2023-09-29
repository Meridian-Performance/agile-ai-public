#!/usr/bin/env bash
echo "Starting Xvfb to enable headless rendering"
Xvfb :99 -screen 0 1280x1024x24&
