from flask import Flask, request, session, redirect, url_for, render_template_string, make_response

app = Flask(__name__)
app.secret_key = 'supersecret'  # Needed for session security

form_html = """
<div style=" font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif">
<h1 style=" text-align: center; font-size: 3rem"> Login Actions </h1>
<form method="POST" style="text-align: center">
  Enter username: <input type="email" name="txn">
  <br><br>
  Enter password: <input type="password" required>
  <br><br>
  <input type="submit" value="Submit" style="padding: 5px; font-size: 15px; background-color: rgb(15, 204, 204); border-radius: 10px;">
</form>
<ul>
{% for t in transactions %}
  <li>
    {{ t }}
    <form method="POST" action="{{ url_for('delete_transaction') }}" style="display: inline;">
      <input type="hidden" name="index" value="{{ loop.index0 }}">
      <input type="submit" value="Delete" style="margin-left: 10px; padding: 5px; font-size: 15px; background-color: rgb(15, 204, 204); border-radius: 10px;">
    </form>
  </li>
{% endfor %}
</ul>
</div>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if 'transactions' not in session:
        session['transactions'] = []

    if request.method == "POST" and request.form.get("txn"):
        txn = request.form.get("txn")
        session['transactions'].append(txn)
        session.modified = True
        return redirect(url_for("home"))  # <-- Redirect to avoid duplicate POST on refresh

    return render_template_string(form_html, transactions=session['transactions'])

@app.route("/delete", methods=["POST"])
def delete_transaction():
    if 'transactions' in session:
        index = int(request.form.get('index'))
        if 0 <= index < len(session['transactions']):
            session['transactions'].pop(index)
            session.modified = True
    return redirect(url_for('home'))

@app.route("/set_cookie")
def set_cookie():
    resp = make_response("Cookie is set")
    resp.set_cookie("userID", "123ABC")
    return resp

@app.route("/get_cookie")
def get_cookie():
    user_id = request.cookies.get("userID")
    return f"User ID from cookie: {user_id}"

if __name__ == "__main__":
    app.run(debug=True)
