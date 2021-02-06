set -e

rm -rf pax_express_client/api
rm -rf pax_express_client/models
rm -rf pax_express_client/client.py
rm -rf pax_express_client/types.py

mkdir tmp
cd tmp
openapi-python-client generate --url http://127.0.0.1:8000/openapi.json --meta=none
rm pax_express_client/__init__.py
rsync -a pax_express_client/ ../pax_express_client/
cd ..
rm -rf tmp