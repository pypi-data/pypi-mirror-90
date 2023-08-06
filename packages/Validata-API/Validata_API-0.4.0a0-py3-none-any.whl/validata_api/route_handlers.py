# validata-api -- Validata Web API
# By: Validata Team <pierre.dittgen@jailbreak.paris>
#
# Copyright (C) 2018 OpenDataFrance
# https://git.opendatafrance.net/validata/validata-api
#
# validata-api is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# validata-api is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


"""
Application route handlers.
"""

import json
import logging
import urllib
from io import BytesIO

import cachetools
import requests
from flask import request

import validata_core
from validata_core.helpers import FileContentValidataResource, URLValidataResource

from . import app, config
from .json_errors import abort_json, make_json_response

# Schema cache size (nb of simultaneously stored schemas)
SCHEMA_CACHE_SIZE = 20
# Schema time to live (in seconds)
SCHEMA_CACHE_TTL = 60


log = logging.getLogger(__name__)


def bytes_data(f):
    """Gets bytes data from Werkzeug FileStorage instance"""
    iob = BytesIO()
    f.save(iob)
    iob.seek(0)
    return iob.getvalue()


@app.route('/')
def index():
    apidocs_href = "{}/apidocs".format(config.SCRIPT_NAME)
    apidocs_url = urllib.parse.urljoin(request.url, apidocs_href)
    return make_json_response({
        "apidocs_href": apidocs_href,
        "message": "This is the home page of Validata Web API. Its documentation is here: {}".format(apidocs_url)
    }, args=None)


@cachetools.cached(cachetools.TTLCache(SCHEMA_CACHE_SIZE, SCHEMA_CACHE_TTL))
def download_schema(schema_url):
    """Download schema by its given url"""

    return requests.get(schema_url).json()


@app.route('/validate', methods={"GET", "POST"})
def validate():
    # Extract parameters

    if request.method == 'GET':
        args = {
            'schema': request.args.get('schema'),
            'url': request.args.get('url'),
        }
    else:
        assert request.method == 'POST', request.method
        args = {
            'schema': request.form.get('schema'),
        }

    if not args['schema']:
        abort_json(400, args, 'Missing or empty "schema" parameter')

    # Download Schema from URL to get control on cache
    # schema json dict is passed to validate function as a dict
    try:
        schema_dict = download_schema(args['schema'])
    except Exception as err:
        abort_json(400, {}, str(err))

    validata_resource = None

    if request.method == 'GET':
        # URL validation
        if not args['url']:
            abort_json(400, args, 'Missing or empty "url" parameter')
        validata_resource = URLValidataResource(args['url'])

    elif request.method == 'POST':
        # Uploaded file validation
        f = request.files.get('file')
        if f is None:
            abort_json(400, args, 'Missing or empty "file" parameter')
        validata_resource = FileContentValidataResource(f.filename, bytes_data(f))

    header, rows = validata_resource.extract_tabular_data()
    validation_report = validata_core.validate([header] + rows, schema_dict)

    body = {
        'report': validation_report.to_dict(),
    }

    # badge info
    if config.BADGE_CONFIG is not None:
         body["badge"] = validata_core.compute_badge_metrics(validation_report, config.BADGE_CONFIG)

    return make_json_response(body, args)
