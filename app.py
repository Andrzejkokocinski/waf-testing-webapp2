import os
import json
from flask import (Flask, request, render_template)

appinsight=''
config_settings=''

#from azure.appconfiguration import AzureAppConfigurationClient
#CONNECTION_STRING = "Endpoint=https://appcs-owasp-87562349798.azconfig.io;Id=HERh;Secret=+mh3UViOcXdzi7Rid3ZXNjRBjSxMOtxlqo75H2i0xlo="
#client = AzureAppConfigurationClient.from_connection_string(CONNECTION_STRING)
#config_settings = client.get_configuration_setting(key="testtoken")
#appinsight = client.get_configuration_setting(key="appinsight")

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

if appinsight:
    from opencensus.ext.azure.trace_exporter import AzureExporter
    from opencensus.ext.flask.flask_middleware import FlaskMiddleware
    from opencensus.trace.samplers import ProbabilitySampler
    # For website monitoring
    AzureAppInsights_ConnectionString = 'InstrumentationKey=3712782d-691c-47d4-bef1-52ae3c0f7dc1;IngestionEndpoint=https://northeurope-2.in.applicationinsights.azure.com/;LiveEndpoint=https://northeurope.livediagnostics.monitor.azure.com/'

    if AzureAppInsights_ConnectionString:
        middleware = FlaskMiddleware(
            app,
            exporter=AzureExporter( connection_string=AzureAppInsights_ConnectionString ),
            sampler=ProbabilitySampler(rate=1.0),
        )

@app.route('/')
def index():
    args = request.args
    arg_search = args.get("search")

    get_request = {}
    if arg_search != '':
        get_request['search'] = arg_search

    return render_template('index.html', request=get_request, config_settings="")

@app.route('/appconfig')
def appconfig():
    return render_template('index.html', config_settings=config_settings)
