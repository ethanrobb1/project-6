"""
CS322 Project 4-5-6
Replacement for RUSA ACP brevet time calculator
Name: Ethan Robb
"""
import flask
import arrow 
import acp_times  
import logging

from os import environ as env

###
# Globals
###

app = flask.Flask(__name__)

def get_server_error(error_msg: str) -> flask.Response:
    err_dict = {"error": error_msg}
    err_resp = flask.jsonify(err_dict)
    err_resp.status_code = 500
    return err_resp

###
# Pages
###

@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(_):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404

###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############

@app.get("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from km, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of km.
    """
    app.logger.debug("Got a JSON request")

    brevet_dist = flask.request.args.get('brevet', None, type=int)
    control_dist = flask.request.args.get('control', None, type=float)
    start_time = flask.request.args.get('start', None, type=arrow.get)

    app.logger.debug(f"brevet={brevet_dist}")
    app.logger.debug(f"control={control_dist}")
    app.logger.debug(f"start={start_time}")
    app.logger.debug(f"request.args: {flask.request.args}")

    try:
        open_time = acp_times.open_time(control_dist, brevet_dist, start_time).format('YYYY-MM-DDTHH:mm')
        close_time = acp_times.close_time(control_dist, brevet_dist, start_time).format('YYYY-MM-DDTHH:mm')
    except ValueError as exc:
        return get_server_error(str(exc))
    except TypeError:
        return get_server_error("A server error occurred.")

    return {"open": open_time, "close": close_time}


#############

if "DEBUG" in env and env["DEBUG"].lower() == "true":
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print(f"Opening for global access on port {env['PORT']}")
    app.run(port=int(env["PORT"]), host="0.0.0.0")
