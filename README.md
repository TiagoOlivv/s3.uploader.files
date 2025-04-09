# s3.uploader.file.app

**A modern desktop app to upload files in parallel to Amazon S3**, built with Python and PyQt6. Simple, elegant, and optimized for performance.

---

## Features

- Upload files in batch to Amazon S3
- Parallel upload for faster performance
- Modern dark UI using PyQt6
- Folder selection via file dialog
- Accurate and responsive progress bar
- Auto-creates S3 bucket if it doesn’t exist
- Option to remember AWS credentials locally
- Field validation and error handling
- Cross-platform build support (PyInstaller)

---

## Project Structure

```
s3.uploader.file.app/
│
├── app/
│   ├── __main__.py              # App entry point
│   ├── gui/
│   │   ├── window.py            # Launches the QApplication
│   │   ├── main_window.py       # Main window logic
│   │   ├── layout.py            # UI layout setup
│   │   ├── styles.py            # UI styles
│   │   ├── utils.py             # GUI utility functions
│   ├── services/
│   │   └── uploader.py          # Parallel upload logic
│   ├── utils/
│   │   ├── s3.py                # AWS S3 helpers
│   │   └── settings.py          # Save/load local config
│
├── requirements.txt
├── Makefile
└── README.md
```

---

## ⚙️ Requirements

- Python 3.10+
- Valid AWS credentials (with S3 access)
- Linux/macOS (Windows support possible with adjustments)

---

## 🧰 Installation & Usage

```bash
git clone https://github.com/tiagoolivv/s3.uploader.file.app.git
cd s3.uploader.file.app
make setup
make run
```

---

## 🛠️ Makefile Commands

| Command           | Description                                     |
|------------------|-------------------------------------------------|
| `make setup`      | Creates virtual environment and installs deps   |
| `make run`        | Launches the application                        |
| `make clean`      | Removes virtual environment and build files     |
| `make freeze`     | Freezes current dependencies to `requirements.txt` |
| `make build-linux`| Builds standalone Linux executable using PyInstaller |

---

## 🧪 How to Use

1. Fill in all AWS credentials:
   - AWS Region
   - Access Key ID
   - Secret Access Key
   - Bucket Name
2. Select the folder containing the files.
3. Optionally check **Save credentials** to reuse them next time.
4. Click **Start Upload**.
5. Monitor the progress bar until upload completes.

---

## 🧵 Behind the Scenes

- Uploads are done using `ThreadPoolExecutor` for parallelism.
- Only file files are uploaded.
- S3 bucket is auto-created if it doesn’t already exist.

---

## 💾 Local Config (Optional)

If the **Save credentials** checkbox is enabled, the app stores your AWS details and bucket name in a local file (`config.json`). These values will be automatically restored on the next launch.

---

## ❌ Not Implemented

- Time remaining estimation (removed due to inaccuracy)
- Drag-and-drop support
- ...

---

## 📄 License

This project is open for free use and modification. Contributions via pull requests are welcome!

---