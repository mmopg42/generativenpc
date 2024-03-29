"""
출처: https://github.com/joonspk-research/generative_agents/blob/main/reverie/backend_server/persona/prompt_template/print_prompt.py

들어간 프롬프트를 확인합니다.

"""

import sys
sys.path.append('../')

import json
import numpy
import datetime
import random

from persona.prompt_template.gpt_structure import *


def print_run_prompts(prompt_template=None, 
                      persona=None, 
                      gpt_param=None, 
                      prompt_input=None,
                      prompt=None, 
                      output=None): 
    
    print (f"=== {prompt_template}")
    print ("~~~ persona    ---------------------------------------------------")
    print (persona.name, "\n")
    print ("~~~ gpt_param ----------------------------------------------------")
    print (gpt_param, "\n")
    print ("~~~ prompt_input    ----------------------------------------------")
    print (prompt_input, "\n")
    print ("~~~ prompt    ----------------------------------------------------")
    print (prompt, "\n")
    print ("~~~ output    ----------------------------------------------------")
    print (output, "\n") 
    print ("=== END ==========================================================")
    print ("\n\n\n")
