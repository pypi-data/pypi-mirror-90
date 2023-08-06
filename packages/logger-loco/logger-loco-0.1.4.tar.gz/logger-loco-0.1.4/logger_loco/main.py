import inspect
import re
import uuid
import functools

current_indent = 0

#__DEBUG__=False
__DEBUG__=True

def loco(logger, indent_symbol=' ', indent_size=2):
  rules = {
    '#@': 'debug',
    '##': 'debug',
    '#-': 'info',
    '#!': 'warning',
    '#X': 'error'
  }

  random = str(uuid.uuid4()).replace('-', '_')

  def decorator(something):
    if inspect.isclass(something):
      c = something

      members = inspect.getmembers(c, predicate=inspect.isfunction)

      for name, method in members:
        if not name.startswith('__') and not name.endswith('__'):
          setattr(c, name, decorator(method))

      return c
    else:
      f = something

      lines = inspect.getsource(f)
      new_lines = []

      if __DEBUG__:
        print('Function sources:')
        print(lines)

      injects = {}
      extra_indention_len = 0

      global current_indent

      if __DEBUG__:
        print('Current indent:', current_indent)

      for line in lines.split('\n'):
        if line.strip().startswith('@'):
          current_indent = len(line.split('@')[0])
          if __DEBUG__:
            print('Skil line ("@" found):', line)
          continue
        if 'def ' in line and ':' in line:
          m = re.match('( *)def.+:.*', line)
          extra_indention_len = len(m.group(1))
          if __DEBUG__:
            print('Function found:', line)
        if '-->' in line:
          current_indent += 1
          if __DEBUG__:
            print('Indent incremented', line)
        if '<--' in line:
          current_indent -= 1
          if __DEBUG__:
            print('Indent decremented', line)

        line = line[extra_indention_len:]

        for trigger, method in rules.items():
          m = re.match(f'^(.+){trigger}(.+)$', line)
          if m:
            indent = m.group(1)
            content = m.group(2)

            content = content.replace('\'', '\u2019')
            content = indent_symbol * (current_indent * indent_size) + content

            line = "{}logger_{}.{}(f'{}')".format(indent, random, method, content)

        if __DEBUG__:
            print('Appending line:', line)
        new_lines.append(line)

      new_source = '\n' * f.__code__.co_firstlineno + '\n'.join(new_lines)

      generated = {
        f'logger_{random}': logger,
        **f.__globals__,
        **injects
      }

      if __DEBUG__:
        print('To be compiled:')
        print(new_source)

      code = compile(new_source, f.__code__.co_filename, 'exec')
      exec(code, generated)

      generated_func = generated[f.__name__]

      return generated_func

  return decorator
