import logging
from omegaconf import OmegaConf
from utils.logger import set_logger
from utils.connectivity import checkAWSaccess
from utils.setup import setSageIAMrole, setSageDomain


set_logger(20)
logger = logging.getLogger(__name__)


def setup(config):
    checkAWSaccess()

    setup_config = {}
    iam_response = setSageIAMrole(config.iam)
    setup_config['iam_role'] = iam_response

    if config.main.need_domain:
        domain_response = setSageDomain(
            config.domain, role_arn=iam_response.get('Arn'))
        setup_config['sage_domain'] = domain_response

    OmegaConf.save(
        OmegaConf.create(setup_config), config.main.out_settings_path)


if __name__ == "__main__":
    config = OmegaConf.load('configs/sage/sage_setup.yaml')
    setup(config)