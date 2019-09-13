# -*- mode: python; python-indent: 4 -*-
import ncs
from ncs.dp import Action
import requests


# ---------------
# ACTIONS EXAMPLE
# ---------------
class DoubleAction(Action):
    @Action.action
    def cb_action(self, uinfo, name, kp, input, output, trans):
        self.log.info('action name: ', name)
        self.log.info('action input.number: ', input.number_of_jokes)
        url = "http://api.icndb.com/jokes/random/"+str(input.number_of_jokes)
        resp = requests.get(url)
        data = resp.json()
        jokes = data["value"]
        joke_response = "\n\n"
        for joke in jokes:
            joke_response = joke_response + joke["joke"]
            joke_response = joke_response + "\n\n"
        output.result = joke_response


# ---------------------------------------------
# COMPONENT THREAD THAT WILL BE STARTED BY NCS.
# ---------------------------------------------
class Main(ncs.application.Application):
    def setup(self):
        # The application class sets up logging for us. It is accessible
        # through 'self.log' and is a ncs.log.Log instance.
        self.log.info('Main RUNNING')

        # When using actions, this is how we register them:
        #
        self.register_action('ntc-action-example-action', DoubleAction)

        # If we registered any callback(s) above, the Application class
        # took care of creating a daemon (related to the service/action point).

        # When this setup method is finished, all registrations are
        # considered done and the application is 'started'.

    def teardown(self):
        # When the application is finished (which would happen if NCS went
        # down, packages were reloaded or some error occurred) this teardown
        # method will be called.

        self.log.info('Main FINISHED')
