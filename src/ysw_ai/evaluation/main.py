from .utils.logger import logger
from .utils.config import config
import json
import base64

from flask import Flask, render_template, request
import webbrowser
import os
from flask_cors import CORS

import lambdaTTS
import lambdaSpeechToScore
import lambdaGetSample


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = '*'

rootPath = ''


@app.route(rootPath+'/')
def main():
    return render_template('main.html')


@app.route(rootPath+'/getAudioFromText', methods=['POST'])
def getAudioFromText():
    event = {'body': json.dumps(request.get_json(force=True))}
    return lambdaTTS.lambda_handler(event, [])


@app.route(rootPath+'/getSample', methods=['POST'])
def getNext():
    event = {'body':  json.dumps(request.get_json(force=True))}
    return lambdaGetSample.lambda_handler(event, [])


@app.route(rootPath+'/GetAccuracyFromRecordedAudio', methods=['POST'])
def GetAccuracyFromRecordedAudio():

    try:
        event = {'body': json.dumps(request.get_json(force=True))}
        lambda_correct_output = lambdaSpeechToScore.lambda_handler(event, [])
    except Exception as e:
        print('Error: ', str(e))
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Credentials': "true",
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': ''
        }

    return lambda_correct_output

def main():
    app_name = config.get("app.name", "Unknown App")
    version = config.get("app.version", "0.0.0")
    
    logger.info(f"Starting {app_name} v{version}")
    logger.info("Hello from ysw_ai!")
    language = 'en'
    app.run(host="0.0.0.0", port=3000)


if __name__ == "__main__":
    main()
