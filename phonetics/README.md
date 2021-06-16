Phonetics explorations with the [Phoible](https://phoible.github.io/) dataset.

### Dependencies
- `python3` (I recommend getting it via `pyenv`)

### Install
Create virtualenv and install packages (or use your method of choice).
```
pip3 -m virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

### Development server
(`source venv/bin/activate` if you didn't already.)
```
make serve
```

### Render report (non-interactive results) to HTML
(`source venv/bin/activate` if you didn't already.)
Build notebook (including cell contents) as HTML.
```
make build
```
