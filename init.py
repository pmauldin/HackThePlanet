# -*- coding: utf-8 -*-

import jinja2
import os

config_prompts = {
    'dev_uri': {
        'message': u'What URL will your development environment use?',
        'default': u'http://localhost:5000'
    },
    'prod_uri': {
        'message': u'What URL will your production environment use?',
        'default': u''
    },
    'key': {
        'message': u'key',
        'default': u''
    },
    'password': {
        'message': u'password',
        'default': u''
    }
}


def generate_config():
    """
    Creates config.py
    """
    with open('templates/config.py', 'r') as f:
        template = jinja2.Template(unicode(f.read()))

    config = {
        'dev_token': os.urandom(24).encode('hex'),
        'prod_token': os.urandom(24).encode('hex')
    }

    for field, prompt in config_prompts.iteritems():
        if prompt.get('default'):
            result = raw_input(u'{0} ({1}) '.format(
                prompt['message'], prompt['default']))
        else:
            result = raw_input(u'{0} '.format(prompt['message']))
        if not result:
            result = prompt.get('default', u'')
        config[field] = result

    with open('config.py', 'w') as f:
        print config
        f.write(template.render(**config))

    print "Created config.py"


def generate_manifest():
    """
    Creates manifest.xml
    """
    from config import manifest

    with open('templates/manifest.xml', 'r') as f:
        template = jinja2.Template(unicode(f.read()))

    with open('manifest.xml', 'w') as f:
        f.write(template.render(**manifest))

    print "Created manifest.xml"

if __name__ == '__main__':
    generate_config()
    generate_manifest()
