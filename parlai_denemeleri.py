from parlai.core.agents import Agent
from parlai.core.opt import Opt
from parlai.core.params import ParlaiParser
from parlai.core.worlds import create_task


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
        if 'label_candidates' in self.observation:
            print('\n')
            print(len(self.observation['label_candidates']))
            print('\n')
        else:
            '\nNo label candidates: '.join(self.observation['text']).join('\n')

        return self.observation


if __name__ == '__main__':
    parser = ParlaiParser()
    opt = parser.parse_args()
    # opt = ['--task', 'light_dialog']
    # opt = Opt()
    # opt['task'] = 'light_dialog'
    agent = RepeatLabelAgent(opt)
    world = create_task(opt, agent)

    for _ in range(3):
        world.parley()
        for a in world.acts:
            # print the actions from each agent
            print(a)
            if world.epoch_done():
                print('EPOCH DONE')
                break
