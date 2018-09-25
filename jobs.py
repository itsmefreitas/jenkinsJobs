from jenkinsapi.jenkins import Jenkins
from datetime import datetime
import sqlite3

# Jenkins-specific sign-in data and connection procedure.
# 1112e0fd5a9f4ff43ded19b449ab7f1c2a - jenkins-generated API token.

host = 'http://localhost:8080'
usr = 'luis'
apiToken = '1112e0fd5a9f4ff43ded19b449ab7f1c2a'

server = Jenkins(host, usr, apiToken)

# Sqlite connection handling

def sqlConnect(fileName):
	sqlSession = sqlite3.connect(fileName)
	sqlSession.text_factory = str
	return (sqlSession, sqlSession.cursor())

def sqlCommit(sqlSession):
	sqlSession.commit()
	sqlSession.close()

# Utility getStrTime function as string
def getStrTime():
	time = datetime.now()
	return time.strftime('%Y/%m/%d %H:%M:%S')

# Jenkins API job data fetching

def getJobsData():

	session = sqlConnect('jobs.db')

	for job_name, job_instance in server.get_jobs():
		if job_instance.is_running():
			status = 'RUNNING'
		elif job_instance.get_last_build_or_none() == None :
			status = 'NOTBUILT'
		else:
			simple_job = server.get_job(job_instance.name)
			simple_build = simple_job.get_last_build()
			status = simple_build.get_status()

		row = (job_name, status, getStrTime())

		session[1].execute('SELECT ID FROM job WHERE job_name = ?',(job_name,))
		result = session[1].fetchone()

		if result is None:
			session[1].execute('INSERT INTO job (job_name, job_status, time) VALUES (?,?,?)',row)
		else:
			session[1].execute('UPDATE job SET job_status = ?, time = ? WHERE ID = ?',(row[1],row[2],result[0],))

		print (session[1].execute('SELECT * FROM job WHERE job_name = ?',(job_name,))).fetchone()

	return session[0]
			

if __name__ == "__main__":
	sqlCommit(getJobsData())