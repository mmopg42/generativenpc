"""

"""
import os
current_file_path = os.path.abspath(__file__)
current_file_dir = os.path.dirname(current_file_path)
os.chdir(current_file_dir)

import sys
sys.path.append(current_file_dir)
sys.path.append('../../')

import json
import datetime

from global_methods import *

# from persona.cognitive_modules.retrieve import *

# from persona.prompt_template.run_gpt_prompt import *

# 모든 상황은 event다
# action, chat, thought

class ConceptNode:
    def __init__(self,
                 node_id, node_count, event_type,
                 s, p, o, created,
                 description, thought, embedding_key, 
                 curr_chat, poignancy,
                 hour_reflect):
        
        self.node_id = node_id
        self.node_count = node_count
        # action, chat, thought
        self.event_type = event_type

        self.created = created
        self.last_accessed = self.created
        
        """
        action 일 경우
            s = 주체
            p = 행동
            o = 대상
        
        chat 일 경우
            s = 주체
            p = chat with
            o = 대상
        """
        self.subject = s
        self.predicate = p
        self.object = o

        self.spo = (s, p, o)

        """
        실제 내용
        action 일 경우
            행동 내용
        chat 일 경우
            대화 요약 내용
        """
        self.description = description
        self.thought = thought

        self.embedding_key = embedding_key

        # 실제 대화 내용
        self.curr_chat = curr_chat
        # 해당 행동에 대해서 perosna의 생각을 저장
        self.poignancy = poignancy

        # reflect 변수, True, False
        self.hour_reflect = hour_reflect


    # print 시 출력되는 부분
    def __str__(self):
        return f"""ConceptNode:
node_id: {self.node_id}, 
node_count: {self.node_count}, 
event_type: {self.event_type}, 
created: {self.created}, 
last_accessed: {self.last_accessed}, 
subject: {self.subject}, 
predicate: {self.predicate}, 
object: {self.object}, 
spo: {self.spo}, 
description: {self.description}, 
thought: {self.thought}, 
embedding_key: {self.embedding_key}, 
curr_chat: 
{self.curr_chat}, 
poignancy: {self.poignancy}
hour_reflect: {self.hour_reflect}"""

    def spo_summary(self):
        return (self.subject, self.predicate, self.object)


class AssociativeMemory:
    def __init__(self, f_saved):
        self.id_to_node = dict()
        self.f_saved = f_saved

        self.seq_event = []
        self.seq_thought = []
        self.curr_chat = []

        self.relationship = json.load(open(self.f_saved+ "/relationship.json"))
        self.embeddings = json.load(open(self.f_saved + "/embeddings.json"))

        nodes_load = json.load(open(f_saved + "/nodes.json"))
        for count in range(len(nodes_load.keys())):
            node_id = f"node_{str(count+1)}"
            node_details = nodes_load[node_id]
            node_count = node_details['node_count']
            event_type = node_details["event_type"]

            if node_details["created"]== "":
                curr_time
            created = datetime.datetime.strptime(node_details["created"], 
                                           '%Y-%m-%d %H:%M:%S')          

            s = node_details["subject"]
            p = node_details["predicate"]
            o = node_details["object"]

            description = node_details["description"]
            thought = node_details["thought"]

            embedding_pair = (node_details["embedding_key"], 
                        self.embeddings[node_details["embedding_key"]])
            
            if event_type=='chat':
                curr_chat = node_details['curr_chat']
            else:
                curr_chat = 'null'
            poignancy = node_details["poignancy"]
            hour_reflect = node_details["hour_reflect"]
            
            if event_type == "action": 
                self.add_action(s, p, o, created,
                        description, thought, embedding_pair,
                        curr_chat, poignancy,
                        hour_reflect)
            elif event_type == "chat": 
                self.add_chat(s, p, o, created,
                        description, thought, embedding_pair,
                        curr_chat, poignancy,
                        hour_reflect)   
            # TODO
            # description 과 thought 를 분리한 후, 저장
            # 이후 retrieve 에서 관련된 사항을 불러올 때, thought와 그와 관련된 컨텍스트에 해당되는 description 를 불러오지 않아도 되나? 에 대한 의문 해결 할것
            # 혹은 따로 불러와서 관계가 있으면 관계를 넣어서 embedding을 저장하는 방법도 고려할 것
            # elif event_type == "thought":
            #     self.add_thought(s, p, o,
            #             description, thought, embedding_pair,
            #             curr_chat, poignancy)      


    def find_nodes_by_subject(self, subjects):
        # subject를 기준으로 노드를 찾는다.
        # node의 subject에 입력으로 들어온 subject가 존재한다면, 해당 노드를 리스트에 넣어서 반환
        return [node for node in self.id_to_node.values() if any(sub in node.subject for sub in subjects)]

    
    def find_nodes_by_embedding_key(self, focal_points):
        # 임베딩 키를 기준으로 노드를 찾는다
        # 임베딩 키를 기준으로 입력 값이 임베딩 키에 존재한다면 노드에 넣어서 반환
        return [node for node in self.id_to_node.values() if any(point in node.embedding_key for point in focal_points)]

    
    def get_most_recent_node(self):
        if not self.id_to_node:
            return None
        return max(self.id_to_node.values(), key=lambda node: int(node.node_id.split('_')[1]))


    # 해당 키를 가진 노드 중 가장 최근 노드를 찾는다.
    def get_most_recent_node_by_key(self, key):
        if not self.id_to_node:
            return None

        # 주어진 키에 해당하는 노드만 필터링
        matching_nodes = [node for node in self.id_to_node.values() if key in node.node_id]

        # matching_nodes가 비어있지 않은 경우에만 최대값 계산
        if matching_nodes:
            return max(matching_nodes, key=lambda node: int(node.node_id.split('_')[1]))
        else:
            return None


    def save(self, out_json):
        r = dict()
        for count in range(len(self.id_to_node.keys()), 0, -1):
            node_id = f"node_{str(count)}"
            node= self.id_to_node[node_id]

            r[node_id] = dict()
            r[node_id]["node_count"] = node.node_count
            r[node_id]["event_type"] = node.event_type 

            r[node_id]["created"] = node.created.strftime(
                '%Y-%m-%d %H:%M:%S')

            r[node_id]["subject"] = node.subject
            r[node_id]["predicate"] = node.predicate
            r[node_id]["object"] = node.object

            r[node_id]["description"] = node.description
            r[node_id]["embedding_key"] = node.embedding_key

            r[node_id]["curr_chat"] = node.curr_chat
            r[node_id]["thought"] = node.thought
            r[node_id]["poignancy"] = node.poignancy

            r[node_id]['hour_reflect'] = node.hour_reflect

        with open(out_json+"/nodes.json", "w") as outfile:
            json.dump(r, outfile)
    
        with open(out_json+"/embeddings.json", "w") as outfile:
            json.dump(self.embeddings, outfile)                



    def add_action(self, s, p, o, created,
                   description, thought, embedding_pair,
                   curr_chat, poignancy,
                   hour_reflect):
        
        node_count = len(self.id_to_node.keys())+1
        event_type = "action"
        node_id = f"node_{str(node_count)}"
        
        embedding_pair[0] = description +' '+ thought
        node = ConceptNode(node_id, node_count, event_type,
                           s, p, o, created,
                           description, thought, embedding_pair[0], 
                           curr_chat, poignancy,
                           hour_reflect)
        self.id_to_node[node_id] = node 
        self.embeddings[embedding_pair[0]] = embedding_pair[1]
        
        
        return node
        

    def add_chat(self, s, p, o, created,
                   description, thought, embedding_pair,
                   curr_chat, poignancy,
                   hour_reflect):
        
        node_count = len(self.id_to_node.keys())+1
        event_type = "chat"
        node_id = f"node_{str(node_count)}"

        embedding_pair[0] = f"{description} {thought}"

        node = ConceptNode(node_id, node_count, event_type,
                           s, p, o, created,
                           description, embedding_pair[0],
                           curr_chat, thought, poignancy, hour_reflect)
        self.id_to_node[node_id] = node 
        self.embeddings[embedding_pair[0]] = embedding_pair[1] 

        return node              

    # 중간 채팅을 저장함.
    def add_curr_chat_node(self, persona, curr_chat):
        # 'chat' 타입의 노드만 필터링
        chat_nodes = [node for node in persona.a_mem.id_to_node.values() if node.event_type == 'chat']

        # chat_nodes가 비어있지 않은 경우에만 최신 노드 찾기
        if chat_nodes:
            latest_node = max(chat_nodes, key=lambda node: int(node.node_id.split('_')[1]))
            # 최신 노드의 curr_chat 업데이트
            latest_node.curr_chat.append(curr_chat)
            return latest_node
        else:
            return None

    def add_curr_chat(self, chat):
        chat_clean = f"{chat[0]}: {chat[1]}"
        self.curr_chat += [chat_clean]


    def add_chat_without_thought(self, s, p, o,
                    description, embedding_pair,
                    chat, poignancy):

        node_count = len(self.id_to_node.keys()) + 1
        type_count = len(self.seq_event) + 1
        event_type = "chat"
        node_id = f"node_{str(node_count)}"

        node = ConceptNode(node_id, node_count, type_count, event_type,
                    s, p, o, 
                    description, embedding_pair[0], poignancy)
            
        # chat 의 형태는 전체 chat이 들어가야 한다.
        # [["tom", "안녕 반가워"],["horalson":"메롱"]]
        if chat is not None:
            self.chat = chat
        self.embeddings[embedding_pair[0]] = embedding_pair[1]
        
        return node


    def load_relationship(self, target_persona):
        relationship = json.load(open(self.f_saved+ "/relationship.json"))
        print(relationship)
        target_relationship = relationship[f"{target_persona.scratch.name}"]
        return target_relationship

    def load_all_relationship(self, persona):
        relationship = json.load(open(self.f_saved + "/relationship.json"))
        text = ""
        for key, value in relationship.items():
            text += f"{persona.scratch.name} feels that their relationship with {key} is {value}.\n"
        return text


    def save_relationship(self, init_persona, target_persona):
        # focal_points = [f"{target_persona.scratch.name}"]
        retrieved = new_retrieve(init_persona, [target_persona.scratch.name], 50)

        all_embedding_keys = list()
        for key, val in retrieved.items():
            for i in val:
                all_embedding_keys += [i.embedding_key]
            all_embedding_key_str = ""
            for i in all_embedding_keys:
                all_embedding_key_str += f"{i}\n"
        
        summarized_relationship = run_gpt_prompt_agent_chat_summarize_relationship(
                              init_persona, target_persona,
                              all_embedding_key_str)[0]

        self.relationship['target_persona'] = summarized_relationship

        with open(self.f_saved+ "/relationship.json", "w") as outfile:
            json.dump(self.relationship, outfile)
        

    def load_summarize(self, persona):
        daily_summarize = json.load(open(self.f_saved+ "/daily_summarize.json"))

    def save_summarize(self, perosna):
        return None
