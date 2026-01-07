@echo off
REM Batch script to start Expo on Windows
REM Equivalent to start-expo.sh for Unix/Linux systems

setlocal enabledelayedexpansion

if defined EXPO_WEB_PORT (
    set EXPO_PORT=%EXPO_WEB_PORT%
) else (
    set EXPO_PORT=3000
)

REM Only set EXPO_PACKAGER_PROXY_URL if CLACKY_PREVIEW_DOMAIN_BASE is defined
if defined CLACKY_PREVIEW_DOMAIN_BASE (
    REM Preview domain: http://3000.preview.example.com (no port suffix)
    set EXPO_PACKAGER_PROXY_URL=http://!EXPO_PORT!!CLACKY_PREVIEW_DOMAIN_BASE!
)
REM Otherwise use default Expo behavior (auto-detect IP for LAN access)

REM Run expo start with arguments
call node_modules\.bin\expo.cmd start %* --port !EXPO_PORT!
