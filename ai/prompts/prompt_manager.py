from pathlib import Path

PROMPT_ROOT = Path(__file__).parent


def load_prompt(relative_path: str) -> str:
    prompt_path = (PROMPT_ROOT / relative_path).resolve()
    if not prompt_path.is_relative_to(PROMPT_ROOT.resolve()) or not prompt_path.is_file():
        raise ValueError("Unknown prompt")
    return prompt_path.read_text(encoding="utf-8")