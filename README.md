# harley-dealership-mining

Data mining US Harley Davidson dealership data

## Dependencies

- [Python 3.x](https://www.python.org/downloads/)
- [Firefox Geckodriver](https://github.com/mozilla/geckodriver/releases)
- See [config/requirements.txt](config/requirements.txt) for PIP dependencies

### Initial Setup

1. Download latest [Firefox Geckodriver](https://github.com/mozilla/geckodriver/releases).
2. Extract download.
3. Move `geckodriver` folder to `/usr/local/bin`, ex:

```sh
sudo mv geckodriver-vX.XX.X-linux64 /usr/local/bin/geckodriver-vX.XX.X-linux64
```

4. Install PIP dependencies:

```sh
pip install -r config/requirements.txt
```

## Zip Codes

ZIP Codes by Area and District codes downloaded 2022-11-01 made publicly available by USPS.[^1]

# Source

[^1]: https://postalpro.usps.com/ZIP_Locale_Detail
