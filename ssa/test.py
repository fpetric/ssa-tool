import yaml

def move_constructor(loader, node):
    value = loader.construct_mapping(node)
    
