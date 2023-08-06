# MX-Notes

## Installation

### pip

```shell
    shell> pip install mx-notes
```

### From source

```shell
    shell> git clone https://github.com/amunger3/mx-notes.git
    shell> cd mx-notes
    shell> python setup.py install
```

## Usage

### CLI

MX-Notes can be ran from the command line with the command `mx`:

```shell
    shell> mx <notes-dir> --host <host> --port <port>
```

where `notes-dir` represents the path to your desired MX-Notes directory.

#### Defaults

- `notes-dir`: `~/MX-Notes` (will create directory if it doesn't exist)
- `host`: `127.0.0.1` (localhost)
- `port`: `5000`

## Features

### Creating Notes

Notes are created by selecting the 'New' button. Setting the title is optional.
Notes are saved automatically as they are edited.

### Editing Notes

The note editing screen allows the user to edit the note title and content. Math
symbols and their keybindings are shown on the left panel for quick access.

### Listing Notes

When the app is started, the main screen is a list of notes in the specified directory.
These notes are ordered by modification time. Clicking on a note's title will bring up its edit screen.

### Notes Format

Notes are saved as <note-title>.txt with a Markdown-style title followed by the note's content.
