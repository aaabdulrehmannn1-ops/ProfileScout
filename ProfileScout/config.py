#!/usr/bin/env python3
"""
ProfileScout Configuration Module
Advanced settings for power users and custom deployments
"""

# ============================================================================
# CORE CONFIGURATION
# ============================================================================

# HTTP Request timeout in seconds
# Increase this if experiencing timeouts on slow connections
HTTP_TIMEOUT = 8

# Number of concurrent threads for platform scanning
# Increase for faster scanning, decrease to avoid rate limiting
MAX_WORKERS = 12

# ============================================================================
# PLATFORM CONFIGURATION
# ============================================================================

# Enable/disable specific platform groups
ENABLE_CODE_PLATFORMS = True           # GitHub, GitLab, Dev.to, etc.
ENABLE_SOCIAL_PLATFORMS = True         # Reddit, Twitter, Instagram, etc.
ENABLE_CREATIVE_PLATFORMS = True       # Medium, Behance, Substack, etc.
ENABLE_VIDEO_PLATFORMS = True          # YouTube, Twitch, TikTok, etc.
ENABLE_MUSIC_PLATFORMS = True          # Spotify, SoundCloud, etc.
ENABLE_GAMING_PLATFORMS = True         # Steam, Discord, etc.

# ============================================================================
# RETRY CONFIGURATION
# ============================================================================

# Automatically retry failed connections
RETRY_ON_TIMEOUT = True
RETRY_ON_CONNECTION_ERROR = True

# Maximum retry attempts per platform
MAX_RETRIES = 2

# Delay between retries (seconds)
RETRY_DELAY = 1

# ============================================================================
# OUTPUT CONFIGURATION
# ============================================================================

# Enable colored terminal output
USE_COLORS = True

# Enable detailed logging
VERBOSE_MODE = False

# Show platform check progress in real-time
SHOW_PROGRESS = True

# ============================================================================
# RATE LIMITING CONFIGURATION
# ============================================================================

# Automatically reduce concurrency if rate-limited
AUTO_REDUCE_WORKERS = True

# Minimum number of workers to keep
MIN_WORKERS = 2

# Delay between requests per platform (seconds)
REQUEST_DELAY = 0

# ============================================================================
# SECURITY CONFIGURATION
# ============================================================================

# Verify SSL certificates (set to False for maximum compatibility)
VERIFY_SSL = False

# Custom User-Agent string
CUSTOM_USER_AGENT = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/120.0.0.0 Safari/537.36'
)

# ============================================================================
# PLATFORM CUSTOMIZATION
# ============================================================================

# Add custom platforms here
CUSTOM_PLATFORMS = {
    # Example format:
    # "CustomPlatform": "https://custom.platform.com/{}",
}

# Platforms to skip during scanning
SKIP_PLATFORMS = [
    # Example:
    # "Discord",  # If Discord is unreliable in your region
]

# ============================================================================
# ADVANCED OPTIONS
# ============================================================================

# Enable HTTP HEAD requests (faster but less reliable)
USE_HEAD_REQUESTS = True

# Fall back to GET if HEAD fails
FALLBACK_TO_GET = True

# Follow redirects
FOLLOW_REDIRECTS = True

# Maximum redirects to follow
MAX_REDIRECTS = 5

# Save results to file
SAVE_RESULTS = False
RESULTS_OUTPUT_FILE = "profilescout_results.json"

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

# Enable file logging
ENABLE_FILE_LOGGING = False
LOG_FILE_PATH = "profilescout.log"

# Log level: DEBUG, INFO, WARNING, ERROR
LOG_LEVEL = "INFO"

# ============================================================================
# HTTP HEADERS CONFIGURATION
# ============================================================================

# Custom headers to send with requests
CUSTOM_HEADERS = {
    # Common headers that help avoid blocking
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
}

# ============================================================================
# EXPORT CONFIGURATION
# ============================================================================

# Export format: json, csv, txt
EXPORT_FORMAT = "json"

# Export file path
EXPORT_PATH = "profilescout_export"

# Include timestamps in export
INCLUDE_TIMESTAMPS = True

# Include HTTP status codes in export
INCLUDE_HTTP_CODES = True
