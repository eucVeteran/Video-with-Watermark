from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def _escape_drawtext(text: str) -> str:
    """Escape characters that are meaningful to FFmpeg's drawtext filter."""
    return text.replace("\\", r"\\\\").replace(":", r"\\:").replace("'", r"\\'")


def process_video(
    input_path: Path,
    output_path: Path,
    watermark_text: str,
    *,
    duration: int = 10,
    font_path: str | None = None,
) -> None:
    """Trim, watermark, and transcode a video using FFmpeg."""
    escaped_text = _escape_drawtext(watermark_text)

    # Опции drawtext без имени фильтра
    drawtext_options = [
        f"text='{escaped_text}'",
        "fontcolor=white",
        "fontsize=32",
        "box=1",
        "boxcolor=black@0.4",
        "boxborderw=10",
        "x=w-tw-20",
        "y=h-th-20",
    ]

    if font_path:
        # fontfile добавляем как обычную опцию
        drawtext_options.insert(0, f"fontfile={font_path}")

    # Важно: именно drawtext=, а не drawtext:
    filter_complex = "drawtext=" + ":".join(drawtext_options)

    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        "-t",
        str(duration),
        "-vf",
        filter_complex,
        str(output_path),
    ]

    try:
        subprocess.run(command, check=True)
    except FileNotFoundError as exc:  # pragma: no cover
        raise RuntimeError(
            "FFmpeg is required but was not found. Install FFmpeg and ensure it is available in PATH."
        ) from exc
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            "FFmpeg failed to process the video. Check the input file and parameters for validity."
        ) from exc


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Trim a video to 10 seconds, add a text watermark, and transcode it to a new file.",
    )
    parser.add_argument("input", type=Path, help="Path to the input video file")
    parser.add_argument("output", type=Path, help="Path for the processed video file (extension sets format)")
    parser.add_argument(
        "-t",
        "--text",
        dest="text",
        default="Sample Watermark",
        help="Text to use for the watermark (default: 'Sample Watermark')",
    )
    parser.add_argument(
        "-d",
        "--duration",
        dest="duration",
        type=int,
        default=10,
        help="Length of the output clip in seconds (default: 10)",
    )
    parser.add_argument(
        "--font",
        dest="font",
        default="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        help="Optional path to a TTF font file to render the watermark",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    process_video(
        input_path=args.input,
        output_path=args.output,
        watermark_text=args.text,
        duration=args.duration,
        font_path=args.font,
    )


if __name__ == "__main__":
    main()