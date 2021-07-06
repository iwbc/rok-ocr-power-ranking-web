## Requirements

- php 7.x
- python 3.9.x
  - pytesseract
  - numpy
  - opencv-python
  - Pillow
- tesseract 4.1.1

## php.ini example

```ini
max_execution_time = 180
max_input_time = -1
memory_limit = 1G
post_max_size = 1G
upload_max_filesize = 1G
max_file_uploads = 100
output_buffering = 4096
```

## change path

- `ocr/process.php` - $python_path
- `ocr/ocr.py` - pytesseract.pytesseract.tesseract_cmd
