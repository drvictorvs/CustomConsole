import re
import yaml


def convert_function_to_yaml(function_line):
  match = re.match(r'Function (\w+)\((.*)\) global native', function_line)
  if not match:
    return None

  func_name = match.group(1)
  args_str = match.group(2)

  args = []
  for arg in args_str.split(','):
    arg = arg.strip()

    if len(arg.split()) > 1:
      arg_type, arg_name = arg.split()[0:2]
      args.append({
          'name':
          arg_name,
          'type':
          arg_type.replace('ai', '').replace('ak', '').replace('[]',
                                                               '').lower(),
          'help':
          f'the {arg_name} to be used'
      })

  words = re.findall(r'[A-Z][a-z]*|[a-z]+', func_name)
  alias = ''.join([word[0]
                    for word in words]).lower()

  yaml_structure = {
      'name': re.sub(r'([A-Z])', '-\\1', func_name).lower().strip('-'),
      'alias': alias,
      'func': func_name,
      'help': f'{func_name.lower().replace("-", " ")} the provided arguments',
      'args': args
  }

  return yaml_structure

def convert_psc_to_yaml(psc_file, yaml_file):
  with open(psc_file, 'r') as file:
    lines = file.readlines()

  yaml_data = {
    'name': 'form-utils',
    'alias': 'futil',
    'script': 'PO3_SKSEFunctions',
    'help': 'utilities for reading and manipulating forms',
    'subs': []
    }
  subs = yaml_data['subs']
  for line in lines:
    line = line.strip()
    if line.startswith('Function') and any(
        line.startswith(f'Function {prefix}')
        for prefix in ['Get', 'Set', 'Add', 'Remove', 'Create']):
      yaml_structure = convert_function_to_yaml(line)
      if yaml_structure:
        subs.append(yaml_structure)

  with open(yaml_file, 'w') as file:
    yaml.dump(yaml_data, file, sort_keys = False)

convert_psc_to_yaml(
    '',
    ''
)
