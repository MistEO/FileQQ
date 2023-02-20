import yaml

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

print("config:", config)

recv_avatar_enabled = config['recv']['avatar']
recv_image_enabled = config['recv']['image']
debug_mode = config['debug']