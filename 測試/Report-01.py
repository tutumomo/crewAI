from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from langchain.tools import tool
import requests
from datetime import datetime
import os

# 加載環境變數
load_dotenv()

# 問使用者要使用的模型
model_choice = input("請選擇您要使用的模型（輸入 '1' 表示使用 Ollama 的 WizardLM2，輸入 '2' 表示使用 OpenAI 的 GPT-4o）：")

if model_choice == '1':
    model = Ollama(model="wizardlm2")
elif model_choice == '2':
    model = ChatOpenAI(model_name="gpt-4o", temperature=0.2)
else:
    raise ValueError("無效的選擇。請重新運行程式並選擇 '1' 或 '2'。")

# 定義工具以從 arXiv 獲取 PDF 論文文章
@tool
def fetch_arxiv_papers(keywords: str) -> str:
    """
    Fetches and preprocesses articles from arXiv given keywords.
    Returns the text of the articles.
    """
    search_url = f"https://export.arxiv.org/api/query?search_query={keywords}&start=0&max_results=5"
    response = requests.get(search_url)
    return response.text  # 這裡應該解析 response 並提取有用資訊

# 定義代理人以提取學術關鍵字
keyword_extractor = Agent(
    role='Keyword Extractor',
    goal='從使用者提供的文字內容中提取相關的學術關鍵字（必須是英文關鍵字）',
    backstory='專門提取文本中的關鍵字和主題',
    verbose=True,
    tools=[],
    allow_delegation=False,
    llm=model
)

# 定義代理人以搜尋 arXiv 論文
arxiv_searcher = Agent(
    role='ArXiv Searcher',
    goal='使用提取的關鍵字在 arXiv 上搜尋相關論文',
    backstory='擅長從 arXiv 中檢索學術論文',
    verbose=True,
    tools=[fetch_arxiv_papers],
    allow_delegation=False,
    llm=model
)

# 定義代理人以列出10個最值得研究的論文方向及論文標題
top_titles_decider = Agent(
    role='Top Titles Decider',
    goal='根據檢索到的論文列出10個最值得研究的論文方向及論文標題（使用繁體中文）',
    backstory='擅長分析和決策學術研究方向',
    verbose=True,
    tools=[],
    allow_delegation=False,
    llm=model
)

# 定義代理人以決定最終的研究方向及論文標題
direction_decider = Agent(
    role='Direction Decider',
    goal='根據10個最值得研究的論文方向及論文標題決定一個最值得研究的方向和標題',
    backstory='擅長分析和決策學術研究方向',
    verbose=True,
    tools=[],
    allow_delegation=False,
    llm=model
)

# 定義代理人以編寫摘要
abstract_writer = Agent(
    role='Abstract Writer',
    goal='編寫論文的摘要部分',
    backstory='專業撰寫學術摘要的專家',
    verbose=True,
    tools=[],
    allow_delegation=False,
    llm=model
)

# 定義代理人以編寫研究方法
methodology_writer = Agent(
    role='Methodology Writer',
    goal='編寫論文的研究方法部分',
    backstory='專業撰寫學術研究方法的專家',
    verbose=True,
    tools=[],
    allow_delegation=False,
    llm=model
)

# 定義代理人以編寫理論基礎
theory_writer = Agent(
    role='Theory Writer',
    goal='編寫論文的理論基礎部分',
    backstory='專業撰寫學術理論基礎的專家',
    verbose=True,
    tools=[],
    allow_delegation=False,
    llm=model
)

# 定義代理人以編寫數據分析
data_analysis_writer = Agent(
    role='Data Analysis Writer',
    goal='編寫論文的數據分析部分',
    backstory='專業撰寫學術數據分析的專家',
    verbose=True,
    tools=[],
    allow_delegation=False,
    llm=model
)

# 定義代理人以編寫結論
conclusion_writer = Agent(
    role='Conclusion Writer',
    goal='編寫論文的結論部分',
    backstory='專業撰寫學術結論的專家',
    verbose=True,
    tools=[],
    allow_delegation=False,
    llm=model
)

# 定義代理人以編寫參考文獻
references_writer = Agent(
    role='References Writer',
    goal='編寫論文的參考文獻部分',
    backstory='專業撰寫學術參考文獻的專家',
    verbose=True,
    tools=[],
    allow_delegation=False,
    llm=model
)

# 定義任務
def keyword_extraction_task(user_content):
    return Task(
        description=f"""從以下使用者提供的文字內容中提取相關的學術關鍵字：
        {user_content}
        關鍵字必須是英文關鍵字。""",
        expected_output="一組相關的學術關鍵字",
        agent=keyword_extractor
    )

def arxiv_search_task(keywords):
    return Task(
        description=f"""使用以下關鍵字在 arXiv 上搜尋相關論文：
        {keywords}""",
        expected_output="一組與關鍵字相關的 arXiv 論文",
        agent=arxiv_searcher
    )

def top_titles_decision_task(papers):
    return Task(
        description=f"""根據以下從 arXiv 檢索到的論文列出10個最值得研究的論文方向及論文標題（使用繁體中文）：
        {papers}""",
        expected_output="10個最值得研究的論文方向及論文標題",
        agent=top_titles_decider
    )

def direction_decision_task(top_titles):
    return Task(
        description=f"""根據以下10個最值得研究的論文方向及論文標題決定一個最值得研究的方向和標題：
        {top_titles}""",
        expected_output="一個最值得研究的論文方向及論文標題",
        agent=direction_decider
    )

def abstract_writing_task(direction_and_title):
    return Task(
        description=f"""根據以下決定的研究方向及論文標題編寫論文的摘要部分：
        {direction_and_title}""",
        expected_output="論文的摘要部分",
        agent=abstract_writer
    )

def methodology_writing_task(direction_and_title):
    return Task(
        description=f"""根據以下決定的研究方向及論文標題編寫論文的研究方法部分：
        {direction_and_title}""",
        expected_output="論文的研究方法部分",
        agent=methodology_writer
    )

def theory_writing_task(direction_and_title):
    return Task(
        description=f"""根據以下決定的研究方向及論文標題編寫論文的理論基礎部分：
        {direction_and_title}""",
        expected_output="論文的理論基礎部分",
        agent=theory_writer
    )

def data_analysis_writing_task(direction_and_title):
    return Task(
        description=f"""根據以下決定的研究方向及論文標題編寫論文的數據分析部分：
        {direction_and_title}""",
        expected_output="論文的數據分析部分",
        agent=data_analysis_writer
    )

def conclusion_writing_task(direction_and_title):
    return Task(
        description=f"""根據以下決定的研究方向及論文標題編寫論文的結論部分：
        {direction_and_title}""",
        expected_output="論文的結論部分",
        agent=conclusion_writer
    )

def references_writing_task(direction_and_title):
    return Task(
        description=f"""根據以下決定的研究方向及論文標題編寫論文的參考文獻部分：
        {direction_and_title}""",
        expected_output="論文的參考文獻部分",
        agent=references_writer
    )

# 使用者輸入
user_content = input("請輸入您的文字內容：")

# 建立 Crew
crew = Crew(
    agents=[
        keyword_extractor, arxiv_searcher, top_titles_decider, direction_decider, 
        abstract_writer, methodology_writer, theory_writer, data_analysis_writer, 
        conclusion_writer, references_writer
    ],
    tasks=[
        keyword_extraction_task(user_content),
        arxiv_search_task("{output[0]}"),
        top_titles_decision_task("{output[1]}"),
    ],
    verbose=2
)

# 執行前3個任務
result = crew.kickoff()

# 調試輸出結果
print(f"Keyword Extraction Task Result: {crew.tasks[0].output.exported_output}")
print(f"Arxiv Search Task Result: {crew.tasks[1].output.exported_output}")
print(f"Top Titles Decision Task Result: {crew.tasks[2].output.exported_output}")

# 獲取 top_titles_decision_task 的輸出結果
top_titles = crew.tasks[2].output.exported_output
print("以下是10個最值得研究的論文方向及論文標題：")
titles = top_titles.split('\n')
for i, title in enumerate(titles, 1):
    print(f"{i}. {title}")

# 讓使用者選擇論文題目
selected_index = int(input("請選擇您想寫的論文題目編號：")) - 1
selected_title = titles[selected_index]

# 重新定義剩餘的任務
tasks = [
    abstract_writing_task(selected_title),
    methodology_writing_task(selected_title),
    theory_writing_task(selected_title),
    data_analysis_writing_task(selected_title),
    conclusion_writing_task(selected_title),
    references_writing_task(selected_title)
]

# 更新 Crew 並執行剩餘任務
crew.tasks.extend(tasks)
result = crew.kickoff()

# 調試每個任務的結果
abstract_result = crew.tasks[4].output.exported_output
methodology_result = crew.tasks[5].output.exported_output
theory_result = crew.tasks[6].output.exported_output
data_analysis_result = crew.tasks[7].output.exported_output
conclusion_result = crew.tasks[8].output.exported_output
references_result = crew.tasks[9].output.exported_output

print("--------------------------")
print(result)

# 將各部分內容合併到最終報告
final_report = f"# {selected_title}\n\n## 摘要\n{abstract_result}\n\n## 研究方法\n{methodology_result}\n\n## 理論基礎\n{theory_result}\n\n## 數據分析\n{data_analysis_result}\n\n## 結論\n{conclusion_result}\n\n## 參考文獻\n{references_result}"

# 將最終報告以 Markdown 格式寫入文件
today = datetime.today().strftime('%Y%m%d')

# 檢查文件名是否存在並自動增加編號
counter = 1
while True:
    filename = f"{today}-{counter:02d}.md"
    if not os.path.exists(filename):
        break
    counter += 1

# 生成報告內容
with open(filename, 'w', encoding='utf-8') as file:
    file.write(final_report)

print(f"報告已寫入文件: {filename}")
