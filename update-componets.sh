#!/bin/bash
# update-components.sh
# A script to find all .html files recursively and replace their <header> and <footer>
# tags with the content from the snippet files in the _includes/ directory.
#
# Usage:
#   ./update-components.sh       # Updates both header and footer
#   ./update-components.sh -h    # Updates only the header
#   ./update-components.sh -f    # Updates only the footer
#   ./update-components.sh -h -f # Updates both header and footer

# --- Configuration ---
HEADER_FILE="_includes/header.snip"
FOOTER_FILE="_includes/footer.snip"

# --- Argument Parsing ---
UPDATE_HEADER=false
UPDATE_FOOTER=false

# If no arguments are provided, update both.
if [ $# -eq 0 ]; then
    UPDATE_HEADER=true
    UPDATE_FOOTER=true
else
    while getopts ":hf" opt; do
        case ${opt} in
            h ) UPDATE_HEADER=true ;;
            f ) UPDATE_FOOTER=true ;;
            \? ) echo "Invalid option: -$OPTARG" >&2; exit 1 ;;
        esac
    done
fi

# --- Safety Checks ---
if [ "$UPDATE_HEADER" = true ] && [ ! -f "$HEADER_FILE" ]; then
    echo "Error: Header snippet not found at '$HEADER_FILE'"
    exit 1
fi

if [ "$UPDATE_FOOTER" = true ] && [ ! -f "$FOOTER_FILE" ]; then
    echo "Error: Footer snippet not found at '$FOOTER_FILE'"
    exit 1
fi

if ! command -v perl &> /dev/null; then
    echo "Error: Perl is not installed. This script requires Perl to run."
    exit 1
fi

# --- Main Logic ---
# Load content only if needed.
if [ "$UPDATE_HEADER" = true ]; then
    HEADER_CONTENT=$(cat "$HEADER_FILE")
    export HEADER_CONTENT
fi

if [ "$UPDATE_FOOTER" = true ]; then
    FOOTER_CONTENT=$(cat "$FOOTER_FILE")
    export FOOTER_CONTENT
fi

# Find all .html files, excluding templates and files within the _includes directory itself.
find . -name "*.html" -not -path "./_includes/*" -not -path "*template.html" -print0 | while IFS= read -r -d '' file; do
    echo "Processing: $file"

    # Ensure analytics.js is loaded just before closing head (idempotent)
    if ! grep -q "js/analytics.js" "$file"; then
        perl -i -p0e 's|</head>|    <script src="/js/analytics.js" defer></script>\n</head>|' "$file"
    fi

    if [ "$UPDATE_HEADER" = true ]; then
        echo "  -> Updating header..."
        perl -i -p0e 'BEGIN { $content = $ENV{"HEADER_CONTENT"}; } s|<header.*?</header>|$content|s' "$file"
        # Cleanup old mobile menu script only when updating the header
        perl -i -p0e 's|<script>\s*// --- Mobile Menu Toggle ---.*?</script>||s' "$file"
    fi

    if [ "$UPDATE_FOOTER" = true ]; then
        echo "  -> Updating footer..."
        perl -i -p0e 'BEGIN { $content = $ENV{"FOOTER_CONTENT"}; } s|<footer.*?</footer>|$content|s' "$file"
    fi
done

echo "✅ Update complete!"
