# Video with Watermark

A small Python script that takes an input video, trims it to 10 seconds, applies a text watermark, and saves the file in any container format supported by FFmpeg (e.g., `.mkv`, `.mp4`, `.mov`).

## Under the Hood

- Minimal dependency: requires [FFmpeg](https://ffmpeg.org) installed and available in `PATH`.
- Uses standard `subprocess` calls without additional libraries.
- The watermark is rendered using the `drawtext` filter in the bottom-right corner with a semi-transparent background for readability.

## Installation

1) Make sure FFmpeg is installed and accessible from the command line.  
2) Clone the repository and navigate to the project folder:

```bash
git clone <repo-url>
cd Video-with-Watermark
```

## Usage

Basic example: trim a video to 10 seconds, add a watermark, and save it in another format.

`python3 video_processor.py input.mp4 output.mkv --text "Watermark"`

Additional parameters:

`-d/--duration — duration of the output clip in seconds (default: 10).`
`--font — path to a TTF font used for text rendering (default: DejaVu Sans from system fonts).`

Example with custom duration and font:

`python3 video_processor.py input.mov clipped.mp4 --text "Demo" --duration 8 --font /path/to/font.ttf`