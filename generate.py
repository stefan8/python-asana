import json
import string
import os

GENERATED_WARNING = '# This file is automatically generated by generate.py using api.json\n'

INIT_PY_TEMPLATE = string.Template('''
from . import $resourceNames
''')

RESOURCE_CLASS_TEMPLATE = string.Template('''
from .$moduleNameBase import $classNameBase

class $name($classNameBase):
    pass
''')

RESOURCE_BASE_CLASS_TEMPLATE = string.Template('''
class $name:
    def __init__(self, client=None):
        self.client = client
''')

RESOURCE_METHOD_TEMPLATE = string.Template('''
    def $name(self, params={}):
        return self.client.$method('$url', params$dispatchOptions)
''')

RESOURCE_METHOD_TEMPLATE_WITH_ARGS = string.Template('''
    def $name(self, $args, params={}):
        path = '$url' % ($args)
        return self.client.$method(path, params$dispatchOptions)
''')

RESOURCE_METHOD_TEMPLATE_ITERATOR = string.Template('''
    def ${name}_iterator(self, params={}):
        return self.client.get_iterator('$url', params$dispatchOptions)
''')

RESOURCE_METHOD_TEMPLATE_ITERATOR_WITH_ARGS = string.Template('''
    def ${name}_iterator(self, $args, params={}):
        path = '$url' % ($args)
        return self.client.get_iterator(path, params$dispatchOptions)
''')

api = json.loads(open('api.json', 'r').read())

resourceNames = []
for resourceName, resource in api['resources'].iteritems():
    resourceNames.append(resourceName)

    className = resourceName.capitalize()
    moduleName = resourceName.lower()
    classNameBase = '_' + resourceName.capitalize()
    moduleNameBase = '_' + resourceName.lower()

    resource_base_py = open('asana/resources/' + moduleNameBase + '.py', 'w')
    resource_base_py.write(GENERATED_WARNING)
    resource_base_py.write(RESOURCE_BASE_CLASS_TEMPLATE.substitute(name=classNameBase))
    if 'methods' in resource:
        for methodName, method in resource['methods'].iteritems():
            templateVariables = {
                'name': methodName,
                'method': method['method'],
                'url': method['url'],
                'args': ', '.join(method['args']) if 'args' in method and len(method['args']) > 0 else None,
                'dispatchOptions': ', ' + repr(method['dispatchOptions']) if 'dispatchOptions' in method else ''
            }

            if templateVariables['args'] is None:
                resource_base_py.write(RESOURCE_METHOD_TEMPLATE.substitute(**templateVariables))
            else:
                resource_base_py.write(RESOURCE_METHOD_TEMPLATE_WITH_ARGS.substitute(**templateVariables))

            if method.get('collection', False):
                if method['method'] != 'get':
                    raise Exception('"collection" set to true with "method" other than "get" is not supported')
                if templateVariables['args'] is None:
                    resource_base_py.write(RESOURCE_METHOD_TEMPLATE_ITERATOR.substitute(**templateVariables))
                else:
                    resource_base_py.write(RESOURCE_METHOD_TEMPLATE_ITERATOR_WITH_ARGS.substitute(**templateVariables))

    resource_base_py.close()

    if not os.path.exists('asana/resources/' + moduleName + '.py'):
        resource_py = open('asana/resources/' + moduleName + '.py', 'w')
        resource_py.write(RESOURCE_CLASS_TEMPLATE.substitute(
            name=className,
            classNameBase=classNameBase,
            moduleNameBase=moduleNameBase
        ))
        resource_py.close()

resourceNames.sort()

init_py = open('asana/resources/__init__.py', 'w')
init_py.write(GENERATED_WARNING)
init_py.write(INIT_PY_TEMPLATE.substitute(resourceNames=', '.join(resourceNames)))
init_py.close()
