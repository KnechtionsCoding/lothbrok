from flask import Flask, request, Response
import json
from lothbrok import main as lothbrok
import logging

app = Flask(__name__)

# Ability to accept artifactory webhooks
# Example json
"""
{
   "repo_key":"docker-remote-cache",
   "path":"library/ubuntu/latest/list.manifest.json",
   "name":"list.manifest.json",
   "sha256":"35c4a2c15539c6c1e4e5fa4e554dac323ad0107d8eb5c582d6ff386b383b7dce",
   "size":1206,
   "image_name":"library/ubuntu",
   "tag":"latest",
   "platforms":[
      {
         "architecture":"amd64",
         "os":"linux"
      },
      {
         "architecture":"arm",
         "os":"linux"
      },
      {
         "architecture":"arm64",
         "os":"linux"
      },
      {
         "architecture":"ppc64le",
         "os":"linux"
      },
      {
         "architecture":"s390x",
         "os":"linux"
    }
  ]
}
"""


@app.route("/webhook/artifactory", methods=["POST"])
def respond():
    data = request.get_json()
    try:
        response = lothbrok.entrypoint(data["image_name"], data["tag"])
        return Response(response[0], response[1])
    except Exception as e:
        logging.error(e)
        return Response(status=500)


if __name__ == "__main__":
    app.run()
