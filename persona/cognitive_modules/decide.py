import os
current_file_path = os.path.abspath(__file__)
current_file_dir = os.path.dirname(current_file_path)
os.chdir(current_file_dir)

import json

import sys
sys.path.append('../../')

from global_methods import *

from persona.cognitive_modules.retrieve import *

from persona.prompt_template.run_gpt_prompt import *

from game_start import *


# 반응할지 말지를 결정하는 함수
# 페르소나와, 페르소나의 objects를 통해서 
def decide_react(persona, objects, player_action, player_chat):
    if player_action:
        decide_player(persona, objects, player_action, player_chat)

    retrieved = new_retrieve(persona, objects)
    # 행동을 할지 말지 결정
    output = run_prompt_generate_decide(persona, objects, retrieved)
    return output

# 채팅에 반응할지 말지를 결정
def decide_chat_react(persona, object):

    return None

def generate_plan_based_decide_action(persona, player_action=None, player_chat=None):
    """
    
    """
    if player_action!=None:
        pass

    load_reflect_description = persona.r_mem.load_reflect_memory()
    curr_context = [node.description for node in persona.a_mem.id_to_node.values() if node.hour_reflect==False]

    load_reflect_description_join = "\n".join(load_reflect_description)
    curr_context_jon = "\n".join(curr_context)

    output = run_prompt_generate_plan_based_decide_action(persona,load_reflect_description_join, curr_context_jon)

    return output

def generate_perceive_based_decide_action(persona, objects, player_action, player_chat):
    """

    """
    load_reflect_description = persona.r_mem.load_reflect_memory()
    curr_context = [node.description for node in persona.a_mem.id_to_node.values() if node.hour_reflect==False]

    load_reflect_description_join = "\n".join(load_reflect_description)
    curr_context_jon = "\n".join(curr_context)

    output = run_prompt_generate_plan_based_decide_action(persona,objects,load_reflect_description_join, curr_context_jon)
    return None


