# AspIde

AspIde is a project developed in 2021 for my bachelor's thesis. It is not perfect and was created for educational and experimental purposes, so some parts may be incomplete. The platform allows syntactic analysis and management of ASP programs, with a Python backend and React/Ionic frontend. The project is designed to facilitate writing, execution, and analysis of logic programs, with regression, timing, and file management features.

## Project Structure

- **backend/**: Python backend for APIs, analysis, regression, timing, and ASP parsing.
	- `app.py`: Backend entry point.
	- `panalysis/`: Modules for regression and CSV writing.
	- `server/`: API server and routes.
	- `syntAnalysis/`: ASP parser.
	- `timing/`: Timing; the DLV2 binary file is not included in the repository, but is expected to be manually placed in this folder.
- **webasp/**: React/Ionic frontend and Android/Capacitor configuration.
	- `src/`: React components, pages, actions, reducer, theme.
	- `public/`: Static files and assets.
	- `android/`: Android build configuration; generated build files (such as APK and temporary builds) are not included in the repository, only the necessary files for compilation.

## Quick Start

### Backend
1. Install Python dependencies:
	```bash
	pip install -r requirements.txt
	```
2. Start the backend:
	```bash
	python backend/app.py
	```

### Frontend
1. Install Node dependencies:
	```bash
	cd webasp
	npm install
	```
2. Start the frontend:
	```bash
	npm start
	```

## Security and Repository Notes

- The `.gitignore` file excludes cache, build, dependencies, temporary files, and the DLV2 binary (`dlv2.win.x64_5`).

## Main Dependencies

- **Backend**: Python 3.x, Flask, pandas, numpy, etc.
- **Frontend**: React (17.0.1), Ionic, Capacitor, Node.js (recommended >=12.x).