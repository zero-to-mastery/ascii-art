import sys
from streamlit_app import main as streamlit_main
from cli import handle_image_conversion

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Command-line mode
        image_path = sys.argv[1]
        output_path = sys.argv[2] if len(sys.argv) > 2 else None
        handle_image_conversion(image_path, output_path)
    else:
        # Streamlit mode
        streamlit_main()