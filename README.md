## Running the backend

cd backend

conda env create -f env.yml

conda activate exam_proctoring_env


#### Run migrations
python manage.py migrate

#### Start Django server
python manage.py runserver

=====================================================================


### Running the frontend

#### Install the required packages
npm i

#### Start the frontend
npm run start
