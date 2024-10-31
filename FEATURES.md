# ASCII Art Generator 

### Overview
This ASCII Art Generator uses customizable patterns and filters to convert images into ASCII art. The script supports options for resizing, brightness/contrast adjustments, and even color themes to enhance your ASCII art.

---

### Installation Requirements

#### Prerequisites
- Python 3.x installed on your system
- Install necessary packages using the following command:
  ```bash
  pip install typer pillow numpy rich
  ```

---

### Command Line Options

| Option           | Description                                                    | Example                                                                                   |
|------------------|----------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| `--width`        | Sets the width of the ASCII art. Default is 100.               | `--width 150`                                                                             |
| `--pattern`      | Selects ASCII pattern type. Options: `basic`, `complex`, `emoji`, `numeric` | `--pattern emoji`                                                                         |
| `--theme`        | Color theme for colorized ASCII. Options: `neon`, `pastel`, `grayscale` | `--theme neon`                                                                            |
| `--brightness`   | Adjusts image brightness. Default is 1.0 (no change).          | `--brightness 1.2`                                                                        |
| `--contrast`     | Adjusts image contrast. Default is 1.0 (no change).            | `--contrast 1.3`                                                                          |
| `--blur`         | Applies blur effect to the image before ASCII conversion.      | `--blur`                                                                                  |
| `--sharpen`      | Sharpens the image before ASCII conversion.                    | `--sharpen`                                                                               |
| `--contours`     | Adds contour effect to enhance edges in ASCII output.          | `--contours`                                                                              |
| `--invert`       | Inverts image colors before conversion.                        | `--invert`                                                                                |
| `--output`       | Saves ASCII art to specified file.                             | `--output output.txt`                                                                     |

1. Basic Usage:

```plaintext
python community-version.py <input_image>
```

Example: `python community-version.py example/ztm-logo.png`


2. Width Option:

```plaintext
python community-version.py <input_image> --width <value> or -w <value>
```

Example: `python community-version.py example/ztm-logo.png --width 150`


3. Output File Option:

```plaintext
python community-version.py <input_image> --output <filename> or -o <filename>
```

Example: `python community-version.py example/ztm-logo.png --output ztm_ascii.txt`


4. ASCII Pattern Option:

```plaintext
python community-version.py <input_image> --pattern <pattern_type> or -p <pattern_type>
```

Available patterns: 'basic', 'complex', 'emoji', 'numeric'
Example: `python community-version.py example/ztm-logo.png --pattern complex`


5. Brightness Adjustment:

```plaintext
python community-version.py <input_image> --brightness <value> or -b <value>
```

Example: `python community-version.py example/ztm-logo.png --brightness 1.2`


6. Contrast Adjustment:

```plaintext
python community-version.py <input_image> --contrast <value> or -c <value>
```

Example: `python community-version.py example/ztm-logo.png --contrast 1.1`


7. Blur Effect:

```plaintext
python community-version.py <input_image> --blur
```

Example: `python community-version.py example/ztm-logo.png --blur`


8. Sharpen Effect:

```plaintext
python community-version.py <input_image> --sharpen
```

Example: `python community-version.py example/ztm-logo.png --sharpen`


9. Contour Effect:

```plaintext
python community-version.py <input_image> --contours
```

Example: `python community-version.py example/ztm-logo.png --contours`


10. Help Command:

```plaintext
python community-version.py --help
```

This displays all available options with their descriptions.




You can combine multiple options in a single command. For example:

```plaintext
python community-version.py example/ztm-logo.png --width 120 --pattern complex --brightness 1.1 --contrast 1.2 --colorize --theme pastel --output ztm_ascii_colored.txt
```

This command will generate a colorized ASCII art of the ZTM logo with a width of 120 characters, using the complex pattern, adjusted brightness and contrast, and the pastel color theme, saving the output to a file named 'ztm_ascii_colored.txt'.

Remember to replace `example/ztm-logo.png` with the path to the image you want to convert to ASCII art.
