from flask import current_app
from werkzeug.security import safe_join

from datetime import datetime
from pathlib import Path


class Note(object):

    def __init__(self, filename, title, text=None, mtime=None):
        self.filename = filename
        self.title = title
        self.text = text
        self.mtime = mtime


def _path_for(fname):
    path = safe_join(current_app.config['NOTES_DIR'], fname)
    return path


def note_exists(fname):
    path = Path(_path_for(fname))
    return (not fname.startswith('.') and path.exists() and path.is_file())


def _read_title(f):
    line = f.readline()
    if line.startswith(b'# ') and f.readline() == b'\n':
        return line[2:-1].decode('utf-8')
    return None


def read_note(fname):
    with open(_path_for(fname), 'rb') as f:
        return Note(fname, _read_title(f), f.read().decode('utf-8'))


def write_note(note):
    with open(_path_for(note.filename), 'wb') as f:
        if note.title:
            f.write(b'# ')
            f.write(note.title.encode('utf-8'))
            f.write(b'\n\n')
        if note.text:
            f.write(note.text.encode('utf-8'))


def list_notes():
    notes = []
    notes_root = Path(current_app.config['NOTES_DIR'])
    for npath in notes_root.iterdir():
        if note_exists(npath.name):
            path = Path(_path_for(npath.name))
            ts = path.stat().st_mtime
            with open(path, 'rb') as f:
                title = _read_title(f)
                note = Note(npath.name, title, None, datetime.fromtimestamp(ts))
                notes.append(note)
    notes.sort(key=lambda x: x.mtime, reverse=True)
    return notes
