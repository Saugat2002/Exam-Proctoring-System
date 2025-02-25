## Running the backend

cd backend

conda env create -f env.yaml
conda activate proctoring_env


#### Install dependencies
pip install -r requirements.txt

#### Run migrations
python manage.py migrate

#### Start Django server
python manage.py runserver

=====================================================================


### Running the frontend

npm i

npm run start