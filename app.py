from flask import Flask, request, render_template_string, jsonify
from scorer import score_transcript

app = Flask(__name__)

INDEX_HTML = '''
<!doctype html>
<title>Nirmaan - Intro Scorer (Demo)</title>
<h2>Nirmaan - Spoken Introduction Scorer (Demo)</h2>
<form method="post" action="/score">
  <textarea name="transcript" rows="12" cols="80" placeholder="Paste transcript here..."></textarea><br/>
  <button type="submit">Score</button>
</form>
<div id="result">{{result|safe}}</div>
'''

@app.route("/", methods=["GET"])
def index():
    return render_template_string(INDEX_HTML, result="")

@app.route("/score", methods=["POST"])
def score():
    transcript = request.form.get("transcript", "").strip()
    if not transcript:
        return render_template_string(INDEX_HTML, result="<p style='color:red'>Please paste a transcript.</p>")
    result = score_transcript(transcript)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
