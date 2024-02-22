"""
출처: https://github.com/joonspk-research/generative_agents/blob/main/reverie/backend_server/persona/prompt_template/gpt_structure.py


gpt 활용 래퍼
"""

import json
import random
# import openai
import time 

import os
current_file_path = os.path.abspath(__file__)
current_file_dir = os.path.dirname(current_file_path)
os.chdir(current_file_dir)

import sys
# sys.path.append('../../')

# sys.path.append('../')
# sys.path.append('../../../')

from model.run_exllama import *

from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings


def temp_sleep(seconds=0.1):
    time.sleep(seconds)


def Local_single_request(prompt):
    temp_sleep()

    """
    간단한 프롬프트.
    여길 수정해 주세요
    """

    

def generate_prompt(curr_input, prompt_lib_file):
    """
    들어온 입력값을 템플릿에 맞게 변형한다.

    INPUT:
        curr_input: 입력으로 넣고 싶은 값을 넣는다. 여러 개일 경우 리스트가 된다.
        이 값은 템플릿에 들어갈 INPUT 부분이다.
        prompt_lib_file: 프롬프트 템플릿이다.
    RETURNS:
        prompt.strip(): 템플릿에 있는 INPUT 부분을 바꿔쳐서 리턴한다.
    """
    import os
    current_file_path = os.path.abspath(__file__)
    # current_file_dir = os.path.dirname(current_file_path)
    os.chdir(current_file_dir)
    # 입력값 타입이 str인지 확인
    # 해당 타입이 리스트가 아니기에 리스트로 바꿔서 저장
    if type(curr_input) == type("string"):
        # 입력값을 리스트로 바꿔서 curr_input에 저장
        curr_input = [curr_input]
    # 리스트로 들어온 값을 컴프리헨션을 통해 하나씩 저장.
    curr_input = [str(i) for i in curr_input]

    # 프롬프트 템플릿 열기
    f = open(prompt_lib_file,'r')
    
    # f = open('local/generate_converse_first_v3.txt', 'r')
    prompt = f.read()
    f.close()

    # for 문을 돌아서 해당하는 값을 replace를 통해 i로 바꾼다.
    for count, i in enumerate(curr_input):
        prompt = prompt.replace(f"!<INPUT {count}>!", i)
    
    # 아래의 문장 밑에 부분만 리턴한다.
    if "<commentblockmarker>###</commentblockmarker>" in prompt:
        # 블록 마커 기준으로 나눠서 밑에 프롬프트에 넣는다.
        prompt = prompt.split("<commentblockmarker>###</commentblockmarker>")[1]

    return prompt.strip()


#############################################################
# [LOCAL STRUCTURE]
#############################################################

def local_request(prompt, parameter, test_prompt=None):
    """
    프롬프트를 로컬 모델에 보내서 대답을 생성합니다.
    
    이 부분을 수정해서 본인의 로컬 모델에 맞게 사용합시다.
    """
    temp_sleep()
    if test_prompt:
        print("local_request 를 시험 중입니다.")
    # print(prompt)
    try:
        # model = load_model("/home/elicer/main/models/Synatra-7B-v0.3-base-exl2")
        # model = load_model('/home/elicer/main/utopiaxl/model/')
        model = load_model('/home/elicer/main/models/zephyr-7b-beta-5.0bpw-exl2')
        
        settings = ExLlamaV2Sampler.Settings()
        settings.temperature = parameter['temperature']
        # settings.top_k = 50
        settings.top_p = parameter['top_p']
        max_new_tokens = parameter['max_tokens']

        # system_prompt = "You are HelixNet. Elaborate on the topic using a Tree of Thoughts and backtrack when necessary to construct a clear, cohesive Chain of Thought reasoning. Always answer without hesitation."

        # user_input = input("You: ")
        user_input = f"""{prompt}"""
        # print(user_input)

        prompt = f"<|user|>: {user_input}\n\n<|assistant|>: "
        response = generate_text(prompt, model, settings, max_new_tokens)
        print(response)
        return response
    
    except:
        print ("local_request error")

def safe_local_generate_response(prompt,
                                parameter,
                                repeat=5,
                                fail_safe_response='error',
                                func_validate=None,
                                func_clean_up=None,
                                verbose=False):
    """
    들어온 prompt 를 local_request에 보내서 값을 받아온다. 
    repeat 횟수만큼 반복하며, func_validate을 통과할 경우, func_clean_up을 반환. repeat 횟수 전부 실패하면 fail_safe_response에 해당하는 값을 반환한다.
    디버깅을 할 때는 verbose 를 True로 할 것

    """
    if verbose:
        print (prompt)

    for i in range(repeat):
        curr_local_response = local_request(prompt, parameter, test_prompt=verbose)

        if verbose:
            print("---- repeat count: ", i, curr_local_response)
            print(curr_local_response)
            print("~~~~~~~~~~~~~~~~")

        # 답변이 제대로 들어왔는지 확인. 확인이 되면
        # func_clean_up 으로 정제한 답변을 리턴한다.
        if func_validate(curr_local_response):
            return func_clean_up(curr_local_response)

    
    return fail_safe_response



def nonsafe_local_generate_response(prompt,
                                parameter,
                                fail_safe_response='error',
                                verbose=False):
    """
    들어온 prompt 를 local_request에 보내서 값을 받아온다. 
    repeat 횟수만큼 반복하며, func_validate을 통과할 경우, func_clean_up을 반환. repeat 횟수 전부 실패하면 fail_safe_response에 해당하는 값을 반환한다.
    디버깅을 할 때는 verbose 를 True로 할 것

    """
    if verbose:
        print (prompt)


    curr_local_response = local_request(prompt, parameter, test_prompt=verbose)
    print(curr_local_response)
    if verbose:
        print("---- repeat count: ", i, curr_local_response)
        print(curr_local_response)
        print("~~~~~~~~~~~~~~~~")

        # 답변이 제대로 들어왔는지 확인. 확인이 되면
        # func_clean_up 으로 정제한 답변을 리턴한다.

    
    return curr_local_response


#############################################################
# [GPT STRUCTURE]
#############################################################

os.environ['OPENAI_API_KEY'] = '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'

def get_embedding(text):
    # text = text.replace("\n", " ")
    model = OpenAIEmbeddings()
    outcome = model.embed_query(text)
    return outcome

# def get_embedding(text, model="text-embedding-ada-002"):
#   text = text.replace("\n", " ")
#   if not text: 
#     text = "this is blank"
#   return openai.Embedding.create(
#           input=[text], model=model)['data'][0]['embedding']


def safe_gpt3_generate_response(prompt,
                                parameter,
                                repeat=3,
                                func_validate=None,
                                func_clean_up=None,
                                verbose=False,
                                fail_safe_response='error'):
    if func_validate!=None:
        for i in range(repeat):
        
            llm = ChatOpenAI(**parameter)
            response = llm.predict(prompt)

            if verbose:
                print("---- repeat count: ", i, response)
                print("~~~~~~~~~~~~~~~~")
                
            if func_validate(response):
                return func_clean_up(response)
            
        return fail_safe_response

    llm = ChatOpenAI(**parameter)
    response = llm.predict(prompt)
    return response

if __name__ == "__main__":
    pass

