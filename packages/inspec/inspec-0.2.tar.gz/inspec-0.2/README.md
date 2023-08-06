# inspec
View spectrograms of audio data files in the terminal as ascii characters. Provides printing to stdout, a terminal gui built on curses, and importable functions.

## install

```
pip install inspec
```

## cli

Invocation of **inspec** uses the entrypoint **python -m inspec.cli**.

#### inspec open
```
Usage: inspec open [OPTIONS] [FILENAMES]...

  Open interactive gui for viewing audio files in command line

Options:
  -r, --rows INTEGER  Number of rows in layout
  -c, --cols INTEGER  Number of columns in layout
  -t, --time FLOAT    Jump to time in file
  --cmap TEXT         Choose colormap (see list-cmaps for options)
  --help              Show this message and exit.
```

![inspec open demo](demo/inspec_open_demo.gif)

#### inspec show
```
Usage: inspec show [OPTIONS] FILENAME

  Print visual representation of audio file in command line

Options:
  --cmap TEXT           Choose colormap (see list-cmaps for options)
  -d, --duration FLOAT
  -t, --time FLOAT
  --amp                 Show amplitude of signal instead of spectrogram
  --help                Show this message and exit.
```

![inspec show demo](demo/inspec_show_demo.gif)

#### importing in python

The code can be imported so renders can be done dynamically in other programs. This is the current gist but would be nice to make a simpler way to do this.

```python
from inspec.plugins.audio.spectrogram_view import BaseAsciiSpectrogramPlugin

# Printing to stdout
plugin = BaseAsciiSpectrogramPlugin()
plugin.set_cmap("plasma")
plugin.read_file(FILENAME)
plugin.render()
```
