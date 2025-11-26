from stable_baselines3 import PPO
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import gym
from Pallet_RL import envs
import os
from Pallet_RL.envs.argument import get_args 

def main(args):

    models_dir = "Pallet_RL/models/PPO"
    logdir = "Pallet_RL/logs"

    if not os.path.exists(models_dir):
        os.makedirs(models_dir)

    if not os.path.exists(logdir):
        os.makedirs(logdir)

    env=gym.make('pallet-v0')

    if args.mode == "train":
        model = PPO("MultiInputPolicy", env, verbose=1,n_steps=500,seed=0, tensorboard_log=logdir)
        # model.learn(total_timesteps=args.train_step, tb_log_name="PPO")

        #get tensor_data
        #tensorboard --logdir=logs

        TIMESTEPS = args.train_step/10
        for i in range (1,7):
            model.load(f"{models_dir}/11_04_{300000+TIMESTEPS*i}")
            model.learn(total_timesteps=TIMESTEPS, tb_log_name="PPO")
            model.save(f"{models_dir}/11_04_{400000+TIMESTEPS*i}")
            model.load(f"{models_dir}/11_04_{400000+TIMESTEPS*i}")
        # plt.subplot(2,1,1)
        model.save(f"{models_dir}/{args.save_model}.pt")

        plt.figure()
        plt.title("Reward", fontsize=24)
        plt.xlabel("episodes",fontsize=14)
        plt.ylabel("Rewards",fontsize=14)
        plt.plot(env.trainreward)
        # plt.subplot(2,1,2)

        plt.figure()
        plt.title("Reward", fontsize=24)
        plt.xlabel("timesteps",fontsize=14)
        plt.ylabel("Rewards",fontsize=14)
        plt.plot(env.step_reward)

        plt.figure()
        plt.title("Space Ratio", fontsize=24)
        plt.plot(env.ratios)
        plt.xlabel("episodes",fontsize=14)
        plt.ylabel("Space ratio",fontsize=14)
        y_major_locator= MultipleLocator(10)
        ax = plt.gca()
        ax.yaxis.set_major_locator(y_major_locator)
        plt.ylim(0, 100)

        plt.figure()
        plt.title("Stack item", fontsize=24)
        plt.xlabel("episodes",fontsize=14)
        plt.ylabel("Item",fontsize=14)
        plt.plot(env.item)

        plt.show()
        del model
    
    elif args.mode == "test":
        model = PPO.load(f"{models_dir}/{args.load_model}")
        obs = env.reset()
        # obs = env.reset()

        episodes = args.episode

        for i in range(episodes):
            obs = env.reset()
            done = False
            while not done:
                action = model.predict(obs)
                obs, reward, done, info = env.step(action[0])
            # if dones:
            #     env.reset()
            env.render()

        plt.figure()
        plt.title("Predict Space Ratio", fontsize=24)
        plt.plot(env.ratios, marker='o', mec='b')
        plt.xlabel("Times",fontsize=14)
        plt.ylabel("Space ratio",fontsize=14)
        y_major_locator=MultipleLocator(10)
        ax = plt.gca()
        ax.yaxis.set_major_locator(y_major_locator)
        plt.ylim(0, 100)


        plt.figure()
        plt.title("Predict Stack item", fontsize=24)
        plt.xlabel("Times",fontsize=14)
        plt.ylabel("Item",fontsize=14)
        plt.plot(env.item, marker='o', mec='b')

        plt.show()
        env.close

if __name__ == '__main__' :
    args = get_args()
    main(args)

# model = PPO.load("PPO_11_05")
# obs = env.reset()
# obs = env.reset()

# while True:
#     action = model.predict(obs)
#     obs, reward, dones, info = env.step(action)
#     if dones:
#         env.reset()
#     env.render()
# while True:
#     action, _states = model.predict(obs)
#     obs, rewards, dones, info = env.step(action)
#     if dones:
#         env.reset()
#     env.render()
