import pathlib


def create_save_directory(save_path: str = '~/docs2txt/') -> pathlib.Path:
    """Create the save directory if it does not exist."""
    if save_path.startswith('~/'):
        save_path = pathlib.Path(save_path).expanduser()
    else:
        save_path = pathlib.Path(save_path)

    if not save_path.exists():
        save_path.mkdir(parents=True)
    return save_path
