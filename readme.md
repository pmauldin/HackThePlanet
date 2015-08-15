# Flask-Azure

A `ResourceProvider` template for integrating with the Azure app store. Based on [Azure's example](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/samples/python-flask).

N.B.:

> I built this on a Mac, so if you're developing on Windows, things may break. If it does break, and you fix it, please make a Pull Request with your fix so we can continue our ceaseless march to victory against bug-kind.

## Install

Get the repo, install dependencies, and proceed to dance:

    git clone git@github.com:garbados/flask-azure.git
    cd flask-azure
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
    make init
    # answer questions about your app
    echo "now it is time to dance" | say

## Usage

This project is a skeleton, a mere shell of the glorious app you will require. To realize its full potential, you must embark on an epic quest into The Source Code.

### tl;dr

Run `make todo` to list everything that isn't yet implemented. Once you've implemented everything, try the test suite to verify you won the game.

### Tests

To make sure your implementation is up to spec, start your development server with `make dev`. Then, with it still running, do `make test`. If anything fails, pray to the gods of your ancestors three times, then fix it!

## API

TODO

### Models

TODO

### Controllers

TODO

### Routes

TODO

## Contributing

To help out, do this:

* Make an issue on GitHub about something that bothers you. Preferably, that something relates to this project.
* Make a Pull Request fixing something that bothered you about this project.

To find things I was too lazy to do yet, clone the repo and run `make lazy`, then do some of those things. If you do, then if I ever meet you in person, I will buy you a food and render you a firm handshake.