Make a package without a service blog

```
packages$ ncs-make-package --help
Usage: ncs-make-package [options] package-name

  ncs-make-package --netconf-ned DIR package-name
  ncs-make-package --snmp-ned DIR package-name
  ncs-make-package --data-provider-skeleton package-name
  ncs-make-package --generic-ned-skeleton package-name
  ncs-make-package --erlang-skeleton package-name
  ncs-make-package --service-skeleton TYPE package-name

      where TYPE is one of:
          java                  Java based service
          java-and-template     Java service with template
          python                Python based service
          python-and-template   Python service with template
          template              Template service (no code)

  ADDITIONAL OPTIONS
  --dest DIR
  --build
  --verbose
  -h | --help

  SERVICE specific options:
    --augment PATH
    --root-container NAME

  JAVA specific options:
    --java-package NAME

  NED specific options:
    --no-java
    --no-netsim
    --no-python
    --vendor STRING
    --package-version STRING

  NETCONF NED specific options:
    --ncs-depend-package DIR
    --pyang-sanitize
    --confd-netsim-db-mode candidate | startup | running-only

  PYTHON specific options:
    --component-class NAME (default main.Main)
    --action-example
    --subscriber-example

  ERLANG specific options:
    --erlang-application-name NAME (uses package name as default)

  LSA PACKAGES

  ncs-make-package --lsa PATH base-name
  ncs-make-package --lsa-upper PATH base-name
  ncs-make-package --lsa-lower PATH TYPE base-name

    Where PATH is the path of a YANG file.

    For LSA packages the resulting name of the package will be:
      --lsa:       <base-name>
      --lsa-upper: lsa-upper-<base-name>
      --lsa-lower: lsa-lower-<base-name>

    For LSA packages the name used in the YANG data model will be:
      --lsa:        <base-name>
      --lsa-upper:  lsa-<base-name>
      --lsa-lower:  lsa-<base-name>


See manpage for ncs-make-package(1) for more info.
packages$ ncs-make-package --service-skeleton python --action-example ntc-action-example
```


default yang from `ncs-make-package --service-skeleton python --action-example ntc-action-example`


```
module ntc-action-example {

  namespace "http://example.com/ntc-action-example";
  prefix ntc-action-example;

  import ietf-inet-types {
    prefix inet;
  }
  import tailf-common {
    prefix tailf;
  }
  import tailf-ncs {
    prefix ncs;
  }

  description
    "Bla bla...";

  revision 2016-01-01 {
    description
      "Initial revision.";
  }

  container action {
    tailf:action double {
      tailf:actionpoint ntc-action-example-action;
      input {
        leaf number {
          type uint8;
        }
      }
      output {
        leaf result {
          type uint16;
        }
      }
    }
  }
  list ntc-action-example {
    description "This is an RFS skeleton service";

    key name;
    leaf name {
      tailf:info "Unique service id";
      tailf:cli-allow-range;
      type string;
    }

    uses ncs:service-data;
    ncs:servicepoint ntc-action-example-servicepoint;

    // may replace this with other ways of refering to the devices.
    leaf-list device {
      type leafref {
        path "/ncs:devices/ncs:device/ncs:name";
      }
    }

    // replace with your own stuff here
    leaf dummy {
      type inet:ipv4-address;
    }
  }
}

```


default python from make package
```python
# -*- mode: python; python-indent: 4 -*-
import ncs
from ncs.application import Service
from ncs.dp import Action


# ---------------
# ACTIONS EXAMPLE
# ---------------
class DoubleAction(Action):
    @Action.action
    def cb_action(self, uinfo, name, kp, input, output, trans):
        self.log.info('action name: ', name)
        self.log.info('action input.number: ', input.number)

        # Updating the output data structure will result in a response
        # being returned to the caller.
        output.result = input.number * 2


# ------------------------
# SERVICE CALLBACK EXAMPLE
# ------------------------
class ServiceCallbacks(Service):

    # The create() callback is invoked inside NCS FASTMAP and
    # must always exist.
    @Service.create
    def cb_create(self, tctx, root, service, proplist):
        self.log.info('Service create(service=', service._path, ')')


    # The pre_modification() and post_modification() callbacks are optional,
    # and are invoked outside FASTMAP. pre_modification() is invoked before
    # create, update, or delete of the service, as indicated by the enum
    # ncs_service_operation op parameter. Conversely
    # post_modification() is invoked after create, update, or delete
    # of the service. These functions can be useful e.g. for
    # allocations that should be stored and existing also when the
    # service instance is removed.

    # @Service.pre_lock_create
    # def cb_pre_lock_create(self, tctx, root, service, proplist):
    #     self.log.info('Service plcreate(service=', service._path, ')')

    # @Service.pre_modification
    # def cb_pre_modification(self, tctx, op, kp, root, proplist):
    #     self.log.info('Service premod(service=', kp, ')')

    # @Service.post_modification
    # def cb_post_modification(self, tctx, op, kp, root, proplist):
    #     self.log.info('Service premod(service=', kp, ')')


# ---------------------------------------------
# COMPONENT THREAD THAT WILL BE STARTED BY NCS.
# ---------------------------------------------
class Main(ncs.application.Application):
    def setup(self):
        # The application class sets up logging for us. It is accessible
        # through 'self.log' and is a ncs.log.Log instance.
        self.log.info('Main RUNNING')

        # Service callbacks require a registration for a 'service point',
        # as specified in the corresponding data model.
        #
        self.register_service('ntc-action-example-servicepoint', ServiceCallbacks)

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

```

stripped down python file without service components
```
# -*- mode: python; python-indent: 4 -*-
import ncs
from ncs.dp import Action


# ---------------
# ACTIONS EXAMPLE
# ---------------
class DoubleAction(Action):
    @Action.action
    def cb_action(self, uinfo, name, kp, input, output, trans):
        self.log.info('action name: ', name)
        self.log.info('action input.number: ', input.number)

        # Updating the output data structure will result in a response
        # being returned to the caller.
        output.result = input.number * 2


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

```

stripped down yang file without service components 
```
module ntc-action-example {

  namespace "http://networktocode.com/ntc-action-example";
  prefix ntc-action-example;

  import tailf-common {
    prefix tailf;
  }
  import tailf-ncs {
    prefix ncs;
  }

  description
    "An action example";

  revision 2019-09-12 {
    description
      "Giving some details for an action example.";
  }

  container action {
    tailf:action double {
      tailf:actionpoint ntc-action-example-action;
      input {
        leaf number {
          type uint8;
        }
      }
      output {
        leaf result {
          type uint16;
        }
      }
    }
  }
}
```


```
packages$ cd ntc-action-example/
ntc-action-example$ cd src
src$ ls
Makefile	yang
src$ make
mkdir -p ../load-dir
mkdir -p java/src
/Users/jabelk/ncs-all/nso-5-install/bin/ncsc  `ls ntc-action-example-ann.yang  > /dev/null 2>&1 && echo "-a ntc-action-example-ann.yang"` \
              -c -o ../load-dir/ntc-action-example.fxs yang/ntc-action-example.yang
packages$ ncs_cli -C -u admin

admin connected from 127.0.0.1 using console on ntc-jasonbelk-macbook-pro.local
admin@ncs# packages reload force

>>> System upgrade is starting.
>>> Sessions in configure mode must exit to operational mode.
>>> No configuration changes can be performed until upgrade has completed.
>>> System upgrade has completed successfully.
reload-result {
    package ntc-action-example
    result true
}
admin@ncs# conf
Entering configuration mode terminal
admin@ncs(config)# action double ?
Possible completions:
  number  <cr>
admin@ncs(config)# action double number 22
result 44
admin@ncs(config)# action double QQ
---------------------------------^
syntax error: expecting
  number -
admin@ncs(config)# 
```


working oiutput
```
admin@ncs# packages reload
reload-result {
    package ntc-action-example
    result true
}
admin@ncs# conf
Entering configuration mode terminal
admin@ncs(config)# action random-norris-joke number-of-jokes 2
result {u'type': u'success', u'value': [{u'joke': u'Chuck Norris can overflow your stack just by looking at it.', u'id': 473, u'categories': [u'nerdy']}, {u'joke': u"Chuck Norris doesn't have disk latency because the hard drive knows to hurry the hell up.", u'id': 450, u'categories': [u'nerdy']}]}
admin@ncs(config)# end
admin@ncs# exit
src$ kickoffnso

admin connected from 127.0.0.1 using console on ntc-jasonbelk-macbook-pro.local
admin@ncs#
admin@ncs# exit
src$ kickoffnso

admin connected from 127.0.0.1 using console on ntc-jasonbelk-macbook-pro.local
admin@ncs# packages reload
reload-result {
    package ntc-action-example
    result true
}
admin@ncs# conf
Entering configuration mode terminal
admin@ncs(config)# action random-norris-joke number-of-jokes 2
result When Chuck Norris was denied an Egg McMuffin at McDonald's because it was 10:35, he roundhouse kicked the store so hard it became a Wendy's.
admin@ncs(config)# exit
admin@ncs# packages reload
reload-result {
    package ntc-action-example
    result true
}
admin@ncs# conf
Entering configuration mode terminal
admin@ncs(config)# action random-norris-joke number-of-jokes 2
Error: Python cb_action error. local variable 'joke_response' referenced before assignment
admin@ncs(config)# exit
admin@ncs# packages reload
reload-result {
    package ntc-action-example
    result true
}
admin@ncs# conf
Entering configuration mode terminal
admin@ncs(config)# action random-norris-joke number-of-jokes 2
result {u'type': u'success', u'value': [{u'joke': u'Chuck Norris can lead a horse to water AND make it drink.', u'id': 203, u'categories': []}, {u'joke': u"When God said, &quot;let there be light&quot;, Chuck Norris said, &quot;say 'please'.&quot;", u'id': 227, u'categories': []}]}
admin@ncs(config)# exit
admin@ncs# packages reload
reload-result {
    package ntc-action-example
    result true
}
admin@ncs# conf
Entering configuration mode terminal
admin@ncs(config)# action random-norris-joke number-of-jokes 2
result Chuck Norris once rode a bull, and nine months later it had a calf.

Chuck Norris does not need to type-cast. The Chuck-Norris Compiler (CNC) sees through things. All way down. Always.


admin@ncs(config)# exit
admin@ncs# packages reload
reload-result {
    package ntc-action-example
    result true
}
admin@ncs# conf
Entering configuration mode terminal
admin@ncs(config)# action random-norris-joke number-of-jokes 2
result

Chuck Norris has banned rainbows from the state of North Dakota.

When you play Monopoly with Chuck Norris, you do not pass go, and you do not collect two hundred dollars. You will be lucky if you make it out alive.


admin@ncs(config)# action random-norris-joke number-of-jokes 6
result

Chuck Norris once roundhouse kicked someone so hard that his foot broke the speed of light, went back in time, and killed Amelia Earhart while she was flying over the Pacific Ocean.

Chuck Norris doesnt shave; he kicks himself in the face. The only thing that can cut Chuck Norris is Chuck Norris.

Chuck Norris is the only man to ever defeat a brick wall in a game of tennis.

Chuck Norris doesn't throw up if he drinks too much. Chuck Norris throws down!

Newton's Third Law is wrong: Although it states that for each action, there is an equal and opposite reaction, there is no force equal in reaction to a Chuck Norris roundhouse kick.

Chuck Norris causes the Windows Blue Screen of Death.


admin@ncs(config)#
```