def get_texts() -> str:
    with open(f'app/wording/commands.json', encoding='utf-8') as texts:
        return texts.read()

