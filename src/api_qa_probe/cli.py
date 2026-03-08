import argparse
from pathlib import Path

from .runner import run_cases, to_json_report, to_markdown_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="API QA Probe CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    run_parser = sub.add_parser("run", help="Run API QA cases")
    run_parser.add_argument("input_path")
    run_parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    run_parser.add_argument("--output", default="")
    return parser


def execute(input_path: str, output_format: str, output_path: str) -> str:
    report = run_cases(input_path)
    rendered = to_markdown_report(report) if output_format == "markdown" else to_json_report(report)
    if output_path:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered, encoding="utf-8")
    return rendered


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "run":
        rendered = execute(args.input_path, args.format, args.output)
        print(rendered)


if __name__ == "__main__":
    main()
