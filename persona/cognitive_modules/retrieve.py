"""

"""
import os
current_file_path = os.path.abspath(__file__)
current_file_dir = os.path.dirname(current_file_path)
os.chdir(current_file_dir)

import sys
sys.path.append(current_file_dir)
sys.path.append('../../')

from global_methods import *
from persona.prompt_template.gpt_structure import *
from persona.prompt_template.run_gpt_prompt import *

from numpy import dot
from numpy.linalg import norm

def retrieve(persona, perceived):
    """
    
    """



# 코사인 유사도 반환
def cos_sim(a, b):
    return dot(a, b)/(norm(a)*norm(b))


def normalize_dict_floats(d, target_min, target_max):
    """

    정규화
    """
    min_val = min(val for val in d.values())
    max_val = max(val for val in d.values())
    range_val = max_val - min_val

    if range_val == 0:
        for key, val in d.items():
            d[key] = (target_max - target_min)/2

    else:
        for key, val in d.items():
            d[key] = ((val - min_val) * (target_max - target_min) 
                / range_val + target_min)

    return d


def top_highest_x_values(d, x):
    """
    상위로 정렬
    """

    sorted_items = sorted(d.items(), key=lambda item: item[1], reverse=True)
    top_v = dict(sorted_items[:x])

    return top_v


def extract_recency(persona, nodes):
    """
    최근 정보 순으로 담긴 node
    """
    recency_decay = 0.995
    recency_vals = [recency_decay ** i
                    for i in range(1, len(nodes) + 1)]

    recency_out = dict()
    for count, node in enumerate(nodes):
        recency_out[node.node_id] = recency_vals[count]

    return recency_out


def extract_importance(persona, nodes):
    """
    poignancy 를 사용하여 중요도 점수가 반영된 노드 목록
    """

    importance_out = dict()
    for count, node in enumerate(nodes):
        importance_out[node.node_id] = node.poignancy


    return importance_out


def extract_relevance(persona, nodes, focal_pt):
    """

    """
    focal_embedding = get_embedding(focal_pt)

    relevance_out = dict()
    for count, node in enumerate(nodes):
        node_embedding = persona.a_mem.embeddings[node.embedding_key]
        relevance_out[node.node_id] = cos_sim(node_embedding, focal_embedding)
    return relevance_out


def generate_poignancy(persona, description, event_type):
    return run_prompt_generate_poignancy(persona, description, event_type)

def new_retrieve(persona, focal_points, n_count=30):
    """
    focal_points 와 관련 있는 것들을 retrieve
    """
    retrieved = dict()
    for focal_pt in focal_points:
        """
        
        """
        nodes = []
        for node in persona.a_mem.id_to_node.values():
            nodes.append(node)
        if nodes == []:
            return []
        recency_out =  extract_recency(persona, nodes)
        recency_out = normalize_dict_floats(recency_out, 0, 1)
        importance_out = extract_importance(persona, nodes)
        importance_out = normalize_dict_floats(importance_out, 0, 1)
        relevance_out = extract_relevance(persona, nodes, focal_pt)
        relevance_out = normalize_dict_floats(relevance_out, 0, 1)

        gw = [0.5, 3, 2]
        master_out = dict()
        for key in recency_out.keys():
            master_out[key] = (recency_out[key]*gw[0]
                               +relevance_out[key]*gw[1]
                               +importance_out[key]*gw[2])
            
        master_out = top_highest_x_values(master_out, len(master_out.keys()))
        for key, val in master_out.items():
            print (persona.a_mem.id_to_node[key].embedding_key, val)
            print (persona.scratch.recency_w*recency_out[key]*1, 
                    persona.scratch.relevance_w*relevance_out[key]*1, 
                    persona.scratch.importance_w*importance_out[key]*1)
            

        master_out = top_highest_x_values(master_out, n_count)
        master_nodes = [persona.a_mem.id_to_node[key]
                        for key in list(master_out.keys())]
        
        for n in master_nodes:
            n.last_accessed = persona.scratch.curr_time
        
        retrieved[focal_pt] = master_nodes

    return retrieved
            
        
        
