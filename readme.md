Setup

```
pip3 install -r requirement.txt
hypercorn --reload index:app
```

Demo

```
http://localhost:8000/demo
```

Docs

```
http://localhost:8000/docs
```

Utils

```
Dowloader script
OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES python3 downloader.py

Conversion script
python3 image_conversion.py
```