# kris-interview-chatbot
kris interview chatbot


Use OpenAI Chat Completion / Function Calling API to implement an end to end Chat Assistant (with custom retreival tool (RAG))

get a frontend template and modify it to a chatbox.
use websocket
create fastApi server

### run project

#### run server
install requirements packages
```shell
pip install -r requirements.txt
```

you need create .env file in root directory.and confirm those config in it.
```
DEBUG=True

OPENAI_API_KEY='your openai api key'
```

run this script in root directory.
```shell
uvicorn main:app 
```

#### run web

entry web directory
```shell
cd web
```

install dependencies
```shell
yarn
```

run web
```
yarn dev
```
