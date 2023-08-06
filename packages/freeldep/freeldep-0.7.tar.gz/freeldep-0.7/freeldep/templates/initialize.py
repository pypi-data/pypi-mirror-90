
try:
    import importlib.resources as pkg_resources
except ImportError:
    # PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

from templates import aws
from templates import gcp



class InitializeDeployerTemplate:
    """Initialize a deployer with an artifact bucket and a registry table"""

    @classmethod
    def name(cls, deployer):
        return f"{deployer['name']}-deployer-initialization-stack"

    @classmethod
    def get(cls, cloud, deployer, config):
        if cloud == "AWS":
            return cls.aws(deployer, config)
        elif cloud == "GCP":
            return cls.gcp(deployer, config)
        raise NotImplementedError("Unknown cloud")

    @classmethod
    def aws(cls, deployer, config):
        return [
            {
                "aws": {
                    "region": config.get("aws", "region", None),
                    "account-id": config.get("aws", "account", None),
                    "deployment-role": config.get("aws", "deployment_role", ""),
                },
                #"location": "./templates/aws/deployer-initialize.yaml",
                "location": pkg_resources.open_text(aws, 'deployer-initialize.yaml'),
                "template": {
                    "name": cls.name(deployer),
                    "parameters": {
                        "artifact-bucket": deployer["artifact"],
                        "registry-table": deployer["registry"],
                    },
                },
                "functions": [],
            }
        ]

    @classmethod
    def gcp(cls, deployer, config):
        return [
            {
                "gcp": {
                    "zone": config.get("gcp", "zone", None),
                    "account-id": config.get("gcp", "account", None),
                    "project": config.get("gcp", "project", ""),
                },
                #"location": "./templates/gcp/deployer-initialize.yaml",
                "location": pkg_resources.open_text(gcp, 'deployer-initialize.yaml'),
                "template": {
                    "name": cls.name(deployer),
                    "parameters": {
                        "artifact-bucket": deployer["artifact"],
                        "bucket-location": config.get("gcp", "zone", None),
                    },
                },
                "functions": [],
                "commands": [],
            }
        ]
