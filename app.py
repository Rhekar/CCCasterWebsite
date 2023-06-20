import os
from flask import Flask, send_file,send_from_directory, render_template, request
from comboparser import *
from lark import UnexpectedCharacters
app = Flask(__name__, static_folder='static')


b = "66b61ef"
c = "Tue, Oct 05, 2021  6:42:41 PM"

b2 = "a1d0721"
c2 = "Thu, Sep 23, 2021 10:36:00 PM"
@app.route("/LatestVersion")
def latest():
    return "3.1.004"
@app.route("/LatestVersionDev")
def latestdev():
    return f"3.1.002\n{b}\n{c}"
@app.route("/PreviousVersion")
def prev():
    return "3.1.003"
@app.route("/PreviousVersionDev")
def prevdev():
    return f"3.1.001\n{b2}\n{c2}"

DOWNLOAD_DIRECTORY = "caster/"
@app.route('/cccaster<string:path>',methods = ['GET','POST'])
def get_files(path):
    """Download a file."""
    try:
        return send_from_directory(DOWNLOAD_DIRECTORY, f"cccaster{path}", as_attachment=True)
    except FileNotFoundError:
        abort(404)

charaNames.sort()
@app.route("/trialmaker")
def trialmaker():
    return render_template('trialpage.html', charas=sorted(charaNames))

@app.route("/trialmaker", methods=['POST'])
def make_trial_post():
  try:
    charaname = f"seqlists/{request.form['moon']}-{request.form['chara']}.csv"
    if not os.path.isfile( charaname ):
        return "Character currently not supported"
    seqList = charaname
    a = ComboTransformer(  seqList )
    comboName = request.form['fname']
    comboText = request.form['text']
    t = comboparser.parse(comboText)
    processed_text = a.transform( t )
    exportCombo( [comboName, processed_text] )
    return send_from_directory("trials/", f"{comboName}.txt", as_attachment=True)
    #os.unlink( f"trials/{comboName}.txt" )
    #return "A"
  except UnexpectedCharacters as e:
      return f"Error encountered, please send input for debugging: <br/> {e._context} <br/> {e.considered_rules} <br/> {e.state}"
  except Exception as e:
      return f"Error encountered, please send input for debugging: \n {e!r}"

@app.route("/")
def main():
    return render_template('homepage.html')

@app.route("/robots.txt")
def robotstxt():
    return send_from_directory(app.static_folder, request.path[1:])

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
