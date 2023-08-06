import gym
import ray

from smarts.core.agent import Agent, AgentSpec
from smarts.core.agent_interface import AgentInterface, AgentType


class SimpleAgent(Agent):
    def act(self, obs):
        return "keep_lane"


@ray.remote
class Environment:
    def __init__(self):
        self.AGENT_ID = "Agent-007"
        agent_spec = AgentSpec(
            interface=AgentInterface.from_type(AgentType.Laner, max_episode_steps=1000),
            agent_builder=SimpleAgent,
        )
        self.env = gym.make(
            "smarts.env:hiway-v0",
            scenarios=["scenarios/loop"],
            agent_specs={self.AGENT_ID: agent_spec},
        )
        self.agent = agent_spec.build_agent()

    def sample(self):
        observations = self.env.reset()

        while True:
            agent_action = self.agent.act(observations[self.AGENT_ID])
            observations, reward, done, _ = self.env.step({self.AGENT_ID: agent_action})
            if done[self.AGENT_ID]:
                break

        return 1  # return sampled trajectory

    def destroy(self):
        self.env.close()


def train(trajectory):
    return 0


if __name__ == "__main__":
    cpu = 2
    ray.init(num_cpus=cpu)
    environments = [Environment.remote() for _ in range(cpu)]
    futures = []
    try:
        for i in range(10000):
            futures = [env.sample.remote() for env in environments]
            trajectories = []
            for env, f in zip(environments, futures):
                trajectories.append(ray.get([f]))
            train(trajectories)
            print("Episode:%d" % i)
    finally:
        futures = [env.destroy.remote() for env in environments]
        ray.get(futures)
        ray.shutdown()
