# harley-dealership-mining

Data mining US [Harley Davidson dealership](https://www.harley-davidson.com/us/en/tools/find-a-dealer.html) information

## Dependencies

- [Python 3.x](https://www.python.org/downloads/)
- [Firefox Geckodriver](https://github.com/mozilla/geckodriver/releases)
- See [config/requirements.txt](config/requirements.txt) for PIP dependencies
- [libpostal](https://github.com/openvenues/libpostal#installation-maclinux)

### Initial Setup

1. Download latest [Firefox Geckodriver](https://github.com/mozilla/geckodriver/releases).
2. Extract download.
3. Move `geckodriver` folder to `/usr/local/bin`, ex:

```sh
sudo mv geckodriver-vX.XX.X-linux64 /usr/local/bin/geckodriver-vX.XX.X-linux64
```

4. Install `pip` dependencies:

```sh
pip install -r config/requirements.txt
```

5. Create `sqlite3` backend:

```sh
cd sql && ./create_zip_codes.py && ./create_dealers.py
```

## Zip Codes

ZIP Codes by Area and District codes downloaded 2022-11-01 made publicly available by USPS.[^1]

# Source

[^1]: https://postalpro.usps.com/ZIP_Locale_Detail
