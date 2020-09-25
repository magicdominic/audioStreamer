#!/usr/bin/env python3

import subprocess
from flask import Flask, request, abort
import re

app = Flask(__name__)

ffplay_proc = None

# rudimentary input filtering...
#ip_regex = re.compile('[0-9.:]+')

@app.route('/start', methods=['POST'])
def start():
    global ffplay_proc

    if not 'IP' in request.form:
        print("missing IP parameter")
        abort(400) # malformed request

    #if not ip_regex.match(request.form['IP']):
        #print("invalid IP")
        #abort(400)

    if ffplay_proc:
        try:
            print("stopping previous instance...")
            ffplay_proc.terminate()
            ffplay_proc.wait(2)
        except subprocess.TimeoutExpired:
            print("failed to properly terminate ffplay")
            ffplay.kill()


    cmd = ['ffplay', 'rtsp://{}'.format(request.form['IP']), '-nodisp']

    print("executing:", " ".join(cmd))
    ffplay_proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    print("started ffplay")
    print("status:", ffplay_proc.poll())

    return "OK"

@app.route('/status')
def status():
    global ffplay_proc

    if ffplay_proc:
        ret = ffplay_proc.poll()
        if ret is None:
            return "ffplay running"
        else:
            stdout, stderr = ffplay_proc.communicate()
            if stderr:
                stderr = stderr.decode('utf8').replace('\n', '<br>\n')
            if stdout:
                stdout = stdout.decode('utf8').replace('\n', '<br>\n')
            return "ffplay stopped with return value {}\n<h2>Errors</h2>\n{}\n<h2>Output</h2>\n{}\n".format(ret, stderr, stdout)
        ffplay_proc = None # otherwise subsequent communicate() calls fail
    else:
        return "ffplay not started"


@app.route('/wake')
def wake():
    subprocess.check_call(["xdotool", "key", "Up"])
