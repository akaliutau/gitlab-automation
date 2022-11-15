import argparse
import copy

from utils import YAML

variables = {
    'variables': {
        'DOCKER_DRIVER': 'overlay2'
    }
}

stages = {
    'stages': ['closure']
}

base_image = {
    '.base_image': {
        'image': '$RUNNER_CUSTOM_IMAGE'
    }
}

deployment_base = {
    '.deployment_base': {
        'extends': ['.base_image'],
        'rules': ['allow_failure: true'],
        'tags': ['saas-linux-medium-amd64']
    }
}

deployment = {
    'deployment': {
        'extends': ['.deployment_base'],
        'stage': '',
        'script': [],
        'variables': {}
    }
}

closure_job = {
    'closure_job': {
        'extends': ['.deployment_base'],
        'stage': 'closure',
        'script': ['exit 0']
    }
}


class Site:
    def __init__(self, name: str, env_vars: dict = None):
        self.name = name
        self.env_vars = env_vars or dict()


class Job:
    def __init__(self, name: str, script: str, env_vars: dict = None, ref: list = None):
        self.name = name
        self.ref = ref or list()
        self.env_vars = env_vars or dict()
        self.script = script


site_map = [
    Site(name='site_1', env_vars={'LOCATION': 'us-east-1', 'ENVIRONMENT': 'site_1_env'}),
    Site(name='site_2', env_vars={'LOCATION': 'us-east-2', 'ENVIRONMENT': 'site_2_env'}),
    Site(name='site_3', env_vars={'LOCATION': 'europe-west-2', 'ENVIRONMENT': 'site_3_env'})
]


def create_job(site: Site, job: Job, pipeline: YAML, bootstrap_map: dict) -> None:
    stage_name = 'deploy_' + job.name
    deployment_section_name = normalise_name('deployment:' + site.name + ':' + job.name)

    deployment_copy = copy.deepcopy(deployment)
    deployment_copy['deployment']['stage'] = stage_name
    deployment_copy['deployment']['script'].append('source ' + job.script)
    deployment_copy['deployment']['variables'].update(site.env_vars)
    deployment_copy['deployment']['variables'].update(job.env_vars)

    deployment_section = dict()
    deployment_section[deployment_section_name] = deployment_copy.get('deployment')
    pipeline.add(deployment_section_name, deployment_section)
    bootstrap_map[job.name] = deployment_section_name


def normalise_name(name: str) -> str:
    return name.replace('_', '-') if name else name


def link(job_name: str, target: dict, to: str) -> None:
    if 'needs' not in target[job_name]:
        target[job_name]['needs'] = []
    target[job_name]['needs'].append(to)


def bootstrap(source: str, refs: list, bootstrap_map: dict, pipeline: YAML) -> None:
    if source == 'before':
        for ref in refs:
            j_name = bootstrap_map.get(ref)
            link(job_name = j_name, target=pipeline.get(j_name), to=bootstrap_map.get('before'))
    else:
        for ref in refs:
            j_name = bootstrap_map.get('after')
            link(job_name=j_name, target=pipeline.get(j_name), to=bootstrap_map.get(ref))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generates pipeline configuration in YAML format')
    parser.add_argument('-o', '--out', help='filename of output yml', required=True)

    args = vars(parser.parse_args())
    print(args)
    deployments = dict()
    yaml = YAML()
    yaml.add('variables_section', copy.deepcopy(variables))
    yaml.add('stages_section', copy.deepcopy(stages))
    yaml.add('base_image_section', copy.deepcopy(base_image))
    yaml.add('deployment_base_section', copy.deepcopy(deployment_base))
    yaml.add('closure_job_section', copy.deepcopy(closure_job))


    jobs = [
        Job(name='before', env_vars={'APP': 'app-name-1,app-name-2'}, script='scripts/before-deploy.sh', ref=['app-name-1']),
        Job(name='app-name-1', env_vars={'APP': 'app-name-1'}, script='scripts/deploy.sh'),
        Job(name='app-name-2', env_vars={'APP': 'app-name-2'}, script='scripts/deploy.sh'),
        Job(name='after', env_vars={'APP': 'app-name-1,app-name-2'}, script='scripts/after-deploy.sh', ref=['app-name-2'])
    ]

    for selected_site in site_map:
        bs_map = dict()
        for selected_job in jobs:
            create_job(job=selected_job, site=selected_site, pipeline=yaml, bootstrap_map=bs_map)
        # TODO one can simplify - use needs for all sequence of jobs, drop 2nd loop
        for selected_job in jobs:
            if selected_job.ref:
                bootstrap(source=selected_job.name, refs=selected_job.ref, bootstrap_map=bs_map, pipeline=yaml)

    add_stages = ['deploy_' + job.name for job in jobs]
    yaml.get('stages_section').get('stages').extend(add_stages)
    pipeline_str = yaml.to_string()
    print(pipeline_str)
    with open(args.get('out'), 'w+') as f:
        f.write(pipeline_str)
