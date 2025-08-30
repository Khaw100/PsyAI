from agents.classificationAgent import ClassificationAgent
from tools.toolInitializer import ToolInitializer
from load_env import get_gemini_client

client = get_gemini_client()
tools = ToolInitializer().setup()
clf = ClassificationAgent(client, tools, "gemini-1.5-flash")

print(clf.run("I feel sad and hopeless"))
print(clf.prompt)
print(clf.context)
print(100*'=')
print(clf.run("I’m nervous and can't sleep before exams"))
