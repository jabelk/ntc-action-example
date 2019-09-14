# -*- mode: python; python-indent: 4 -*-
import ncs
from ncs.dp import Action
import requests
class NorrisAction(Action):
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
class Main(ncs.application.Application):
    def setup(self):
        self.log.info('Main RUNNING')
        self.register_action('ntc-action-example-action', NorrisAction)
    def teardown(self):
        self.log.info('Main FINISHED')
