import os, re
import yaml

# ---
# Customize this area
# ---
psc_file = '/bla/blabla.psc'
psc_filename = os.path.splitext(os.path.basename(psc_file))[0]
output_name = psc_filename.replace('Script', '').strip('-_ ') + '-utils'
output_file = '/bla/blabla/' + output_name + '.yaml'
# ---
# End customize
# ---

def convert_function_to_yaml(function_line, named_arguments):
  match = re.search(r'[Ff]unction (\w+)\((.*)\)', function_line)
  if not match:
    return None

  func_name = match.group(1)
  args_str = match.group(2)

  args = []
  for arg in args_str.split(','):
    arg = arg.strip()

    if len(arg.split()) > 2:
      print('INFO Argument has default value: ' + arg.split().__str__())

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
      'unc': func_name,
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
    if any('unction ' + prefix in line for prefix in [
        'Get', 'Set', 'Add', 'Remove', 'Create', 'Equip', 'Is', 'Activate',
        'Count', 'Update', 'Improve'
    ]):
      yaml_structure = convert_function_to_yaml(line, named_arguments)
      if yaml_structure:
        subs.append(yaml_structure)
  print(f'Saving {output_file}...')
  with open(yaml_file, 'w') as file:
    yaml.dump(yaml_data, file, sort_keys=False)

yaml_data = {
    'name': output_name,
    'alias': ''.join([word[0] for word in re.findall(r'[A-Z][a-z]*|[a-z]+', output_name)]).lower(),
    'script': psc_filename,
    'help': 'utilities from ' + psc_filename,
    'subs': []
}

convert_psc_to_yaml(psc_file, output_file, yaml_data, False)
