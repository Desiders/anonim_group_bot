from typing import Text


def get_texts() -> Text:
    with open(f'app/wording/commands.json', encoding='utf-8') as texts:
        return texts.read()

