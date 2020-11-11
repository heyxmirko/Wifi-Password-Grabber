from flask import Flask, request
from zipfile import ZipFile
from os import remove

app = Flask(__name__)

def unzip_all_files():
    with ZipFile('data.zip', 'r') as zipObj:
        zipObj.extractall(path="passwords")
    remove("data.zip")


@app.route("/wpg/<file>", methods=["PUT"])
def data_handler(file):
    with open("data.zip", 'wb') as f:
        for chunk in iter(lambda: request.stream.read(16384), bytes()):
            f.write(chunk)
    unzip_all_files()
    return "done"


if __name__ == "__main__":
    app.run(port=80, host="0.0.0.0")