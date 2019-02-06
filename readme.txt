command to train NLU
    make train-mms-nlu
command to train core
    make train-mms-core
Run rasa core server
    make run-core
Run action server to invoke action.py
    make action-server
Run this for running core with debugging mode in console
    make run-core-debug
Run this for running in interactive mode to know flow of code
    make run-interactive
TO Run all 3 commands at a time i.e train nlu , train core and run core 
    make run-all-3-commands

You can view all commands in Makefile

To install Dependencies 
    pip install -r requirements.txt

Process to Add new Utter or New Intent : 
 1. Add Intent name and example sentences in data/mms-nlu-data folder by creating a new file or writing in any existing file.
 2. Add Intent name in domain.yml file .
 3. If there are any entities to extract specify them in domain.yml file in slots section
 4. write an action for that Intent in domain.yml either it can be utter_< intent name > or action_< intent name >
 5. if it is utter we can specify a template directly in domain.yml in templates section
 6. if it is an action then we should write a class for that action in actions.py
 7. Then Write a story for that intent + action in mms-stories.md
 8. Done !!

 Rasa NLU and Rasa Core Process :
 1 . Train nlu data to understand user inputs by passing config file and training data files
 2 . Train Core to Process user inputs and predict what to say to user by passing domain.yml , stories and dilog model
 3 . Run Action server to run python script for custom actions
 4 . Run core server to enable rasa core api for making api calls

When bot receives a message from user 
i .  It identifies intent
ii.  Extarct entites and fills slots if there are any.
iii. Go to stories and runs action according to that particular intent
iv.  An Action can be utter_ or custom action
v.   Utter aciton goes to domain.yml template and cusom action goes to python script action.py 

Template for Defining Action in action.py

class ActionIntentName(Action):
    def name(self):
        return "action_intent_name"
    def run(self , dispatcher , tracker , domain ):
        # Process the code here
        # we can do any API calls or utter templates from domain file also
        # dispatcher.utter_message(" Any message you need to give to user  ")