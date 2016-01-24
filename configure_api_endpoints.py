import argparse


ANGULAR = "angular.module('conf', [])\
.constant('API_END_POINT', \
'{endpoint}');"

parser = argparse.ArgumentParser(
    description='Set API endpoints for www and admin_www.'
)

parser.add_argument(
    '-e',
    '--environment',
    required=True,
    type=str,
    action='store',
    choices=['staging', 'production', 'local'],
)
args = parser.parse_args()

tmp = {
    'local': ANGULAR.format(
        endpoint='http://localhost:5000/api/v1'
    ),
    'production': ANGULAR.format(
        endpoint='https://festeasy-production.herokuapp.com/api/v1'
    ),
    'staging': ANGULAR.format(
        endpoint='https://festeasy-staging.herokuapp.com/api/v1'
    ),
}

data = {
    'www/src/app/settings.coffee': tmp[args.environment],
    'admin_www/src/app/settings.coffee': tmp[args.environment],
}

for path, line in data.items():
    with open(path, 'w') as f:
        f.write(line)
        print("Wrote '{line}' into {path}".format(line=line, path=path))