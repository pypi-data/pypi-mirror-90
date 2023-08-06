import json
import os

import requests

if 'GITLAB_ACCESS_TOKEN' not in os.environ:
    raise Exception('GITLAB_ACCESS_TOKEN required')

headers = {'Private-Token': os.environ['GITLAB_ACCESS_TOKEN']}


def trigger_pipeline(project_id, branch='master'):
    url = 'https://gitlab.com/api/v4/projects/%s/pipeline?ref=%s' % (project_id, branch)
    res = requests.post(url=url, headers=headers)
    res_dict = json.loads(res.text)
    return res_dict['id'], res_dict['web_url']


def get_pipeline(project_id, pipeline_id):
    url = 'https://gitlab.com/api/v4/projects/%s/pipelines/%s' % (project_id, pipeline_id)
    res = requests.get(url=url, headers=headers)
    return json.loads(res.text)

def get_jobs(project_id, pipeline_id):
    url = 'https://gitlab.com/api/v4/projects/%s/pipelines/%s/jobs' % (project_id, pipeline_id)
    res = requests.get(url=url, headers=headers)
    return json.loads(res.text)
