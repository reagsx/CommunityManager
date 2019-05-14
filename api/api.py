from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
sys.path.insert(0, "/home/chris/Community_Manager")
from tools import sqlhelpers

app = Flask(__name__)
CORS(app)

@app.route('/guildlist', methods=['GET'])
def get_guildlist():
  return jsonify(sqlhelpers.json_ready_guild_list())

@app.route('/attendance', methods=['GET'])
def get_attendance():
  startdate = request.args.get('startdate')
  enddate = request.args.get('enddate')
  return jsonify(sqlhelpers.get_attendance_list(startdate,enddate))

@app.route('/events')
def get_events():
  return jsonify(sqlhelpers.event_list())

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000, threaded=True)