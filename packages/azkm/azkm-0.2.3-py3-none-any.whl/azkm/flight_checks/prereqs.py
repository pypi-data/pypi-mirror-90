import shutil
from tabulate import tabulate
from azkm.utils import osutil
import os
import json

prereq_cmd = [
    'terraform',
    'kubectl'
]

cdktf_cfg = {
    "language": "python",
    "app": "python ./__main__.py",
    "terraformProviders": ["azurerm@~> 2.40.0"],
    "codeMakerOutput": "providers"
}

def check_cmd():
    prereq_paths = []
    for cmd in prereq_cmd:
        cmd_path = shutil.which(cmd)
        assert cmd_path is not None, 'Please install {0}'.format(cmd)
        prereq_paths = prereq_paths + [(cmd, cmd_path)]
    return prereq_paths

def confirm_cmd():
    prereqs = check_cmd()
    print('Pre-requisites:')
    print(tabulate(prereqs, headers=['cmd', 'path']))
    print('\r\n')

def get_providers():
    if not os.path.isdir('{0}/azkm/providers/azurerm'.format(osutil.ROOT_DIR)):
        assert shutil.which('cdktf') is not None,  'Please install cdktf: npm i cdktf-cli'
        osutil.chdir('azkm')
        with open('cdktf.json', 'w') as cfg:
            cfg.write(json.dumps(cdktf_cfg))
        osutil.run_subprocess(['cdktf', 'get'])

def install():
    check_cmd()
    get_providers()