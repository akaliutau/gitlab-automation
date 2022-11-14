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
        'only': {
            'variables': ['$DEPLOYMENT']
        },
        'tags': ['saas-linux-medium-amd64']
    }
}

deployment_vars = {
    '.deployment_vars': {
        'stage': 'stage_placeholder',
        'variables': {
            'LOCATION': 'location_placeholder',
            'ENVIRONMENT': 'environment_placeholder',
        }
    }
}

deployment = {
    'deployment': {
        'extends': ['.deployment_base'],
        'script': ['source scripts/deploy.sh']
    }
}

closure_job = {
    'closure_job': {
        'extends': ['.deployment_base'],
        'stage': 'closure',
        'script': ['cat scripts/pipeline.yml', 'exit 0']
    }
}

site_map = [
    ('site_1', 'us-east-1', 'site_1_env'),
    ('site_2', 'us-east-2', 'site_2_env'),
    ('site_3', 'europe-west-2', 'site_3_env')
]


def normalise_name(name: str) -> str:
    return name.replace('_', '-') if name else name


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generates pipeline configuration in YAML format')
    parser.add_argument('-o', '--out', help='filename of output yml', required=True)

    args = vars(parser.parse_args())
    print(args)
    deployments = dict()
    pipeline = YAML()
    pipeline.add('variables_section', copy.deepcopy(variables))
    pipeline.add('stages_section', copy.deepcopy(stages))
    pipeline.add('base_image_section', copy.deepcopy(base_image))
    pipeline.add('deployment_base_section', copy.deepcopy(deployment_base))
    pipeline.add('closure_job_section', copy.deepcopy(closure_job))
    print(pipeline.sections_map)

    for site_name, location, env in site_map:
        stage_name = 'deploy-' + normalise_name(site_name)
        deployment_vars_section_name = '.deployment_vars_' + site_name
        deployment_section_name = 'deployment_' + site_name

        pipeline.get('stages_section').get('stages').append(stage_name)
        deployment_vars_copy = copy.deepcopy(deployment_vars)
        deployment_vars_copy['.deployment_vars']['stage'] = stage_name
        deployment_vars_copy['.deployment_vars']['variables']['LOCATION'] = location
        deployment_vars_copy['.deployment_vars']['variables']['ENVIRONMENT'] = env

        deployment_vars_section = dict()
        deployment_vars_section[deployment_vars_section_name] = deployment_vars_copy.get('.deployment_vars')
        pipeline.add(deployment_vars_section_name, deployment_vars_section)

        deployment_copy = copy.deepcopy(deployment)
        deployment_copy['deployment']['extends'].append(deployment_vars_section_name)

        deployment_section = dict()
        deployment_section[deployment_section_name] = deployment_copy.get('deployment')
        pipeline.add(deployment_section_name, deployment_section)

    pipe = pipeline.to_string()
    print(pipe)
    with open(args.get('out'), 'w+') as f:
        f.write(pipe)
