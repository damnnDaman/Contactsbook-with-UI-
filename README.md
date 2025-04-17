<!--
 Copyright 2025 daman

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     https://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
-->


# vCard Management Application

This project is a vCard management tool that parses and manages vCard files (`.vcf`). It includes a C library for vCard parsing and validation, and a text-based Python user interface. The Python UI (built with Asciimatics) uses the C library via `ctypes` to handle vCard data. Optionally, the application can integrate with a MySQL database to store and query contact metadata.

## Features
- Parse and validate vCard (`.vcf`) files using a custom C library (`libvcparser`).
- Text-based UI built with Asciimatics for interactive viewing and management of contacts.
- C/Python integration via `ctypes` to leverage the C parser library from Python.
- Optional MySQL database support for storing and querying vCard metadata.

## Usage
1. **Build the C library:** Run `make` inside the `assign1/` directory to compile the parser (produces `libvcparser.so`).
2. **Prepare vCard files:** Place your contact `.vcf` files in the `bin/cards/` folder (or use the sample files provided).
3. **Run the UI:** From the project root, execute the Python interface: `python3 bin/A3main.py`.
    - Use the text menu to load vCards, view contact details, and perform available operations.
    - *(Optional)* If using the database features, ensure a MySQL server is running and configured for the application.

## Dependencies
- **C compiler** (e.g., GCC) – to build the C library.
- **Python 3.x** – to run the application.
- **Asciimatics** – Python library for the text UI (install via pip).
- *(Optional)* **MySQL** – MySQL server and Python connector for database features.