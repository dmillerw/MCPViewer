from app import app

import urllib2
import os
import zipfile
from StringIO import StringIO

_DOWNLOAD_PATH_ = "http://export.mcpbot.bspk.rs/{0}/{1}/{2}.zip"

@app.route('/mcp/snapshot/<mapping>/<type>')
def snapshot(mapping, type):
    return grab_mapping("mcp_snapshot", mapping, type)

@app.route('/mcp/stable/<mapping>/<type>')
def stable(mapping, type):
    return grab_mapping("mcp_stable", mapping, type)

def grab_mapping(type, version, file):
    url = _DOWNLOAD_PATH_.format(type, version, type + "-" + version)
    file_path = "cache/" + type + "-" + version + "/"
    dirname = os.path.dirname(file_path)

    if file != "fields" and file != "methods" and file != "params":
        return "{} is an invalid mapping type".format(file)

    # If it doesn't exist, download it
    if not os.path.exists(dirname):
        os.makedirs(dirname)

        try:
            req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
            data = urllib2.urlopen(req).read()
            zip = zipfile.ZipFile(StringIO(data))
            zip.extractall(file_path)
        except IOError, e:
            return "{} doesn't exist as a mapping".format(type + "-" + version)
    else:
        return open(file_path + file + ".csv", "r").read()

