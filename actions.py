# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import requests
import json
from rasa_core_sdk import Action

# may be these are for form action slot filing
from rasa_core_sdk import ActionExecutionRejection
from rasa_core_sdk import Tracker
from rasa_core_sdk.events import SlotSet
from rasa_core_sdk.executor import CollectingDispatcher
from rasa_core_sdk.forms import FormAction, REQUESTED_SLOT

logger = logging.getLogger(__name__)

class ActionSetBankSlot(Action):
    def name(self):
        return "testing_it_will_not_work_for_now"
    def run(self , dispatcher , tracker , domain):
        name = tracker.get_slot("name")
        if(name):
            name = " I did it : "
        else:
            name = None
        return [SlotSet('name',name)]