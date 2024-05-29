from textwrap import dedent
from crewai import Task

class GameTasks():
	def code_task(self, agent, game):
		return Task(description=dedent(f"""You will create a game using python, these are the instructions:

			Instructions
			------------
    	{game}

			輸出代碼並寫入本地"D:\TOMO.Project\crewAI\crewAI-examples\game-builder-crew"資料夾內，檔案名稱依據遊戲命名，並依據-01、-02、-03給定版次，然後執行代碼。
			"""),
			agent=agent
		)

	def review_task(self, agent, game):
		return Task(description=dedent(f"""\
			You are helping create a game using python, these are the instructions:

			Instructions
			------------
			{game}

			Using the code you got, check for errors. Check for logic errors,
			syntax errors, missing imports, variable declarations, mismatched brackets,
			and security vulnerabilities.

			輸出代碼並寫入本地"D:\TOMO.Project\crewAI\crewAI-examples\game-builder-crew"資料夾內，檔案名稱依據遊戲命名，並依據-01、-02、-03給定版次，然後執行代碼。
			"""),
			agent=agent
		)

	def evaluate_task(self, agent, game):
		return Task(description=dedent(f"""\
			You are helping create a game using python, these are the instructions:

			Instructions
			------------
			{game}

			You will look over the code to insure that it is complete and
			does the job that it is supposed to do.

			輸出代碼並寫入本地"D:\TOMO.Project\crewAI\crewAI-examples\game-builder-crew"資料夾內，檔案名稱依據遊戲命名，並依據-01、-02、-03給定版次，然後執行代碼。
			"""),
			agent=agent
		)