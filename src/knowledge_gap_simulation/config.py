from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SimulationConfig:
    data_dir: Path
    output_dir: Path = Path("outputs")
    model_name: str = "gemini-2.5-flash"
    sample_size: int = 30
    pilot_per_subject: int = 2
    knowledge_levels: tuple[int, ...] = (1, 2, 3)
    strategies: tuple[str, ...] = ("A", "B")
    seed: int = 42
