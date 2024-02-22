import os
current_file_path = os.path.abspath(__file__)
current_file_dir = os.path.dirname(current_file_path)
os.chdir(current_file_dir)

import sys
sys.path.append(current_file_dir)
sys.path.append('../../')

# from global_methods import *

from persona.prompt_template.run_gpt_prompt import *


def generate_wake_up_hour(persona):
    """
    페르소나가 깨어나는 시간을 생성한다. 이것은 페르소나의 일일 계획을 생성하는 과정에서 중요한 부분이 된다.

    Persona state: identity stable set(정체성 안정 set), lifestyle, first_name

    INPUT:
        persona: 페르소나 클래스 인스턴스
    OUTPUT:
        페르소나가 깨어나는 시간을 나타내는 정수
    EXAMPLE OUTPUT:
        8
    """
    
    return run_prompt_wake_up_hour(persona)

def generate_daily_request(persona, new_day=None):
    """
    이전 일을 고려하여 할일 생성
    원래 코드에선s revise로 했으나, past_summarize 로 대체하여 지난날을 요약 한 내용을 컨텍스트로 넣는다.
    """
    # for index, node in persona.a_mam.id_to_node.items():
    #     node=first
    output = run_prompt_generate_daily_request(persona, new_day)
    return output


def hour_plan_preprocessing(plan):
    result = []
    for line in plan.split('\n'):
        match = re.search(r'\[.* (\d+):\d+\]: (.*)', line)  # 수정된 정규식 패턴
        if match:
            hour = int(match.group(1))
            description = match.group(2)
            duration = 60  # 1 시간
            result.append([description, duration])
    return result


def generate_daily_schedule_hourly(persona, wakeup_time, new_day=None):
    """
    하루의 시간당 플랜
    """

    output_hourly_plan = run_prompt_generate_daily_schedule_hourly(persona, wakeup_time)
    # output = hour_plan_preprocessing(output_hourly_plan)
    return output_hourly_plan

# def past_daily_summarize(persona):
