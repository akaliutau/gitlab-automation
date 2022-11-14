echo execiting plan command

cd scripts || exit 1
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt

python3 pipeline_generator.py -o pipeline.yml

