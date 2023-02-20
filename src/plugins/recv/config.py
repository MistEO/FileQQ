import yaml

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

print("config:", config)


avatar_enabled = config['recv']['avatar']
image_enabled = config['recv']['image']
