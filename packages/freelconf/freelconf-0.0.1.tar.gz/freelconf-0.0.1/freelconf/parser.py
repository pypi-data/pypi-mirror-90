from freelconf.utils import FileManager
import yaml
import json
import copy

class ConfParser():

    @classmethod
    def compile(cls, stack_files, output_file, account_file="accounts.yaml"):
        accounts = yaml.safe_load(FileManager.read(account_file))
        configs = []

        for stack_file in stack_files:
            stack_list = yaml.safe_load(FileManager.read(stack_file))

            for stack in stack_list:
                if not DefValidation.valid(stack, accounts):
                    raise ValueError(f"Stack {json.dumps(stack)} not valid.")
                template = cls._get_template()
                template['template'] = cls._format_stack_template(stack)
                template["location"] = stack['location']
                template['action'] = stack['action']
                template['test'] = stack['test'] if 'test' in stack else ''
                if 'notify' in stack:
                    template['notify'] = stack['notify']

                configs += cls._add_account_details(template, stack, accounts)

        with open(output_file, "w+") as f:
            yaml.dump(configs, f)


    @classmethod
    def _get_template(cls):
        return {
            "location": None,
            "template": {},
            "functions": [],
            "action": None,
        }

    @classmethod
    def _format_stack_template(cls, stack):
        out = {
            'name': stack['name'],
            'parameters': stack['parameters']
        }
        for key, val in stack.get('variables', {}).items():
            out['template'][key] = val
        return out

    @classmethod
    def _add_account_details(cls, template, stack, accounts):
        out = []
        for env in stack['environments']:
            temp = copy.deepcopy(template)
            if env not in accounts:
                env = "_default"
            temp[accounts[env]['Cloud']['Name']] = {
                'account-id': str(accounts[env]['Cloud'].get('AccountId', None)),
                'region': accounts[env]['Cloud'].get('Region', None),
                'deployment-role': accounts[env]['Cloud'].get('DeploymentRole', None),
                'project-id': accounts[env]['Cloud'].get('ProjectId', None),
                'zone': accounts[env]['Cloud'].get('Zone', None),
            }
            out.append(temp)
        return out

class DefValidation():

    REQUIREMENTS = ['name', 'environments', 'location', 'action', 'parameters']
    STACK_ACTION = ['UPDATE_STACK', 'CREATE_OR_UPDATE_STACK', 'CREATE_STACK', 'DELETE_STACK']
    FUNCTION_REQUIREMENTS = ['name', 'location', 'template-attribute', 'bucket']

    @classmethod
    def valid(cls, definition, accounts):
        return (
            cls._meet_requirements(definition)
            and cls._available_environments(definition, accounts)
            and cls._template_exists(definition)
            and cls._available_action(definition)
            and cls._validate_functions(definition)
        )

    @classmethod
    def _meet_requirements(cls, definition):
        if len(cls.REQUIREMENTS) != len(list(set([x for x in definition if x in cls.REQUIREMENTS]))):
            print(f"[ERROR] Missing keys among: {', '.join([x for x in cls.REQUIREMENTS if x not in definition])}")
            return False
        return True

    @classmethod
    def _available_environments(cls, definition, accounts):
        for env in definition['environments']:
            if env not in accounts and '_default' not in accounts:
                print(f"[ERROR] ({definition['name']}) Invalid environment {env}")
                return False
        return True

    @classmethod
    def _template_exists(cls, definition):
        if not FileManager.local_path(definition['location']):
            print(f"[ERROR] ({definition['name']}) Missing template: {definition['location']}")
            return False
        return True

    @classmethod
    def _available_action(cls, definition):
        if definition['action'].upper() not in cls.STACK_ACTION:
            print(f"[ERROR] ({definition['name']}) Invalid action {definition['action']}. Must be among {', '.join(cls.STACK_ACTION)}")
            return False
        return True

    @classmethod
    def _validate_functions(cls, definition):
        if 'functions' in definition:
            valid = True
            for funct in definition['functions']:
                valid &= cls._validate_function(funct)
            return valid
        return True

    @classmethod
    def _validate_function(cls, definition):
        if len(cls.FUNCTION_REQUIREMENTS) != len(list(set([x for x in definition if x in cls.FUNCTION_REQUIREMENTS]))):
            print(f"[ERROR] ({definition['name']}) Missing keys among: {', '.join([x for x in definition])}")
            return False
        if 'variables' not in definition:
            print(f"[ERROR] ({definition['name']}) Need variables if you use functions")
        if definition['template-attribute'] not in definition['variables']:
            print(f"[ERROR] ({definition['name']}) Missing template attribute in variables.")
            return False
        if not FileManager.local_path(definition['location']):
            print(f"[ERROR] ({definition['name']}) Lambda package not found.")
            return False
        return True

