from parlai.core.agents import Agent
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
        reply = {'id': self.id}
        if 'labels' in self.observation:
            reply['text'] = ', '.join(self.observation['labels'])
        else:
            reply['text'] = "I don't know."
        return reply


if __name__ == '__main__':
    parser = ParlaiParser()
    opt = parser.parse_args()

    agent = RepeatLabelAgent(opt)
    world = create_task(opt, agent)

    for _ in range(10):
        world.parley()
        for a in world.acts:
            # print the actions from each agent
            print(a)
            if world.epoch_done():
                print('EPOCH DONE')
                break
