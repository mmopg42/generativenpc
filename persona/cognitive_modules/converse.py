import os
current_file_path = os.path.abspath(__file__)
current_file_dir = os.path.dirname(current_file_path)
os.chdir(current_file_dir)

import sys
sys.path.append(current_file_dir)
sys.path.append('../../')

from global_methods import *
from game_start import *

from persona.memory_structures.associative_memory import *

from persona.cognitive_modules.retrieve import *

from persona.prompt_template.run_gpt_prompt import *


def generate_chat_summarize(init_persona, target_persona):
    
    init_persona_curr_chat = init_persona.a_mem.curr_chat
    target_persona_curr_chat = target_persona.a_mem.curr_chat

    poignancy = generate_poignancy(init_persona,init_persona_curr_chat, event_type='chat')

    summarize, thought = run_prompt_chat_summarize(init_persona, target_persona, init_persona_curr_chat)
    
    chat_summarize_embedding = get_embedding(f'{summarize} {thought}')

    embedding_pair = [summarize, chat_summarize_embedding]
    curr_time = load_game_time()
    # curr_time = 'x시간'
    init_persona.a_mem.add_chat(init_persona.scratch.name, 'chat with', target_persona.scratch.name, curr_time,
                                summarize, thought, embedding_pair, 
                                init_persona_curr_chat, poignancy,
                                False)
    print(f'save {init_persona}')
    init_persona.a_mem.curr_chat = []


def agent_chat_one_utterance_new(init_persona, target_personas):
    curr_chat = []
    if init_persona.a_mem.curr_chat == []:
        if len(target_personas) != 1:
            target_persona = random.choice(target_personas)
        else:
            target_persona = target_personas[0]
        focal_points = [f"{target_persona.scratch.name}"]
        retrieved = new_retrieve(init_persona, focal_points, 50)
        target_relationship = init_persona.a_mem.load_relationship(target_persona)
        last_chat = ""
        utt, end = run_prompt_generate_converse_first(init_persona, target_persona, retrieved, target_relationship, model='local')
        repeat = 0
        # while not check_action_state():
        #     time.sleep(3)
        #     repeat += 1
        #     if repeat == 10:
        #         end_curr_chat_node(init_persona, target_persona)
        #         end_curr_chat_node(target_persona, init_persona)
        #         return False
    else: 
        # if not generate_decide_chat_react(target_persona, ):
        #     return end
        if len(target_personas) != 1:
            target_persona = random.choice(list)
        else:
            target_persona = target_personas[0]
        focal_points = [f"{target_persona.scratch.name}"]
        retrieved = new_retrieve(init_persona, focal_points, 50)
        target_relationship = init_persona.a_mem.load_relationship(target_persona)
        last_chat = ""
        utt, end = run_prompt_generate_converse_second(init_persona, target_persona, retrieved, target_relationship, model='local')
        repeat = 0
        # while not check_action_state():
        #     time.sleep(3)
        #     repeat += 1
        #     if repeat == 10:
        #         end_curr_chat_node(init_persona, target_persona)
        #         end_curr_chat_node(target_persona, init_persona)
        #         return False        
    init_persona.a_mem.add_curr_chat(utt)
    for i in target_personas:
        i.a_mem.add_curr_chat(utt)
    print(init_persona.a_mem.curr_chat)
 
    if end:
        generate_chat_summarize(init_persona, target_persona)
        for i in target_personas:
            generate_chat_summarize(i, init_persona)

    return utt


def agent_chat_one_utterance(init_persona, target_persona):
    curr_chat = []
    focal_points = [f"{target_persona.scratch.name}"]
    retrieved = new_retrieve(init_persona, focal_points, 50)
    # retrieved = 'asd'
    target_relationship = init_persona.a_mem.load_relationship(target_persona)
    last_chat = ""
    if init_persona.a_mem.curr_chat == []:
        utt, end = run_gpt_generate_converse_first(init_persona, target_persona, retrieved, target_relationship, model='gpt')
    else:
        utt, end = run_prompt_generate_converse_second(init_persona, target_persona, retrieved, target_relationship)
    
    if end:
        init_persona.a_mem.add_curr_chat(utt)
        target_persona.a_mem.add_curr_chat(utt)
        # generate_agent_chat_summarize
    init_persona.a_mem.add_curr_chat(utt)
    print(init_persona.a_mem.curr_chat)
    target_persona.a_mem.add_curr_chat(utt)

    return init_persona.a_mem.curr_chat

if __name__ == '__main__':
    # new_retrieve()
    pass

# def generate_decide_chat_react()