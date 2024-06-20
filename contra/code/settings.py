from pathlib import Path

W_RESO,H_RESO = 1280,720

CODE_DIR = Path(__file__).parent
ROOT_DIR = CODE_DIR.parent
GRAPHICS_DIR = ROOT_DIR / 'graphics'
AUDIO_DIR = ROOT_DIR / 'audio'
DATA_DIR = ROOT_DIR / 'data'

LAYERS = {
    'BG': 0,
    'BG Detail': 1,
    'Level': 2,
    'FG Detail Bottom': 3,
    'FG Detail Top': 4,
}
