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
        return "action_set_bank_slot"
    def run(self , dispatcher , tracker , domain):
        bankname = tracker.get_slot("bankname")
        if(bankname):
            bankname = " I did it : "
        else:
            bankname = None
        return [SlotSet('bankname',bankname)]
class ShowMoreSalaryTransferNegative(Action):
    def name(self):
        return "action_show_more_personal_loans_salary_transfer_negative"
    def run(self , dispatcher , tracker , domain ):
        personalLoanApiData = {
                "category": "Personal Loan",
                "financeAmountSort": None,
                "interestRateSort": None,
                "isSalaryTransfer": None,
                "limit": 10,
                "maxFinanceAmount": None,
                "maxFlatRate": None,
                "maxInterestRate": None,
                "maxReducingRate": None,
                "maxSalary": None,
                "mimimumSalarySort": None,
                "minFinanceAmount": None,
                "minFlatRate": None,
                "minInterestRate": None,
                "minReducingRate": None,
                "minSalary": None,
                "popularity": 1,
                "provider": [],
                "reducingRateSort": None,
                "skip": 0,
                "type": "Loans"
        }
        bankname = tracker.get_slot("bankname")
        print("\n================bankname====================\n")
        print( "{ bankname :  " +  '"' + bankname + '"'   +"  }" )
        print("\n================bankname====================\n")
        if( "Dunia Finance".replace(" ", "").lower() in bankname.replace(" ", "").lower() 
             or 
             bankname.replace(" ", "").lower() == "Dunia Finance".replace(" ", "").lower()
          ):
            bankname = "dunia-finance"
            print("Changed bank name" + bankname)
        
        if(bankname):
            personalLoanApiData["provider"].append(bankname)
        personalLoanApiData["isSalaryTransfer"] = False
        msg = ''
        # url for calling personalloans api in MMS
        url = "http://localhost:3000/api/searach/loans/personalloans"
        # converting into json
        data_json = json.loads(json.dumps(personalLoanApiData))
        # calling api in MMS getting response
        response = requests.post(url, json=data_json)
        res_object = json.loads(response.text)
        # making link tags and appending into msg
        if(res_object["total"] > 0):
            for i in range(5,len(res_object["data"])):
                if not (i<len(res_object["data"])):
                    break
                href = "/personal-loan/" + res_object["data"][i]["productUrl"]
                text = res_object["data"][i]["provider"] + " " + res_object["data"][i]["planName"]
                link = "<a href='" + href + "' target='_blank' > " + text + "</a>" + "<br>"
                msg += link
        else:
            msg = "No data available for your query"
        msg = "More Personal loans with no salary transfer <br>" + msg
        if( len(res_object["data"]) <= 5 ):
            msg = "There is no more Data Available"
        dispatcher.utter_message(msg)
        return []

# this is for personal loans salary transfer is true
class ActionSalaryTransferPositive(Action):
   def name(self):
      return "action_personal_loans_salary_transfer_positive"
   def run(self, dispatcher, tracker, domain):
        personalLoanApiData = {
                "category": "Personal Loan",
                "financeAmountSort": None,
                "interestRateSort": None,
                "isSalaryTransfer": None,
                "limit": 10,
                "maxFinanceAmount": None,
                "maxFlatRate": None,
                "maxInterestRate": None,
                "maxReducingRate": None,
                "maxSalary": None,
                "mimimumSalarySort": None,
                "minFinanceAmount": None,
                "minFlatRate": None,
                "minInterestRate": None,
                "minReducingRate": None,
                "minSalary": None,
                "popularity": 1,
                "provider": [],
                "reducingRateSort": None,
                "skip": 0,
                "type": "Loans"
        }
        personalLoanApiData["isSalaryTransfer"] = True
        call = ActionPersonalLoans.callPersonalLoansApi
        msg = call( None , personalLoanApiData)
        msg = "Top Personal Loans with salary transfer : <br>" + msg
        dispatcher.utter_message(msg)
        return []
# this is for personal loans salary transfer is false
class ActionSalaryTransferNegative(Action):
    def name(self):
        return "action_personal_loans_salary_transfer_negative"
    def run(self, dispatcher, tracker, domain):
        personalLoanApiData = {
                "category": "Personal Loan",
                "financeAmountSort": None,
                "interestRateSort": None,
                "isSalaryTransfer": None,
                "limit": 10,
                "maxFinanceAmount": None,
                "maxFlatRate": None,
                "maxInterestRate": None,
                "maxReducingRate": None,
                "maxSalary": None,
                "mimimumSalarySort": None,
                "minFinanceAmount": None,
                "minFlatRate": None,
                "minInterestRate": None,
                "minReducingRate": None,
                "minSalary": None,
                "popularity": 1,
                "provider": [],
                "reducingRateSort": None,
                "skip": 0,
                "type": "Loans"
        }
        bankname = tracker.get_slot("bankname")
        if(bankname):
            personalLoanApiData["provider"].append(bankname)
        personalLoanApiData["isSalaryTransfer"] = False
        call = ActionPersonalLoans.callPersonalLoansApi
        msg = call( None , personalLoanApiData)
        msg = "Top Personal loans with no salary transfer <br>" + msg
        url = "http://localhost:3000/api/searach/loans/personalloans"
        data_json = json.loads(json.dumps(personalLoanApiData))
        response = requests.post(url, json=data_json)
        res_object = json.loads(response.text)
        # msg = str(len(res_object["data"])) + msg
        dispatcher.utter_message(msg)
        if(res_object["total"] > 0):
            if(len(res_object["data"]) > 5):
                dispatcher.utter_template("utter_show_more_personal_loans_salary_transfer_negative" , tracker)
        return [SlotSet('bankname',bankname)]

# custom action class for form action home loans
class FormActionHomeLoans(FormAction):
    def name(self):
        return "home_loan_form"
    @staticmethod
    def required_slots(tracker):
        return ["bankname"]
    def slot_mappings(self):
        return {"bankname": self.from_entity(entity="bankname",not_intent="greet")}

    def submit(self, dispatcher, tracker, domain):
        
        # extracting bank name
        bankname = tracker.get_slot("bankname")
        if(bankname):
            print("\n========slots===========================\n")
            print( "{ bankname :  " +  '"' + bankname + '"'   +"  }" )
            print("\n=========slots==========================\n")
        homeLoanApiData = {
            "category" : "Home Loan",
            "type" : "Loans",
            "minDownPayment" : None,
            "maxDownPayment" : None,
            "minRepaymentsUpTo" : None,
            "maxRepaymentsUpTo" : None,
            "minFinanceAmount" : None,
            "maxFinanceAmount" : None,
            "minSalary" : None,
            "maxSalary" : None,
            "minFlatRate" : None,
            "maxFlatRate" : None,
            "minReducingRate" : None,
            "maxReducingRate" : None,
            "isSalaryTransfer" : None,
            "minInterestRate" : None,
            "maxInterestRate" : None,
            "isForCompletedProperty" : None,
            "isForUnderConstructionProperty" : None,
            "provider" : [],
            "skip" : 0,
            "limit" : 10,
            "mimimumSalarySort" : None,
            "interestRateSort" : None,
            "financeAmountSort" : None,
            "reducingRateSort" : None
        }
        if not bankname:
            bankname =''
        else :
            # http://localhost:3000/api/searach/loans/homeloans
            homeLoanApiData["provider"].append(bankname)
            temp_text = bankname + " Home loans are following <br>"
        msg = self.callHomeLoanApiData(homeLoanApiData)
        msg = temp_text + msg
        dispatcher.utter_message(msg)
        return []
    def callHomeLoanApiData( self , homeLoanApiData ):
        msg = ''
        # url for calling personalloans api in MMS
        url = "http://localhost:3000/api/searach/loans/homeloans"
        # converting into json
        data_json = json.loads(json.dumps(homeLoanApiData))
        # calling api in MMS getting response
        response = requests.post(url, json=data_json)
        res_object = json.loads(response.text)
        # making link tags and appending into msg
        if(res_object["total"] > 0):
            for i in range(len(res_object["data"])):
                if not (i<5):
                    break
                href = "/home-loan/" + res_object["data"][i]["productUrl"]
                text = res_object["data"][i]["provider"] + " " + res_object["data"][i]["planName"]
                link = "<a href='" + href + "' target='_blank' > " + text + "</a>" + "<br>"
                msg += link  
        else:
            msg = "Sorry , Your query has NO results FOUND HOME_LOANS"
        return msg
# this is form action personal loans
class FormActionPersonalLoans(FormAction):
    def name(self):
        print("\n=== 1 name metohd ===")
        return "personal_loan_form"
    @staticmethod
    def required_slots(tracker):
        print("\n=== 2 required slots method===")
        return ["bankname"]
    def slot_mappings(self):
        print("\n=== 3 slot mappings method ===")
        return {"bankname": self.from_entity(entity="bankname",not_intent="greet")}
    def validate(self, dispatcher, tracker, domain):
        print("\n=== 4 validate method===")
        
        return []
    def submit(self, dispatcher, tracker, domain):
        print("\n=== 5 submmit method===")
        # getting bank name from slot
        call = ActionSetBankSlot.run
        gotIt = call(self, dispatcher, tracker, domain)
        print(gotIt)
        # print(gotIt[0]["value"])
        bankname = tracker.get_slot("bankname")
        bankname = gotIt[0]["value"]
        msg = ''
        print("\n==== bankname ===" + bankname)
        personalLoanApiData = {
                "category": "Personal Loan",
                "financeAmountSort": None,
                "interestRateSort": None,
                "isSalaryTransfer": None,
                "limit": 10,
                "maxFinanceAmount": None,
                "maxFlatRate": None,
                "maxInterestRate": None,
                "maxReducingRate": None,
                "maxSalary": None,
                "mimimumSalarySort": None,
                "minFinanceAmount": None,
                "minFlatRate": None,
                "minInterestRate": None,
                "minReducingRate": None,
                "minSalary": None,
                "popularity": 1,
                "provider": [],
                "reducingRateSort": None,
                "skip": 0,
                "type": "Loans"
        }
        if bankname is None:
            # temporary text template 
            temp_text = "given below are personal loans <br>"
        else :
            # pushing provider 
            personalLoanApiData["provider"].append(bankname)
            temp_text = "given below are "+ bankname +" personal loans <br>"  
        msg = self.callPersonalLoansApi(personalLoanApiData)
        msg = temp_text + msg 
        dispatcher.utter_message(msg) #send the message back to the user
        return []
     #function for calling API and returning message
    def callPersonalLoansApi( self , personalLoanApiData ):
        print("\n=== 6 callPersonalLoansApi method ===")
        msg = ''
        # url for calling personalloans api in MMS
        url = "http://localhost:3000/api/searach/loans/personalloans"
        # converting into json
        data_json = json.loads(json.dumps(personalLoanApiData))
        # calling api in MMS getting response
        response = requests.post(url, json=data_json)
        res_object = json.loads(response.text)
        # making link tags and appending into msg
        if(res_object["total"] > 0):
            for i in range(len(res_object["data"])):
                if not (i<5):
                    break
                href = "/personal-loan/" + res_object["data"][i]["productUrl"]
                text = res_object["data"][i]["provider"] + " " + res_object["data"][i]["planName"]
                link = "<a href='" + href + "' target='_blank' > " + text + "</a>" + "<br>"
                msg += link  
        else:
            msg = " Nothing found for your query"
        return msg

# custom action class for credit cards
class ActionCreditCards(Action):
    def name(self):
        return "action_credit_cards"
    def run(self , dispatcher , tracker , domain ):
        msg = ''
        temp_text = ''
        creditCardApiData = {
            "type" : 'Cards',
            "category" : 'Credit Card',
            "isBalanceTransfer" : None,
            "minFxRate" : None,
            "maxFxRate" : None,
            "minSalary" : None,
            "maxSalary" : None,
            "minAnnualFee" : None,
            "maxAnnualFee" : None,
            "minInterestRate" : None,
            "maxInterestRate" : None,
            "isPrepaid" : None,
            "isForLadies" : None,
            "isCinema" : None,
            "isValet" : None,
            "isShopping" : None,
            "isDining" : None,
            "isGolf" : None,
            "isCashBack" : None,
            "hasAirmiles" : None,
            "provider" : [],
            "skip" : 0,
            "limit" : 5,
            "mimimumSalarySort" : None,
            "interestRateSort" : None,
            "annulFeeSort" : None
        }
        # getting bank name from entity
        bankname = tracker.get_slot("bankname")
        # getting filter from entity
        _filter = tracker.get_slot("filter")
        # getting range from entity
        _range = tracker.get_slot("range")
        # getting amount from entity
        amount = tracker.get_slot("amount")
        # getting cashback_filter from entity
        cashback_filter = tracker.get_slot("cashback_filter")
        # getting more_data from entity
        more_data = tracker.get_slot("more_data")
        
        print( "{ bankname :  " +  '"' + bankname + '"'   +"  }" )
        print( "{ _filter :  " +  '"' + _filter + '"'   +"  }" )
        print( "{ _range :  " +  '"' + _range + '"'   +"  }" )
        print( "{ amount :  " +  '"' + amount + '"'   +"  }" )
        print( "{ cashback_filter :  " +  '"' + cashback_filter + '"'   +"  }" )
        print( "{ more_data :  " +  '"' + more_data + '"'   +"  }" )
        
        if(bankname):
            creditCardApiData["provider"].append(bankname)
            temp_text = bankname + " "
            if( not _filter and not _range and not amount and not cashback_filter and not more_data ):
                temp_text = bankname + " Credit cards <br>"
            if(cashback_filter):
                temp_text = bankname + " Credit cards "
        if not (bankname):
            temp_text = ''
        if(_filter):
            if("fee" in _filter or "annual" in _filter):
                if(amount and "no" in amount):
                    temp_text += "Credit cards with no annual fee <br>"
                    creditCardApiData["minAnnualFee"] = 0
                    creditCardApiData["maxAnnualFee"] = 0
                elif("no" not in amount):
                    if(_range ):
                        temp_text += "Credit cards with annual fee " + _range + " " + amount + " AED <br>"
                        if("less" in _range):
                            creditCardApiData["minAnnualFee"] = 0
                            creditCardApiData["maxAnnualFee"] = amount
                        elif("more" in _range or "greater" in _range):
                            creditCardApiData["minAnnualFee"] = amount
                            creditCardApiData["maxAnnualFee"] = 10000
                    else:
                        temp_text += "Credit cards with annual fee " + amount + " AED <br>"
                        creditCardApiData["minAnnualFee"] = amount
                        creditCardApiData["maxAnnualFee"] = amount
            elif("salary" in _filter):
                if("no" not in amount):
                    if(_range ):
                        temp_text += "Credit cards with salary " + _range + " " + amount + " AED <br>"
                        if("less" in _range):
                            creditCardApiData["minSalary"] = 0
                            creditCardApiData["maxSalary"] = amount
                        elif("more" in _range or "greater" in _range):
                            creditCardApiData["minSalary"] = amount
                            creditCardApiData["maxSalary"] = 30000
                    else:
                        temp_text += "Credit cards with salary " + amount + " AED <br>"
                        creditCardApiData["minSalary"] = amount
                        creditCardApiData["maxSalary"] = amount
        if(cashback_filter):
            creditCardApiData["isCashBack"] = True
            if( len(temp_text) > 0 ):
                temp_text += "and also with cashback <br>"
            else:
                temp_text += "Best cashback credit cards <br>"
        if( len(temp_text) == 0 ):
            temp_text = "Best Credit cards are given below <br>"
            
        msg = self.callCreditCardsApi(creditCardApiData)
        msg = temp_text + msg 
        dispatcher.utter_message(msg)
        return []
    #function for calling API and returning message
    def callCreditCardsApi( self , creditCardApiData ):
        msg = ''
        # url for calling personalloans api in MMS
        url = "http://localhost:3000/api/searach/cards/creditcards"
        # converting into json
        data_json = json.loads(json.dumps(creditCardApiData))
        # calling api in MMS getting response
        response = requests.post(url, json=data_json)
        res_object = json.loads(response.text)
        # making link tags and appending into msg
        if(res_object["total"] > 0):
            for i in range(len(res_object["data"])):
                if not (i<5):
                    break
                href = "/credit-card/" + res_object["data"][i]["productUrl"]
                text = res_object["data"][i]["provider"] + " " + res_object["data"][i]["productName"]
                link = "<a href='" + href + "' target='_blank' > " + text + "</a>" + "<br>"
                msg += link  
        else:
            msg = "Sorry , Your query has NO results FOUND"
        return msg

# custom action class for personal loans
class ActionPersonalLoans(Action):
    # function for defining action
    def name(self):
        return "action_personal_loans"
    # function for custom action message  generation
    def run(self , dispatcher , tracker , domain ):
        # getting bank name from slot
        bankname = tracker.get_slot("bankname")
        msg = ''
        personalLoanApiData = {
                "category": "Personal Loan",
                "financeAmountSort": None,
                "interestRateSort": None,
                "isSalaryTransfer": None,
                "limit": None,
                "maxFinanceAmount": None,
                "maxFlatRate": None,
                "maxInterestRate": None,
                "maxReducingRate": None,
                "maxSalary": None,
                "mimimumSalarySort": None,
                "minFinanceAmount": None,
                "minFlatRate": None,
                "minInterestRate": None,
                "minReducingRate": None,
                "minSalary": None,
                "popularity": 1,
                "provider": [],
                "reducingRateSort": None,
                "skip": 0,
                "type": "Loans"
        }
        if bankname is None:
            # temporary text template 
            temp_text = "given below are personal loans <br>"
        else :
            # pushing provider 
            personalLoanApiData["provider"].append(bankname)
            temp_text = "given below are "+ bankname +" personal loans <br>"  
        msg = self.callPersonalLoansApi(personalLoanApiData)
        msg = temp_text + msg 
        dispatcher.utter_message(msg) #send the message back to the user
        return []
    #function for calling API and returning message
    def callPersonalLoansApi( self , personalLoanApiData ):
        msg = ''
        # url for calling personalloans api in MMS
        url = "http://localhost:3000/api/searach/loans/personalloans"
        # converting into json
        data_json = json.loads(json.dumps(personalLoanApiData))
        # calling api in MMS getting response
        response = requests.post(url, json=data_json)
        res_object = json.loads(response.text)
        # making link tags and appending into msg
        if(res_object["total"] > 0):
            for i in range(len(res_object["data"])):
                if not (i<5):
                    break
                href = "/personal-loan/" + res_object["data"][i]["productUrl"]
                text = res_object["data"][i]["provider"] + " " + res_object["data"][i]["planName"]
                link = "<a href='" + href + "' target='_blank' > " + text + "</a>" + "<br>"
                msg += link
        else:
            msg = "No data available for your query"
        return msg