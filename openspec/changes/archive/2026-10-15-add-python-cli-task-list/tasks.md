# Tasks

## 1. JSON persistence

- [x] 1.1 Implement local JSON task storage with UUID identifiers, incomplete status, missing-file handling, and atomic writes; verify tests cover creating, reloading, and completing saved task records.
- [x] 1.2 Handle unreadable or invalid JSON without replacing the stored data; verify tests assert a clear error and that the original file remains unchanged.

## 2. Command-line interface

- [x] 2.1 Implement `todo.py` with `add`, `list`, and `complete` subcommands, including empty descriptions and unknown identifiers; verify CLI tests cover success, error messages, and persisted status.
- [x] 2.2 Document setup-free invocation, command syntax, and the JSON storage location in `README.md`; verify the documented examples run successfully with an isolated home directory.
