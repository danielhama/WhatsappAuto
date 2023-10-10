import io
import os
import re

path = os.path.abspath(r"C:\Users\c084029\Downloads\chromedriver_win32\chromedriver.exe")
replacement = "dan_dsjlfiflkdjfuejlpduejf".encode()
with io.open(path, "r+b") as f:
    for line in iter(lambda: f.readline(), b""):
        if b"cdc_" in line:
            f.seek(-len(line), 1)
            newline = re.sub(b"cdc_.{22}", replacement, line)
            f.write(newline)
            print("Alterado")