from gym.envs.registration import register

register(
        id = 'pallet-v0',
        entry_point='pallet_model.Pallet_RL.envs:Pallet_env')
