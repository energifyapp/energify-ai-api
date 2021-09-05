from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)

INFORMATION = {}

# https://url.com/form?params=<info>
@app.route("/form", methods=["GET"])
def get():
    # This part gets the info from the parameters
    data = request.args.get("params")
    INFORMATION['data'] = data
    # This part redirects the user to response.html after getting the data
    return redirect("/response")

# This function is just to return the jsonified info and nothing else

def response():
    # Json should look something like: {'data': (data)}
    info = jsonify(INFORMATION)
    return info

if __name__ == "__main__":
    app.run()