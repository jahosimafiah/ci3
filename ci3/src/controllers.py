import typing

from datetime import datetime as dt
from ci3.src.handlers import DeploymentAssetHandler
from ci3.src.constants import MINIMUM_KEEP_COUNT

GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

def coordinate_asset_cleanup(handler: DeploymentAssetHandler, keep_count: int, dry_run=True):
    print('min', MINIMUM_KEEP_COUNT)
    if keep_count < MINIMUM_KEEP_COUNT:
        raise ValueError('deploy_count argument must be greater than 0')
    hashes = list(handler.deploy_hashes)
    # Sort the file hashes based on Datetime where they are sorted with newest first
    hashes.sort(key=lambda x: x[1], reverse=True)
    # If dry_run is specified then return the results from coordinate_plan_assets call
    if dry_run:
        return produce_plan_output(hashes, keep_count)
    for deploy, _ in hashes[keep_count:]:
        print('deleting deploy', deploy)
        handler.delete_deploy_files(deploy_hash=deploy)

def produce_plan_output(deployments_with_dt: typing.List[typing.Any], deploy_count: int):
    for idx, deploy_with_dt in enumerate(deployments_with_dt):
        prefix = f'{GREEN}[KEEP] {RESET}'
        if idx + 1 > deploy_count:
            prefix = f'-{RED}[DELETE] {RESET}'
        yield f'{prefix} {deploy_with_dt[0]} {deploy_with_dt[1]}'
