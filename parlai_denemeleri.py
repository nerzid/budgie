from parlai.core.agents import Agent
from parlai.core.opt import Opt
from parlai.core.params import ParlaiParser
from parlai.core.worlds import create_task
from parlai.core.worlds import create_task_world
from parlai.scripts.display_data import DisplayData
import spacy

class RepeatLabelAgent(Agent):
    # initialize by setting id
    def __init__(self, opt):
        self.id = 'RepeatLabel'

    # store observation for later, return it unmodified
    def observe(self, observation):
        self.observation = observation
        return observation

    # return label from before if available
    def act(self):
        reply = {'id': self.id}
        if 'labels' in self.observation:
            reply['text'] = ', '.join(self.observation['labels'])
        else:
            reply['text'] = "I don't know."
        return {}


if __name__ == '__main__':
    nlp = spacy.load('en_core_web_sm')
    parser = ParlaiParser()
    # opt = parser.parse_args()
    # print(opt)
    # opt = ['--task', 'light_dialog']
    opt = Opt().load('./parlai_settings/parlai_opt_file.txt')
    opt['datapath'] = "/home/eyildiz/projects/socially-aware-dialogue-system/venv/lib/python3.8/site-packages/data"
    opt['num_examples'] = 20
    agent = RepeatLabelAgent(opt)
    # opt.save('parlai_opt_file')

    # DisplayData.main(task='light_dialog', num_examples=5)

    world = create_task(opt, agent)
    num_of_episodes = 1
    ix = 0
    inf_loop_breaker_limit = 1000
    ix_inf = 0
    while ix < num_of_episodes:
        ix_inf += 1
        if ix_inf >= inf_loop_breaker_limit:
            break
        world.parley()
        # display_str = world.display()ð
        display_str = world.acts[0]['labels'][0]
        tokens = nlp(display_str)

        tag_info = ""
        for token in tokens:
            if 'VB' in token.tag_:
                tag_info += f"{token.text}({token.pos_},{token.tag_}), "
            # print("Text:" + token.text + " POSTag: " + token.pos_ + " Tag: " + token.tag_)
            # print(
            #     f'{token.text:{8}} {token.pos_:{6}} {token.tag_:{6}} {token.dep_:{6}} {spacy.explain(token.pos_):{20}} {spacy.explain(token.tag_)}')
        display_str += f'[{tag_info}]'
        print(display_str)


        if '- - - - - - - END OF EPISODE - - - - - - - - - -' in display_str:
            ix += 1

        # for a in world.acts:
        #     # print the actions from each agent
        #     if 'text' in a:
        #         print(a['text'])
        #         print('yo')
        #     if world.epoch_done():
        #         print('EPOCH DONE')
        #         break
