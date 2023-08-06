from bropoker.envs.env import Env
from bropoker.envs.vec_env import VecEnv
from bropoker.envs.registration import register, make

register(
    env_id='leduc-holdem',
    entry_point='bropoker.envs.leducholdem:LeducholdemEnv'
)

register(
    env_id='limit-holdem',
    entry_point='bropoker.envs.limitholdem:LimitholdemEnv',
)

register(
    env_id='no-limit-holdem',
    entry_point='bropoker.envs.nolimitholdem:NolimitholdemEnv',
)