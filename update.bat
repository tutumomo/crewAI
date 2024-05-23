@echo off
echo  請先 Sync Folk 這些項目
start https://github.com/tutumomo/crewAI
start https://github.com/tutumomo/crewAI-examples
start https://github.com/tutumomo/crewai-autocrew
start https://github.com/tutumomo/crewai-experiments
start https://github.com/tutumomo/crewAI-tools
start https://github.com/tutumomo/example-crewai
start https://github.com/tutumomo/CrewaiGeminiPro-Opensourcemodel
pause

echo git pull crewai
git pull
call ac
pip install -U crewai jupyter-ai ipywidgets ollama duckduckgo-search langchain-google-genai unstructured pyowm tools wikipedia yfinance sec-api tiktoken faiss-cpu python-dotenv langchain-community langchain-core openai arxiv
pip install crewai[tools]

call sub_update "crewAI-examples"
call sub_update "crewai-autocrew"
call sub_update "crewai-experiments"
call sub_update "crewAI-tools"
call sub_update "example-crewai"
call sub_update "CrewaiGeminiPro-Opensourcemodel"

echo 更新完成 ~~
pause
