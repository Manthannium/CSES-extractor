# web scraping libraries
from bs4 import BeautifulSoup
import requests
import shutil

MAX_LIMIT = 3  # 300 for all

def createSession(username, password):
	loginData = {
		'nick': username,
		'pass': password
	}
	with requests.Session() as session:
		url = 'https://cses.fi/login'
		soup = BeautifulSoup(session.get(url).content, 'html.parser')
		loginData['csrf_token'] = soup.find('input', attrs = {'name':'csrf_token'})['value']
		response = session.post(url, data = loginData)
		return session
	
def getQuestions(session):
	questions = dict()
	response = session.get(r'https://cses.fi/problemset/').content
	soup = BeautifulSoup(response, 'html.parser')
	
	for t in soup.find_all('li', class_ = 'task'):
		questionID = t.a['href'].split('/')[-1]  # 1146
		questionName = t.a.string                # Weird Algorithm
		questionDetail = t.span.string           # 1200 / 1560
		questions[questionID] =  {"name": questionName, "detail": questionDetail}
	return questions

def findCorrectSolutionLink(session, question):
	response = session.get(r"https://cses.fi/problemset/view/" + question + "/").content
	soup = BeautifulSoup(response,'html.parser')
	total_submissions = int(soup.find('p').string.split()[-1])
	
	if total_submissions == 0: 
		return None

	for link in soup.find_all('a', attrs = {'class':'details-link'}):
		solution = link['href']
		status = soup.find('a', href = solution, class_ = '').span['class'][2] 
		if status == 'full':
			return 'https://cses.fi' + solution
	return None

def getSolutionCode(session, question, solution_link):
	response = session.get(solution_link).content
	soup = BeautifulSoup(response, 'html.parser')
	code = soup.find('pre', class_ = "linenums").get_text()
	# language = soup.find('table', class_ = "summary")
	return code

def createFile(questions, question, code):
	ext = '.cpp'	# change if you use other programming language
	path = 'output/' + question + ' - ' + questions[question]["name"] + ext
	file = open(path, 'w')
	file.writelines(code.split('\n'))
	file.close()
	
def run(username,  password):
	session = createSession(username, password)
	questions = getQuestions(session)
	
	maxlimit = MAX_LIMIT
	for question in questions:
		solution = findCorrectSolutionLink(session, question)
		if not solution:
			continue
		code = getSolutionCode(session, question, solution)
		createFile(questions, question, code)
		maxlimit -= 1
		if maxlimit == 0:
			break

	shutil.make_archive("compressed", 'zip', "output")

if __name__ == "__main__":
	username = input('username: ')
	password = input('password: ')
	session = createSession(username, password)
	questions = getQuestions(session)

	maxlimit = MAX_LIMIT
	for question in questions:
		solution = findCorrectSolutionLink(session, question)
		if not solution:
			continue
		code = getSolutionCode(session, question, solution)
		createFile(questions, question, code)
		maxlimit -= 1
		if maxlimit == 0:
			break