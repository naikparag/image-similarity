Setup

```
pip3 install -r requirement.txt
hypercorn --reload index:app
OR
hypercorn --reload  index:app -b 127.0.0.1:8100
OR
hypercorn --workers 4 index:app -b 127.0.0.1:8100
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
