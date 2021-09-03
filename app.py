import os
from flask import Flask, send_file,send_from_directory, render_template, request
from comboparser import *
app = Flask(__name__)

b = "d0c6d5c-custom"
c = "Sat, Aug 21, 2021 12:19:03 PM"
@app.route("/LatestVersion")
def latest():
    return "3.1.001"
@app.route("/LatestVersionDev")
def latestdev():
    return f"3.1.001\n{b}\n{c}"
@app.route("/PreviousVersion")
def prev():
    return "3.1.001"
@app.route("/PreviousVersionDev")
def prevdev():
    return f"3.1.001\n{b}\n{c}"

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
def maketrial():
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
  except Exception as e:
      return f"Error encountered, please send input for debugging: \n {e!r}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
