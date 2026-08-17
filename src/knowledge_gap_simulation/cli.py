import argparse
from pathlib import Path

from .config import SimulationConfig
from .pipeline import analyze_pipeline, generate_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(prog="knowledge-gap-sim"); commands = parser.add_subparsers(dest="command", required=True)
    generate = commands.add_parser("generate"); generate.add_argument("--data-dir", type=Path, default=Path("data")); generate.add_argument("--output-dir", type=Path, default=Path("outputs")); generate.add_argument("--model-name", default="gemini-2.5-flash"); generate.add_argument("--sample-size", type=int, default=30)
    analyze = commands.add_parser("analyze"); analyze.add_argument("--data-dir", type=Path, required=True); analyze.add_argument("--output-dir", type=Path, default=Path("outputs/analysis")); args = parser.parse_args()
    if args.command == "generate": generate_pipeline(SimulationConfig(args.data_dir, args.output_dir, args.model_name, args.sample_size))
    else: print(analyze_pipeline(args.data_dir, args.output_dir).to_string(index=False))


if __name__ == "__main__": main()
