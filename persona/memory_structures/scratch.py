"""
출처: https://github.com/joonspk-research/generative_agents/blob/main/reverie/backend_server/persona/memory_structures/scratch.py

생성형 에이전트의 단기 메모리 모듈
"""

import datetime
import json
import sys

# sys.path.append('../../')

from global_methods import *

# from server_python import *

class Scratch:
    def __init__(self, f_saved):


        # 현재 시간
        self.curr_time = None
        # 게임 시간
        self.curr_game_time = None
        # 현재 xyz 좌표
        self.curr_xyz = None
        # 현재 장소
        self.curr_place = None

        # 이름
        self.name = None
        # 나이
        self.age = None
        # 선천적 특성
        self.innate = None
        # 후천적 경험
        self.background = None
        # 장기목표
        self.long_term_goal = None
        # 단기목표
        self.short_term_goal = None
        # 현재 상태
        self.currently = None
        # 기본 삶
        self.lifestyle = None
        # 집
        self.living_area = None

        
        # 하루 목적을 정리
        self.daily_req = []
        # 하루 시간당 계획
        self.daily_schedule_hourly = []
        # 하루 분당 계획
        self.daily_schedule_min = []

        self.act_descruption = None 
        self.emoji = None
        self.location = None
        self.act_object= None
        
        # 현재 액션 상태
        self.act_duration = None
        self.act_event = None
        self.chatting_with = None
        self.chat = None

        if check_if_file_exists(f_saved):
            scratch_load = json.load(open(f_saved))

            if scratch_load['curr_time']:
                self.curr_time = datetime.datetime.strptime(scratch_load['curr_time'], "%B %d, %Y, %H:%M:%S")
            else:
                curr_time = datetime.datetime.now()
                self.curr_time = datetime.datetime.now().strftime("%B %d, %Y, %H:%M:%S")
            try:
                self.curr_game_time = load_game_time()
            except:
                self.curr_game_time = datetime.datetime.strptime(self.curr_time, "%B %d, %Y, %H:%M:%S").strftime("%A %B, %d, %H:%M:%S")
            # if scratch_load['curr_xyz']:
            #     self.curr_xyz = scratch_load['curr_xyz']
            # else:
            #     self.curr_xyz=None

            self.curr_place = scratch_load['curr_place']

            self.name = scratch_load["name"]
            self.age = scratch_load["age"]
            self.innate = scratch_load["innate"]
            self.background = scratch_load["background"]
            self.long_term_goal = scratch_load["long_term_goal"]
            self.short_term_goal = scratch_load["short_term_goal"]
            self.currently = scratch_load["currently"]
            self.lifestyle = scratch_load["lifestyle"]
            self.living_area = scratch_load["living_area"]


            # 하루 목적을 정리
            self.daily_req = scratch_load['daily_req']
            # 하루 시간당 계획
            self.daily_schedule_hourly = scratch_load['daily_schedule_hourly']
            # 하루 분당 계획
            self.daily_schedule_min = scratch_load['daily_schedule_min']
    
            self.act_description = scratch_load['act_description']
            self.emoji = scratch_load['emoji']
            self.location = scratch_load['location']
            self.act_object = scratch_load['act_object']
        
            
            self.act_duration = scratch_load['act_duration']
            self.act_event = scratch_load['act_event']
            self.chatting_with = scratch_load['chatting_with']
            self.chat = scratch_load['chat']

    
    def save(self, out_json):
        """
        scratch 정보를 저장한다
        """
        scratch = dict() 
        # 현재 시간
        scratch['curr_time']=self.curr_time
        # 현재 게임 시간
        try:
            scratch['curr_game_time']=self.curr_game_time
        except:
            scratch['curr_game_time']=self.curr_time
        # 현재 xyz 좌표
        scratch['curr_xyz']=self.curr_xyz
        # 현재 장소
        scratch['curr_place']=self.curr_place


        # 이름
        scratch['name']=self.name
        # 나이
        scratch['age']=self.age
        # 선천적 특성
        scratch['innate']=self.innate
        # 후천적 경험, background
        scratch['background']=self.background
        # 장기목표
        scratch["long_term_goal"] = self.long_term_goal
        # 단기목표
        scratch["short_term_goal"] = self.short_term_goal
        # 현재 상태
        scratch['currently']=self.currently
        # 기본 삶
        scratch['lifestyle']=self.lifestyle
        # 집
        scratch['living_area']=self.living_area

        
        # 하루 목적을 정리
        scratch['daily_req']=self.daily_req
        # 하루 시간당 계획
        scratch['daily_schedule_hourly']=self.daily_schedule_hourly
        # 하루 분당 계획
        scratch['daily_schedule_min']=self.daily_schedule_min
        
        scratch['act_description'] = self.act_description
        scratch['act_object'] = self.act_object
        scratch['emoji'] = self.emoji
        scratch['location'] = self.location
        # 현재 액션 상태
        scratch['act_start_time'] = self.act_start_time
        scratch['act_duration'] = self.act_duration
        # scratch['act_spo'] = self.act_spo
        scratch['chatting_with'] = self.chatting_with
        scratch['chat'] = self.chat


    def get_daily_plan_hourly_index(self, advance=0):
        """
        시간별 스케쥴을 입력 받아서 현재 시간의 시간별 스케쥴의 인덱스를 가져온다.
        """

        today_min_elapsed = 0
        today_min_elapsed += self.curr_game_time.hour * 60
        today_min_elapsed += self.curr_game_time.minute
        today_min_elapsed += advance

        curr_index = 0
        elapsed = 0
        for task, duration in self.daily_schedule_hourly:
            elapsed += duration
            if elapsed > today_min_elapsed:
                return curr_index
            curr_index += 1

        return curr_index
            

    def get_daily_schedule_min_index(self, advance=0):
        """
        분별 스케쥴을 입력 받아서 현재 분의 스케쥴 인덱스를 가져온다
        """
        today_min_elapsed = 0
        today_min_elapsed += self.curr_game_time.hour * 60
        today_min_elapsed += self.curr_game_time.minute
        today_min_elapsed += advance


        curr_index = 0
        elapsed = 0
        for task, duration in self.daily_schedule_min: 
            elapsed += duration
            if elapsed > today_min_elapsed: 
                return curr_index
            curr_index += 1
        return curr_index
    

    def get_sentence_iss(self):
        """
        0 : 이름
        1 : 나이
        2 : innate
        3 : background
        4 : long-term goal
        5 : short-term goal
        6 : currently
        7 : lifestyle
        8 : plan_request
        9 : current_data
        """
        if not isinstance(self.curr_time, datetime.datetime):
            self.curr_time = datetime.datetime.strptime(
                self.curr_time, "%B %d, %Y, %H:%M:%S")
        if self.daily_req == []:
            text = "The name of <0> is <0>. The age of <0> is <1> years old. The Innate traits of <0> are <2>. The Background of <0> are <3>. The long-term goal of <0> is <4>. <0>'s short-term goal is <5>.Recently, <0> has been <6>. The Lifestyle of <0> is <7>. Current Data is <8>."
            data = [self.name, str(self.age), self.innate, self.background, self.long_term_goal, self.short_term_goal, self.currently, self.lifestyle, self.curr_time.strftime('%A %B %d')]
            
        else:       
            text = "The name of <0> is <0>. The age of <0> is <1> years old. The Innate traits of <0> are <2>. The Background of <0> are <3>. The long-term goal of <0> is <4>. <0>'s short-term goal is <5>.<0> has been recently thinking like <6>. The Lifestyle of <0> is <7>. To determine the daily request of <0> is <8>. Current Data is <9>."
            data = [self.name, str(self.age), self.innate, self.background, self.long_term_goal, self.short_term_goal, self.currently, self.lifestyle, self.daily_req, self.curr_time.strftime('%A %B %d')]
        
        
        for index, value in enumerate(data):
            text = text.replace(f"<{index}>", value)

        return text
    

    def get_f_daily_schedule_hourly_org_index(self, advance=0):
        """
        self.f_daily_schedule_hourly_org의 현재 인덱스를 가져온다.
        그 위에는 get_f_daily_schedule_index와 동일하다.

        INPUT
            advance: 미래의 시간을 몇 분 뒤로 볼 것인지에 대한 정수 값.
            이를 통해 미래 시점의 인덱스를 얻을 수 있다.
        OUTPUT
            f_daily_schedule의 현재 인덱스에 대한 정수 값
        """
        # 우선 오늘 지난 분의 수를 계산한다.
        today_min_elapsed = 0
        today_min_elapsed += self.curr_time.hour * 60
        today_min_elapsed += self.curr_time.minute
        today_min_elapsed += advance
        # 그 다음 그를 기반으로 현재 인덱스를 계산한다.
        
        curr_index = 0
        elapsed = 0
        # f_daily_schedule 에서 시간을 가져온다.
        # 해당 시간을 elapsed에 넣는다
        # 만약 elapsed가 today_min_elapsed(현재 시간) 보다 커지면
        # 해당 인덱스를 반환한다
        # 만약 크지 않으면 +1 을 하여 다음 인덱스를 탐색한다.
        for task, duration in self.f_daily_schedule_hourly_org:
            elapsed += duration
            if elapsed > today_min_elapsed:
                return curr_index
            curr_index += 1

        return curr_index


    def get_str_iss(self):
        """
        ISS는 "정체성 안정 집합(Identity Stable Set)"를 의미한다. 이것은 이 페르소나의 공통 요약 집합을 설명하는 것으로, 거의 모든 프롬프트에서 페르소나를 호출할 때 사용되는 기본 최소 설명이다

        INPUT:
            None
        OUTPUT:
            문자열 형태로 된 페르소나의 정체성 안정 집합 요약
        EXAMPLE:
            "Name: Dolores Heitmiller
            Age: 28
            Innate traits: hard-edged, independent, loyal
            backgrounds: Dolores is a painter who wants live quietly and paint 
                while enjoying her everyday life.
            Currently: Dolores is preparing for her first solo show. She mostly 
                works from home.
            Lifestyle: Dolores goes to bed around 11pm, sleeps for 7 hours, eats 
                dinner around 6pm.
            Daily plan requirement: Dolores is planning to stay at home all day and 
                never go out."

            들어가는 것은 이름, 나이, 선천적 특성, 후천적 특성, 현재, 라이프스타일, 일일 요구사항이다
        """
        commonset = ""
        commonset += f"Name: {self.name}\n"
        commonset += f"Age: {self.age}\n"
        commonset += f"Innate traits: {self.innate}\n"
        commonset += f"Background: {self.background}\n"
        commonset += f"Currently: {self.currently}\n"
        commonset += f"Lifestyle: {self.lifestyle}\n"
        commonset += f"Daily plan requirement: {self.daily_req}\n"
        if not isinstance(self.curr_time, datetime.datetime):
            self.curr_time=datetime.datetime.strptime(
                self.curr_time, "%B %d, %Y, %H:%M:%S")
        commonset += f"Current Date: {self.curr_time.strftime('%A %B %d')}\n"
        # curr_time_obj = datetime.datetime.strptime("November 6, 2023, 00:00:00", "%B %d, %Y, %H:%M:%S")
        # 그 다음, datetime 객체에 대해 strftime 메서드를 사용하여 원하는 형식의 문자열로 변환합니다.
        # formatted_date = curr_time_obj.strftime('%A %B %d')
        # # 이제 formatted_date를 문자열에 추가합니다.
        # commonset += f"Current Date: {formatted_date}\n"
        return commonset


    def get_str_curr_date_str(self): 
        if not isinstance(self.curr_time, datetime.datetime):
            self.curr_time=datetime.datetime.strptime(
                    self.curr_time, "%B %d, %Y, %H:%M:%S")
        return self.curr_time.strftime("%A %B %d")


    def get_curr_event(self):
        if not self.act_address: 
            return (self.name, None, None)
        else: 
            return self.act_event
        
    def get_curr_event_and_desc(self): 
        if not self.act_address: 
            return (self.name, None, None, None)
        else: 
            return (self.act_event[0], 
                    self.act_event[1], 
                    self.act_event[2],
                    self.act_description)


    def get_curr_obj_event_and_desc(self): 
        if not self.act_address: 
            return ("", None, None, None)
        else: 
            return (self.act_address, 
                    self.act_obj_event[1], 
                    self.act_obj_event[2],
                    self.act_obj_description)


    def add_new_action(self, 
                        action_address, 
                        action_duration,
                        action_description,
                        action_pronunciatio, 
                        action_event,
                        chatting_with, 
                        chat, 
                        chatting_with_buffer,
                        chatting_end_time,
                        act_obj_description, 
                        act_obj_pronunciatio, 
                        act_obj_event, 
                        act_start_time=None): 
        self.act_address = action_address
        self.act_duration = action_duration
        self.act_description = action_description
        self.act_pronunciatio = action_pronunciatio
        self.act_event = action_event

        self.chatting_with = chatting_with
        self.chat = chat 
        if chatting_with_buffer: 
            self.chatting_with_buffer.update(chatting_with_buffer)
        self.chatting_end_time = chatting_end_time

        self.act_obj_description = act_obj_description
        self.act_obj_pronunciatio = act_obj_pronunciatio
        self.act_obj_event = act_obj_event

        self.act_start_time = self.curr_time

        self.act_path_set = False


    def act_time_str(self): 
        """
        Returns a string output of the current time. 

        INPUT
            None
        OUTPUT 
            A string output of the current time.
        EXAMPLE STR OUTPUT
            "14:05 P.M."
        """
        return self.act_start_time.strftime("%H:%M %p")


    def act_check_finished(self): 
        """
        Checks whether the self.Action instance has finished.  

        INPUT
            curr_datetime: Current time. If current time is later than the action's
                            start time + its duration, then the action has finished. 
        OUTPUT 
            Boolean [True]: Action has finished.
            Boolean [False]: Action has not finished and is still ongoing.
        """
        if not self.act_address: 
            return True
            
        if self.chatting_with: 
            end_time = self.chatting_end_time
        else: 
            x = self.act_start_time
            if x.second != 0: 
                x = x.replace(second=0)
                x = (x + datetime.timedelta(minutes=1))
            end_time = (x + datetime.timedelta(minutes=self.act_duration))

        if end_time.strftime("%H:%M:%S") == self.curr_time.strftime("%H:%M:%S"): 
            return True
        return False


    def act_summarize(self):
        """
        Summarize the current action as a dictionary. 

        INPUT
            None
        OUTPUT 
            ret: A human readable summary of the action.
        """
        exp = dict()
        exp["persona"] = self.name
        exp["address"] = self.act_address
        exp["start_datetime"] = self.act_start_time
        exp["duration"] = self.act_duration
        exp["description"] = self.act_description
        exp["pronunciatio"] = self.act_pronunciatio
        return exp


    def act_summary_str(self):
        """
        Returns a string summary of the current action. Meant to be 
        human-readable.

        INPUT
            None
        OUTPUT 
            ret: A human readable summary of the action.
        """
        start_datetime_str = self.act_start_time.strftime("%A %B %d -- %H:%M %p")
        ret = f"[{start_datetime_str}]\n"
        ret += f"Activity: {self.name} is {self.act_description}\n"
        ret += f"Address: {self.act_address}\n"
        ret += f"Duration in minutes (e.g., x min): {str(self.act_duration)} min\n"
        return ret


    def get_str_daily_schedule_summary(self): 
        ret = ""
        curr_min_sum = 0
        for row in self.f_daily_schedule: 
            curr_min_sum += row[1]
            hour = int(curr_min_sum/60)
            minute = curr_min_sum%60
            ret += f"{hour:02}:{minute:02} || {row[0]}\n"
        return ret


    def get_str_daily_schedule_hourly_org_summary(self): 
        ret = ""
        curr_min_sum = 0
        for row in self.f_daily_schedule_hourly_org: 
            curr_min_sum += row[1]
            hour = int(curr_min_sum/60)
            minute = curr_min_sum%60
            ret += f"{hour:02}:{minute:02} || {row[0]}\n"
        return ret    

if __name__ =="__main__":
    # scratch_saved = f"/home/elicer/main/agents_test/frontend/persona/Tom/bootstrap_memory/scratch.json"
    # scratch = Scratch(scratch_saved)
    # print(scratch.get_str_iss())
    # print(scratch.curr_time)
    pass