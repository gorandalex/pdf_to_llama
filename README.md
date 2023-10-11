### DocuBot

<img src="docubot.jpg" align="center" style="width: 550px"  />

## REST API Service for work and analyze pdf files

This is a REST API service that allows users to upload and recognize of text from PDF files. Due to LLM technologies it allows to get only necessary information 

### Technologies

HTML/CSS
JavaScript 
Python
SqlAlchemy 
Redis
Faiss
OpenAI



### The API supports the following features:

- User registration and authentication
- Uploading and storing pdf and text files
- Adding  tags  to files and filtering them by tags
- Recognizing of text in pdf and store it 
- Chat options and issues about information in files


### How to start the API
Firstly add .env file to the main folder with data as in .env.example

Start Docker and run the next command for starting the API, PostgreSQL and REDIS:

docker-compose up -d

Make migrations for creating/updating database:

alembic upgrade head

After that you can go to http://127.0.0.1:8000

Than you can Sign In or Sign UP, download your files (5 docs are acceptable) and ask questions in chat (click the name of doc to open the window with chat) for getting info from your doc.

The file's size for downloading depend on the user's level (by default no more than 5 MB). You also can use no more than 50K tokens for your questions per 24 hours.


### Our Team 3:

Developer + Team Lead : [Andriy Gorobets](https://github.com/gorandalex)

Developer + Scrum Muster: [Natalia Sokil](https://github.com/Natalkina)

Developer: [Kateryna Pomazunova](https://github.com/KatePomazunova)

Developer:  [Andriy Martynyuk](https://github.com/MartynyukAndriy)

Developer: [Tetiana Kondra](https://github.com/tetianakondra/)
