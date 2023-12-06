import os
from flask import Flask, request, render_template
from azure.appconfiguration.provider import load, SettingSelector
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient



app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


blob_service_client = BlobServiceClient(account_url="https://stlzone7682.blob.core.windows.net/", credential=DefaultAzureCredential() )

### Azure App Configuration ###
from azure.appconfiguration import AzureAppConfigurationClient
AppConfigUrl = "https://appcs-demo.azconfig.io"
selects = SettingSelector(key_filter="testapp_settings_*")
azure_app_config = ''
azure_app_config = load(
                        endpoint=AppConfigUrl,
                        credential=DefaultAzureCredential(),
                        selects=[selects],
                        trim_prefixes=["testapp_settings_"]
                   )
app.config.update(azure_app_config)


### App Insights ###
AzureAppInsights_ConnectionString = ''
AzureAppInsights_ConnectionString = app.config.get("appinsight")
if AzureAppInsights_ConnectionString:
    from opencensus.ext.azure.trace_exporter import AzureExporter
    from opencensus.ext.flask.flask_middleware import FlaskMiddleware
    from opencensus.trace.samplers import ProbabilitySampler
    # For website monitoring
    middleware = FlaskMiddleware(
        app,
        exporter=AzureExporter( connection_string=AzureAppInsights_ConnectionString ),
        sampler=ProbabilitySampler(rate=1.0),
    )

@app.route('/')
def index():

    context = {}

    if (azure_app_config):
        azure_app_config.refresh()
        app.config.update(azure_app_config)

    print('Request for index page received')

    args = request.args
    arg_search = args.get("search")

    get_request = {}
    if arg_search != '':
        get_request['search'] = arg_search
        print(arg_search)

    context['search'] = arg_search

    return render_template('index.html', context=context)

@app.route('/appconfig')
def appconfig():

    context = {}

    if (azure_app_config):
        azure_app_config.refresh()
        app.config.update(azure_app_config)
        context['token'] = app.config.get('token')

    print('Request for appconfig page received')


    return render_template('index.html', context=context)

if __name__ == '__main__':
   app.run()