from parlai.core.agents import Agent
from parlai.core.opt import Opt
from parlai.core.params import ParlaiParser
from parlai.core.worlds import create_task
from parlai.scripts.display_data import DisplayData

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
    parser = ParlaiParser()
    # opt = parser.parse_args()
    # print(opt)
    # opt = ['--task', 'light_dialog']
    opt = Opt().load('./parlai_settings/parlai_opt_file')
    opt['datapath'] = "/home/eyildiz/projects/socially-aware-dialogue-system/venv/lib/python3.8/site-packages/data"
    opt['num_examples'] = 20
    agent = RepeatLabelAgent(opt)
    # opt.save('parlai_opt_file')

    DisplayData.main(task='light_dialog', num_examples=5)

    world = create_task(opt, agent)
    world.display()

    for _ in range(30):
        pass
        # for a in world.acts:
        #     # print the actions from each agent
        #     if 'text' in a:
        #         print(a['text'])
        #         print('yo')
        #     if world.epoch_done():
        #         print('EPOCH DONE')
        #         break
