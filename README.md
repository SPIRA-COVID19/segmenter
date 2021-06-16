# segmenter
A segmenter of speech audios. In comes a raw audio, out comes boundaries between speech and silence.

### Usage

#### Via docker

```bash
docker build . -t segmenter
docker run -it --rm -v <INPUT_DATA>:/data:ro -v <OUTPUT_DATA>:/out segmenter /out /data
```

#### (recommended) Via python's virtual environment

1. Make sure pipenv is installed.
```bash
pip install pipenv
```

2. Clone this repository.
```bash
git clone https://github.com/SPIRA-COVID19/segmenter.git
cd segmenter/
pipenv sync
```

3. Run main.
```bash
pipenv run python main.py --help
```
