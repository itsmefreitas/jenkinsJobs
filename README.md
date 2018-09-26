# jenkinsJobs

Jenkins (http://jenkins-ci.org/) is an open source continuous integration server.

This is a script, in Python, that uses Jenkins' API to get a list of jobs and their status from a given Jenkins instance.
The status for each job is stored in a sqlite database along with the time for when it was checked.

An API token is used for security reasons, which can be revoked at any time from the corresponding running jenkins instance.
