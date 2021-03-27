# aInstagenic

On Instagram, there’s no room for “good enough” shots. Time to level up using AI.

## Setup and Installation

Put the correct credentials in [config.json](config.json.template).
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install packages.

```bash
pip install requirements.txt
```

### Data Curation

```bash
cd data_curation
sh download.sh
python preProcessImages.py
```
Upload the curated dataset on the [Custom Vision Portal](https://www.customvision.ai/projects).

### Run the App using Docker

```bash
sh deploy.sh
```

## License
[MIT](https://choosealicense.com/licenses/mit/)