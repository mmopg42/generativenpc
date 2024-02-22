"""
출처: https://github.com/joonspk-research/generative_agents/blob/main/reverie/backend_server/persona/memory_structures/spatial_memory.py



"""
import json
import sys
# sys.path.append('../../')

# from utils import *
from global_methods import *

class MemoryTree: 
    def __init__(self, f_saved):
        self.tree = {}
        if check_if_file_exists(f_saved):
            self.tree = json.load(open(f_saved))


    def print_tree(self):
        def _print_tree(tree, depth):
            dash = " >" * depth
            if type(tree) == type(list()):
                if tree:
                    print (dash, tree)
                return
            
            for key, val in tree.items():
                if key:
                    print(dash, key)
                _print_tree(val, depth+1)
        _print_tree(self.tree,0)

    def save(self, out_json):
        with open(out_json, "w") as outfile:
            json.dump(self.tree, outfile) 

    def get_str_accessible_sectors(self, curr_world):
        """
        현재 월드에서 페르소나가 접근 가능한 모든 섹터의 요약 문자열을 반환한다

        주의할 점은 페르소나가 들어갈 수 없는 장소도 있다는 것이다. 이 정보는 페르소나 시트에서 제공된다. 이는 함수에서 고려된다.

        INPUT:
            curr_world
        OUTPUT:
            현재 접근 가능한 모든 섹터가 쉼표로 나눠진 목록

        """
        x = ", ".join(list(self.tree[curr_world].keys()))
        return x
    

    def get_str_accessible_sector_arenas(self, sector): 
        """
        현재 섹터에서 접근 가능한 모든 아레나를 반환한다.
        
        INPUT:
            world:sector
        OUTPUT:
            해당 섹터에서 접근 가능한 아레나 목록
        
        """
        curr_world, curr_sector = sector.split(":")
        if not curr_sector: 
            return ""
        x = ", ".join(list(self.tree[curr_world][curr_sector].keys()))
        return x


    def get_str_accessible_arena_game_objects(self, arena):
        """
        해당 아레나에서 접근 가능한 오브젝트 반환
        
        INPUT:
            world:sector:arena 의 문자열
        OUTPUT:
            접근 가능한 오브젝트 목록
        
        """
        curr_world, curr_sector, curr_arena = arena.split(":")

        if not curr_arena: 
            return ""

        try: 
            x = ", ".join(list(self.tree[curr_world][curr_sector][curr_arena]))
        except: 
            x = ", ".join(list(self.tree[curr_world][curr_sector][curr_arena.lower()]))
        return x        
    
    def get_accessible_all_objects_sentence(self, persona):
        location = []
        objects = []
        processed_text = []
        for world, sectors in self.tree.items():
            sector_descriptions = []
            for sector, arenas in sectors.items():
                arena_descriptions = []
                for arena, items in arenas.items():
                    item_list = ", ".join([f"a {item}" for item in items])
                    arena_descriptions.append(f"In the {arena}, there is {item_list}")
                    location.append(arena)
                    objects.append(item_list)
                arena_descriptions_text = " ".join(arena_descriptions)
                sector_descriptions.append(f"Within the {sector}, {persona.scratch.name} can access several location: {', '.join(arenas.keys())}. {arena_descriptions_text}")
            sectors_text = " ".join(sector_descriptions)
            processed_text.append(f"In {world}, {persona.scratch.name} can access {', '.join(sectors.keys())}. {sectors_text}")
        text = " ".join(processed_text)
        text += f'\nLocation: {location}'
        text += f"\nObject: {objects}"
        return text

    # 이전 버전
    # def get_accessible_all_objects_sentence(self,persona):
    #     processed_text = []
    #     for world, sector in self.tree.items():
    #         sector_names = ", ".join([f"the {sector_name}" for sector_name in sector.keys()])
    #         processed_text.append(f"In {world}, {persona.scratch.name} can access {sector_names}.")
    #         for sector, arena in sector.items():
    #             arena_names = ", ".join([f"the {arena_name}" for arena_name in arena.keys()])
    #             processed_text.append(f"Within the {sector}, {persona.scratch.name} can access the {arena_names}.")
    #             for arena_name, items in arena.items():
    #                 item_list = ", ".join([f"the {item_name}" for item_name in items])
    #                 processed_text.append(f"In the {arena_name}, there is a {item_list}.")
    
    #     return " ".join(processed_text)

if __name__ == '__main__':
    pass