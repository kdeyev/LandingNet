from flask import Flask, render_template, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from LandingNet import utils 
from LandingNet.HttpException import InvalidUsage
import subprocess

app = Flask(__name__)
app.config.from_object('LandingNet.config')
db = SQLAlchemy(app)

import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
logging.getLogger('werkzeug').setLevel(logging.DEBUG)

@app.route("/")
def index():
    from sqlalchemy import func
    from LandingNet.models import Crashs, MiniDump, Product
    #traces = MiniDump.query.join(Crashs,(Crashs.id == MiniDump.crash_id)).join(Product,(Product.id == MiniDump.product_id)).add_columns(Crashs.name.label("crash_name"), \
	#Crashs.id.label("crash_id"), Crashs.count.label("crash_count"), Product.name.label("product_name"), \
	#Crashs.updated.label("crash_updated"), MiniDump.build.label("build"), MiniDump.os.label("os")).distinct(Crashs.name)
    traces = Crashs.query.order_by(Crashs.updated.desc()).limit(100).all()
    return render_template("index.html", traces=traces)

@app.route("/crash/<int:cid>")
def crash(cid):
    from LandingNet.models import Crashs, MiniDump
    import json
    crash = Crashs.query.filter_by(id = cid).first_or_404()
    dumps = MiniDump.query.filter_by(crash_id = crash.id).order_by(MiniDump.timestamp.desc()).all()
    if len(dumps) == 0:
        raise InvalidUsage("No dumps for trace " + str(cid))

    crash.data = json.loads(dumps[0].data)

    return render_template("crash.html", crash=crash, dumps=dumps)
    
@app.route("/minidump/<int:did>")
def minidump(did):
    from LandingNet.models import MiniDump
    import json
    dump = MiniDump.query.filter_by(id = did).first_or_404()
    dump.data = json.loads(dump.data)
    return render_template("minidump.html", dump=dump)

@app.route("/upload_symbols", methods=["POST"])
def uploadSymbols():
    from flask import request
    from werkzeug import secure_filename
    import os

    if "symbols" not in request.files:
        raise InvalidUsage("Missing symbols file")

    file = request.files["symbols"]
    ext = file.filename.rsplit(".", 1)[1]

    symFile = None
    debugFile = None
    if ext == "zip":
        import zipfile
        import tempfile
        zfile = zipfile.ZipFile(file)
        zsymFile = None

        for name in zfile.namelist():
            (dirname, filename) = os.path.split(name)
            zext = filename.rsplit(".", 1)[1]
            if zext == "sym" and symFile is None:
                symFile = tempfile.TemporaryFile()
                symFile.write(zfile.read(name))
                symFile.seek(0)
            elif zext == "debug" and debugFile is None:
                debugFile = tempfile.TemporaryFile()
                debugFile.write(zfile.read(name))
                debugFile.seek(0)

        if symFile is None:
            raise InvalidUsage("No .sym file found in archive")
    elif ext == "sym":
        symFile = file
    else:
        raise InvalidUsage("Wrong symbols format, .sym or .zip extension expected")


    # Debug symbols need to be stored with a specific directory structure :
    # BREAKPAD_DEBUG_SYMBOLS_DIR/<exec name>/<hash>/<exec name>.sym

    # The first line of the sym file give the needed information
    # eg : MODULE Linux x86_64 6EDC6ACDB282125843FD59DA9C81BD830 test
    #                          |> Hash                           |> Exec name
    tmp = symFile.readline()
    tmp = tmp.split(" ")
    symFile.seek(0)
    execName = tmp[4].strip()

    path = os.path.join(app.config["BREAKPAD_DEBUG_SYMBOLS_DIR"], execName, tmp[3].strip())
    utils.mkdirs(path)

    with open(os.path.join(path, tmp[4].strip() + ".sym"), "w") as handle:
        handle.write(symFile.read())

    symFile.close()

    if debugFile is not None:
        fields = ["build", "arch", "system"]
        for field in fields:
            if field not in request.form:
                raise InvalidUsage("Missing field " + field)

        name = "%s_%s_%s_%s.debug" % (execName, request.form["system"], request.form["arch"], request.form["build"])
        with open(os.path.join(app.config["DEBUG_SYMBOLS_DIR"], name), "w") as handle:
            handle.write(debugFile.read())

        debugFile.close()
            
    return render_template("upload_success.html")

@app.route("/submit", methods=["POST"])
def submit():
    from flask import request
    from LandingNet import models
    from werkzeug import secure_filename
    import os
    import uuid

    minidumpArg = ""
    if "minidump" in request.files:
        minidumpArg = "minidump"
    elif "upload_file_minidump" in request.files: # Special case for OSX breakpad crash reporter
        minidumpArg = "upload_file_minidump"
    else:
        raise InvalidUsage("No minidump specified")

    file = request.files[minidumpArg]

    if file is None or file.filename.rsplit(".", 1)[1] != "dmp":
        raise InvalidUsage("Wrong dump format")

    if "build" not in request.form:
        raise InvalidUsage("Build is not specified")

    if "product" not in request.form:
        raise InvalidUsage("Product is not specified")

    if "version" not in request.form:
        raise InvalidUsage("Version is not specified")

    product = models.Product.query.filter_by(version=request.form["version"], name=request.form["product"]).first()
    if product is None:
        product = models.Product()
        product.name = request.form["product"]
        product.version = request.form["version"]
        db.session.add(product);
        db.session.commit()

    filename = str(uuid.uuid4()) + ".dmp"
    file.save(os.path.join(app.config["MINIDUMP_UPDLOAD_DIR"], filename))

    ret = utils.processMinidump(filename)

    crash = models.Crashs.query.filter_by(signature = ret["signature"]).first()
    if crash is None:
        crash = models.Crashs()
        crash.count = 0
        crash.name = ret["name"]
        crash.signature = ret["signature"]
        db.session.add(crash)
        db.session.commit()
        project = "PREV"
        component = "CoreEngine"            
        if (app.config["PRODUCTS_MAP"].has_key(product.name)):
            project = app.config["PRODUCTS_MAP"][product.name][0]
            component = app.config["PRODUCTS_MAP"][product.name][1]
        crash_url = request.host_url.rstrip('/') + url_for('crash', cid=crash.id)
        description = "Product {} is crashed. Please check URL {} for further details". format(product.name, crash_url)
        issue = app.config["JIRA_CLIENT"].create_issue(project=project, summary=ret["name"],
            description=description, issuetype={'name': 'Bug'},customfield_10121={'value': '2-Medium'},versions=[{'name': 'Paradigm 18'}],components=[{'name': component}])
        crash.jira_url = issue.permalink()
        
    md = models.MiniDump()
    md.crash_id = crash.id
    md.product_id = product.id
    md.signature = ret["signature"]
    md.minidump = filename
    md.build = request.form["build"]
    md.data = ret["data"]
    md.system_info = ret["systemInfo"]
    md.name = ret["name"]
    md.user = request.form["user"]

    crash.count = crash.count + 1

    db.session.add(md)
    db.session.commit()
    
    if 'ELK' in app.config and app.config['ELK'] != None:
        elk = ret
        elk["product_name"] = product.name
        elk["product_version"] = product.version
        elk["build"] = request.form["build"]
        elk["user"] = request.form["user"]
        elk["filename"] = filename      
        ELK = app.config['ELK'] 
        index = app.config['ELK_INDEX']
        docType = app.config['ELK_DOCTYPE']
        result = ELK.index(index, docType, id=md.id, body=elk)
    return render_template("upload_success.html")

@app.errorhandler(InvalidUsage)
def handleInvalidUsage(error):
    from flask import jsonify
    return "ERROR : " + error.message + "\r\n", 422

@app.template_filter("datetime")
def format_datetime(value):
	return str (value)
    #from babel.dates import format_datetime
    #return format_datetime(value, "YYYY-MM-dd 'at' HH:mm:ss")

@app.template_filter("normalizeFilename")
def normalizeFilename(value):
    filename = "N/A"

    if isinstance(value, basestring) :
        filename = value.rsplit("/", 1)[1]

    return filename

@app.template_filter("normalizeLine")
def normalizeLine(frame):
    result = ""
    if frame.get("line"):
        result += ":" + str(frame["line"])

    return result

@app.template_filter("normalizeIssue")
def normalizeIssue(issueUrl):
    if issueUrl is None:
        return ""
    splitted = issueUrl.split("/")
    return splitted[len(splitted) - 1]
       
@app.template_filter("normalizeFrame")
def normalizeFrame(frame):
    ret = ""

    if frame.get("function"):
        ret = frame["function"]
    else:
        ret = "N/A"

    return ret
