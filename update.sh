#!/bin/bash

# ���}�s�����óX��GitHub�ܮw
open "https://github.com/tutumomo/crewAI"
open "https://github.com/tutumomo/crewAI-examples"
open "https://github.com/tutumomo/crewai-autocrew"
open "https://github.com/tutumomo/crewai-experiments"
open "https://github.com/tutumomo/crewAI-tools"
open "https://github.com/tutumomo/example-crewai"
open "https://github.com/tutumomo/CrewaiGeminiPro-Opensourcemodel"

# ���ݤ@�q�ɶ��H�T�O�s�����[������
sleep 5

# ����git pull
echo "git pull crewai"
git pull

# �ե�ac�}���]���]ac�O�@��Shell�}�����^
./ac.sh

# �w��Python�]
pip3 install -U crewai jupyter-ai ipywidgets ollama duckduckgo-search langchain-google-genai unstructured pyowm tools wikipedia yfinance sec-api tiktoken faiss-cpu python-dotenv langchain-community langchain-core openai arxiv

# �J���Χ�sGitHub�ܮw
clone_or_pull() {
    if [ ! -d "$1" ]; then
        git clone "$2"
    else
        cd "$1"
        git pull
        cd ..
    fi
}

clone_or_pull "crewAI-examples" "https://github.com/tutumomo/crewAI-examples.git"
clone_or_pull "crewai-autocrew" "https://github.com/tutumomo/crewai-autocrew.git"
clone_or_pull "crewai-experiments" "https://github.com/tutumomo/crewai-experiments.git"
clone_or_pull "crewAI-tools" "https://github.com/tutumomo/crewAI-tools.git"
clone_or_pull "example-crewai" "https://github.com/tutumomo/example-crewai.git"
clone_or_pull "CrewaiGeminiPro-Opensourcemodel" "https://github.com/tutumomo/CrewaiGeminiPro-Opensourcemodel.git"

echo "��s���� ~~"
