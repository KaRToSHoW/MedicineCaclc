# PowerShell script to start Expo on Windows
# Equivalent to start-expo.sh for Unix/Linux systems

$EXPO_PORT = if ($env:EXPO_WEB_PORT) { $env:EXPO_WEB_PORT } else { "3000" }

# Only set EXPO_PACKAGER_PROXY_URL if CLACKY_PREVIEW_DOMAIN_BASE is defined
if ($env:CLACKY_PREVIEW_DOMAIN_BASE) {
    # Preview domain: http://3000.preview.example.com (no port suffix)
    $env:EXPO_PACKAGER_PROXY_URL = "http://${EXPO_PORT}${env:CLACKY_PREVIEW_DOMAIN_BASE}"
}
# Otherwise use default Expo behavior (auto-detect IP for LAN access)

# Run expo start with arguments
& ./node_modules/.bin/expo.cmd start @args --port $EXPO_PORT
