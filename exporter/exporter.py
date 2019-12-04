import requests
from flask import Flask
from flask_restful import Api, Resource
import yaml
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
api = Api(app)

# val = 0
response_to_be_sent = ''


def service_status():
    with open('exporter_config.yaml', 'r') as stream:
        try:
            file = yaml.safe_load(stream)
            for url in file.get('url'):
                name = url.get('name')
                end_point = url.get('URL')
                data = url.get('data_validation')
                for env in url.get('applicable_env'):
                    final_url = file.get('env')[0].get(env) + end_point
                    resp = requests.get(final_url)
                    if data in resp.content.decode("utf-8"):
                        global response_to_be_sent
                        response_to_be_sent = response_to_be_sent + 'service_status{name="' + name + '"env="' + env + \
                                              '", url="' + final_url + '"} 1\n'
                    else:
                        response_to_be_sent = response_to_be_sent + 'service_status{name="' + name + '"env="' + env + \
                                              '", url="' + final_url + '"} 0\n'

        except yaml.YAMLError as exc:
            print(exc)


class exporter(Resource):
    def get(self):
        global response_to_be_sent
        response_to_be_sent = ''
        service_status()
        data = response_to_be_sent.split('\n')
        response = app.response_class(response=response_to_be_sent, status=200)
        response.headers["content-type"] = "text/plain"
        return response


api.add_resource(exporter, '/metrics')  # Route_1

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5002')
# if __name__ == '__main__':
#     test_method()
#     # global response_to_be_sent
#     print(response_to_be_sent)
#     # print(val)
