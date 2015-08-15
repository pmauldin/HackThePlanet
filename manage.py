import resourceprovider
import config
import sys

# env defaults
defaults = {
    'development': {
        'debug': True
    }
}


def start_app(env="development"):
    options = config.app[env]
    resourceprovider.create_app(options).run(**defaults.get(env, {}))

if __name__ == "__main__":
    start_app(sys.argv[1])
