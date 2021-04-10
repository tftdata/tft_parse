from pprint import pprint
from pathlib import Path
import json
import tft_parse

file_path = Path(__file__).parents[0].resolve()
with open(file_path.joinpath('match.json'), 'r') as f:
    data = json.loads(f.read())


match = tft_parse.MatchDto(data)
pprint(match.metadata.region)