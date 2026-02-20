#!/bin/bash

# The base URL of your website, taken from the CNAME file.
BASE_URL="https://www.local083.org"

# The output file for the sitemap.
OUTPUT_FILE="sitemap.xml"

# --- Script Start ---

# Start fresh by deleting the old sitemap.
rm -f $OUTPUT_FILE

# Print the XML header to the new sitemap file.
echo '<?xml version="1.0" encoding="UTF-8"?>' > $OUTPUT_FILE
echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' >> $OUTPUT_FILE

# Find all .html files, excluding template sources, test pages, and 404.
find . -name "*.html" \
  | grep -vE "^\\./templates/" \
  | grep -vE "^\\./test-pages/" \
  | grep -v "/404.html$" \
  | while read -r line; do
    # Remove the leading './' from the file path.
    url_path=$(echo "$line" | sed 's|^\./||')

    # Print the formatted URL entry to the sitemap.
    echo "  <url>" >> $OUTPUT_FILE
    echo "    <loc>${BASE_URL}/${url_path}</loc>" >> $OUTPUT_FILE
    echo "  </url>" >> $OUTPUT_FILE
done

# Print the XML footer to close the urlset tag.
echo '</urlset>' >> $OUTPUT_FILE

echo "Sitemap created at ${OUTPUT_FILE}"

# --- Optional: Add Sitemap to robots.txt ---
ROBOTS_FILE="robots.txt"
SITEMAP_ENTRY="Sitemap: ${BASE_URL}/${OUTPUT_FILE}"

# Check if the sitemap entry already exists in robots.txt
if ! grep -q "${SITEMAP_ENTRY}" "${ROBOTS_FILE}"; then
    echo "Adding sitemap to ${ROBOTS_FILE}..."
    echo "" >> $ROBOTS_FILE # Add a newline for spacing
    echo "${SITEMAP_ENTRY}" >> $ROBOTS_FILE
    echo "Done."
else
    echo "Sitemap entry already exists in ${ROBOTS_FILE}."
fi
