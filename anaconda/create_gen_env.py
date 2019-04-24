"""
Sharing anaconda environments via .yml files (such as the output of
`conda env export > environment.yml`) can be tricky since exact build numbers
depend on platform. Often even trivial environments cannot be shared since
anaconda tailors python package builds, as much as possible, to each user's
platform. Thus, for example, an environment.yml file created from a Windows 7
machine is often unusable as-is on a Linux machine.

This script solves this problem by stripping out the unnecessary platform specs.
All other important information, such as exact package versions, are retained so
that functionally-identical environments may be easily installed on multiple
machines and platforms by sharing the `gen_environment.yml` file.

Currently key order is not preserved by yaml (see
https://github.com/yaml/pyyaml/issues/110). This does not affect creating a
conda environment from the file created by this script.
"""
import yaml

win_only = [
    'pyreadline', 'vc', 'vs2008_runtime', 'vs2010_runtime', 'vs2013_runtime',
    'vs2015_runtime', 'wincertstore'
]

with open('environment.yml', 'r', encoding='utf-8') as f:
    old_env = yaml.load(f, Loader=yaml.BaseLoader)

new_env = old_env
new_env['dependencies'] = [
    '='.join(dep.split('=')[0:2]) for dep in old_env['dependencies']
    if dep.split('=')[0] not in win_only
]

with open('generic_environment.yml', 'w+', encoding='utf-8') as out:
    yaml.dump(new_env, out, default_flow_style=False, explicit_start=False)
