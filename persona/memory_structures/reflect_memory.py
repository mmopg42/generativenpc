import os
current_file_path = os.path.abspath(__file__)
current_file_dir = os.path.dirname(current_file_path)
os.chdir(current_file_dir)

import sys
import json
# sys.path.append('../../')
from global_methods import *

# from server_python import *

class Reflectnode:
    def __init__(self, 
                 node_id, node_count, reflect_type,
                 reflect_time,
                 reflect_description,
                 daily_reflect_boolean):
        
        self.node_id = node_id
        self.node_count = node_count
        # 일자 기준인지 시간 기준인지
        # day, hour
        self.reflect_type = reflect_type
        # reflect 한 시간대
        self.reflect_time = reflect_time
        # 설명
        self.reflect_description = reflect_description
        # 일 리플랙트를 했는지 안 했는지
        self.daily_reflect_boolean = daily_reflect_boolean

class ReflectMemory:
    def __init__(self, f_saved):
        self.id_to_node = dict()
        self.f_saved = f_saved

        self.hour_reflect = None
        self.daily_reflect = None

        self.daily_reflect_boolean = None

        nodes_load = json.load(open(f_saved))
        for count in range(len(nodes_load.keys())):
            node_id = f"node_{str(count+1)}"
            node_details = nodes_load[node_id]
            node_count = node_details['node_count']
            reflect_type = node_details["reflect_type"]

            reflect_time = node_details["reflect_time"]
            reflect_description = node_details["reflect_description"]

            daily_reflect_boolean = node_details["daily_reflect_boolean"]
            
            self.add_reflect(reflect_type, reflect_time, reflect_description, daily_reflect_boolean)

    def save(self, out_json):
        r = dict()
        for count in range(len(self.id_to_node.keys()), 0, -1):
            node_id = f"node_{str(count)}"
            node = self.id_to_node[node_id]

            r[node_id] = dict()
            r[node_id]["node_count"] = node_node_count
            r[node_id]["reflect_type"] = node.reflect_type
            r[node_id]["reflect_time"] = node.reflect_time
            r[node_id]["reflect_description"] = node.reflect_description
            r[node_id]["daily_reflect_boolean"] = node.daily_reflect_boolean

        with open(out_json + '/reflect_node.json', "w") as outfile:
            json.dump(r, outfile)


    def load_reflect_memory(self):
        # 이전까지 reflect 했던 내용을 반환
        nodes = [node.reflect_description for node in self.id_to_node.values()]
        return nodes
        

    def add_reflect(self, reflect_type, reflect_time,
                    reflect_description, daily_reflect_boolean):
        node_count = len(self.id_to_node.keys())+1
        node_id = f"node_{str_node_count}"
        node = Reflectnode(node_id, node_count, reflect_type,
                           reflect_description, daily_reflect_boolean)
        self.id_to_node[node_id] = node

        return node


    def generate_hour_reflect(self, persona):
        # hour_reflect가 False인 노드들의 description을 가져오고, 동시에 hour_reflect 값을 업데이트
        node_description = []
        for node in persona.a_mem.id_to_node.values():
            if node.hour_reflect == False:
                node_description.append(node.description)
                node.hour_reflect = True  # hour_reflect 값을 True로 설정

        # description 리스트를 문자열로 변환
        node_description_str = '\n'.join(node_description)
        output = run_prompt_generate_hour_reflect(persona, node_description_str)
        reflect_time = load_game_time().strftime('%A %B %d %H')
        self.add_reflect('hour', reflect_time, output, False)


    def generate_daily_reflect(self, persona):
        node_description = []
        for node in persona.a_rem.id_to_node.values():
            if node.daily_reflect_boolean == False:
                node_description.append(node.reflect_description)
                node.daily_reflect_boolean == True
        node_description_str = '\n'.join(node_description)
        output = run_prompt_generate_daily_reflect(persona, node_description_str)
        reflect_time = load_game_time().strftime('%A %B %d')
        self.add_reflect('daily', reflect_time, output, False)
        

if __name__ =="__main__":
    pass

