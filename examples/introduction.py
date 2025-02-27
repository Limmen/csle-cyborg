from csle_cyborg.agents.simple_agents.b_line import B_lineAgent
from csle_cyborg.agents.simple_agents.green_agent import GreenAgent
from csle_cyborg.agents.simple_agents.blue_monitor_agent import BlueMonitorAgent
from csle_cyborg.agents.wrappers.challenge_wrapper import ChallengeWrapper
from csle_cyborg.main import Main
import inspect

if __name__ == '__main__':
    path = str(inspect.getfile(Main))
    path = path[:-7] + '/shared/scenarios/Scenario2.yaml'
    env = Main(path, 'sim')
    results = env.reset(agent='Red')
    obs = results.observation
    print(obs)
    action_space = results.action_space
    print(list(action_space.keys()))
    agent = B_lineAgent()
    action = agent.get_action(obs,action_space)
    results = env.step(agent='Red',action=action)
    print(results.observation)
    print(76*'-')
    print(results.action)
    print(76*'-')
    print(results.done)
    agents = {
        'Red': B_lineAgent,
        'Green': GreenAgent
    }

    env = Main(path,'sim',agents=agents)

    results = env.reset(agent='Blue')
    obs = results.observation
    action_space = results.action_space
    agent = BlueMonitorAgent()

    for step in range(20):
        action = agent.get_action(obs,action_space=action_space)
        results = env.step(agent='Blue',action=action)
        obs = results.observation
        reward = results.reward
        print(reward)

    cyborg = Main(path,'sim',agents=agents)
    env = ChallengeWrapper(env=cyborg,agent_name='Blue')
    obs = env.reset()
    print(obs)
    action = 0

    obs, reward, done, info = env.step(action)

    print(obs)
    print(76*'-')
    print(reward)
    print(76*'-')
    print(done)
    print(76*'-')
    print(info)