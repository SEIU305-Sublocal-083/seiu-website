#!/bin/bash

# A script to auto-generate Open Graph images and inject meta tags into HTML files.

# --- CONFIGURATION ---
# Set your website's full base URL (no trailing slash)
BASE_URL="https://yourwebsite.com"

# Set the directory where your HTML files are located
HTML_DIR="."

# Set the name of the folder where images will be saved
IMAGE_DIR="og-images"
# --- END CONFIGURATION ---


# Create the image directory if it doesn't exist
mkdir -p "$IMAGE_DIR"

# Find all HTML files in the specified directory
find "$HTML_DIR" -name "*.html" | while read -r html_file; do
    echo "Processing: $html_file"

    # 1. Extract the page title from the HTML file
    # Uses grep to find the title tag and sed to remove the tags themselves
    TITLE=$(grep -o '<title>.*</title>' "$html_file" | sed -e 's/<title>//' -e 's/<\/title>//')

    # If no title is found, use a default
    if [ -z "$TITLE" ]; then
        TITLE="An Interesting Page"
    fi

    # 2. Generate a unique filename
    UUID_NAME=$(uuidgen)
    WEBP_PATH="$IMAGE_DIR/$UUID_NAME.webp"

    # 3. Generate and convert the image using ImageMagick
    # This creates a 1200x630 image with a blue background and centered white text.
    # You can customize colors, fonts, and text position here!
    convert \
        -size 1200x630 \
        xc:"#3b82f6" \
        -font "Arial" \
        -pointsize 70 \
        -fill white \
        -gravity center \
        -annotate +0+0 "$TITLE" \
        -quality 80 \
        "$WEBP_PATH"

    if [ $? -eq 0 ]; then
        echo "  ✅ Generated image: $WEBP_PATH"
    else
        echo "  ❌ Failed to generate image for $html_file"
        continue # Skip to the next file
    fi

    # 4. Construct the full image URL and the meta tags block
    FULL_IMAGE_URL="$BASE_URL/$WEBP_PATH"

    # Using a heredoc for the meta tags makes it clean and readable
    META_TAGS=$(cat <<EOF

<meta property="og:type" content="website">
<meta property="og:url" content="$BASE_URL/$(basename "$html_file")">
<meta property="og:title" content="$TITLE">
<meta property="og:image" content="$FULL_IMAGE_URL">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:url" content="$BASE_URL/$(basename "$html_file")">
<meta name="twitter:title" content="$TITLE">
<meta name="twitter:image" content="$FULL_IMAGE_URL">

EOF
)

    # 5. Inject the meta tags block right before the </head> tag
    # The -i '' flag is the macOS-specific way to edit a file in-place
    sed -i '' "s|</head>|${META_TAGS}</head>|" "$html_file"

    echo "  ✅ Injected meta tags into $html_file"
    echo "---"
done

echo "🎉 All done!"