# kacz_scrapper


Steps:
1. install virtual environment (/kacz_scrapper)
python3 -m venv venv

2. activate virtual environmentin (/kacz_scrapper) 
. venv/bin/activate

3. install requirements from requirements.txt (/kacz_scrapper)
pip3 install -r requirements.txt

4. make django migrations (/scrappers)
python3 manage.py makemigrations

5. run django migrate (/scrappers)
python3 manage.py migrate

6. run scrapper (/scrappers)
python3 manage.py kaczmarski_run
