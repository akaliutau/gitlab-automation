import datetime
import os
from typing import List

import gitlab

from constants import HOST_PROJECT, OLG_GITLAB_URL, GL_PROJECT_ID, DASHBOARD_ID
from gcp import BigQuery


def get_template(file: str, params: dict) -> str:
    return open(file, 'r').read().format_map(params)


def get_sites(sites: List[str]) -> str:
    return '\n'.join([f'* [ ] {s}' for s in sites])


def get_completed(sites: List[str]) -> str:
    return '\n'.join([f'* [x] {s}' for s in sites])


def main() -> None:
    token = os.environ.get('PAT_TOKEN')
    gl = gitlab.Gitlab(OLG_GITLAB_URL, private_token=token, timeout=30, ssl_verify=True)
    print(gl.version())
    osp_project = gl.projects.get(GL_PROJECT_ID)
    issues = osp_project.issues.get(1)
    print(issues)
    deployment_board = osp_project.boards.get(id=DASHBOARD_ID)
    print(deployment_board)
    print('creating an issue')
    today = datetime.datetime.now()

    pipeline = 13365057

    params = {
        'applications': '`app-name-1`',
        'pipeline': f'https://gitlab.com/automation299/gitlab-automation/-/pipelines/{pipeline}',
        'sites': get_sites(['site-1', 'site-2']),
        'approach': 'DEPLOY_IN_PARALLEL'
    }

    template = get_template('templates/ticket.templ', params=params)

    issue = osp_project.issues.create(
        {'title': f'Deployment #{pipeline} ({today})', 'description': template, 'labels': 'deployments'})

    osp_project.issues.update(id=issue.get_id(), new_data={'description': template})
    result = f"""
    Deployment #{pipeline} has finished.
    Successful jobs: 2
    Failed jobs: 0
    """
    osp_project.issues.get(issue.get_id()).discussions.create({'body': result})

    print(issue)

    bq = BigQuery(project_id=HOST_PROJECT)


if __name__ == "__main__":
    main()
