from dreamssh import config
from dreamssh.sdk import registry


config.updateConfig()
registry.registerConfig(config)
