import re
import yaml


def convert_function_to_yaml(function_line, named_arguments):
  match = re.match(r'Function (\w+)\((.*)\)', function_line)
  if not match:
    return None

  func_name = match.group(1)
  args_str = match.group(2)

  args = []
  for arg in args_str.split(','):
    arg = arg.strip()

    if len(arg.split()) > 2:
      print(arg.split())

    if len(arg.split()) > 1:
      arg_type, arg_name = arg.split()[0:2]
      arg_type = arg_type.replace('ai', '').replace('ak',
                                                    '').replace('[]',
                                                                '').lower()
      args.append({
          'name':
          f'--{arg_name}' if named_arguments else arg_name,
          'type':
          f'-{arg_type}' if named_arguments else arg_type,
          'help':
          f'the {arg_type} to be used',
          'required':
          len(arg.split()) < 2,
          'selected':
          arg_type in ['actor', 'objectreference', 'weapon']
          and not (any(argument['selected'] for argument in args))
      })

  words = re.findall(r'[A-Z][a-z]*|[a-z]+', func_name)
  alias = ''.join([word[0] for word in words]).lower()

  yaml_structure = {
      'name': re.sub(r'([A-Z])', '-\\1', func_name).lower().strip('-'),
      'alias': alias,
      'func': func_name,
      'help': f'{func_name.lower().replace("-", " ")} the provided arguments',
      'args': args
  }

  return yaml_structure


def convert_psc_to_yaml(psc_file, yaml_file, yaml_data, named_arguments):
  with open(psc_file, 'r') as file:
    lines = file.readlines()

  subs = yaml_data['subs']
  for line in lines:
    line = line.strip()
    if line.startswith('Function') and any(
        line.startswith(f'Function {prefix}')
        for prefix in ['Get', 'Set', 'Add', 'Remove', 'Create']):
      yaml_structure = convert_function_to_yaml(line, named_arguments)
      if yaml_structure:
        subs.append(yaml_structure)

  with open(yaml_file, 'w') as file:
    yaml.dump(yaml_data, file, sort_keys=False)

# ---
# Customize this area
# ---
yaml_data = {
    'name': 'quest-utils',
    'alias': 'qu',
    'script': 'Quest',
    'help': 'utilities from Quest',
    'subs': []
}

convert_psc_to_yaml(
    'Quest.psc',
    'questutils.yaml',
    yaml_data, False)
