"""application entry point."""
from frontend import create_app
from flask import render_template

app = create_app()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.jinja2'), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0")