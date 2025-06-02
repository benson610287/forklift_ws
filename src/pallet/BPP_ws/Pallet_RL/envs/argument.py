import argparse

def get_args():
    parser = argparse.ArgumentParser(description='RL_model')
    parser.add_argument('--mode',       default='train',  type=str,
                            help='train | test')

    parser.add_argument('--box_model',  default=1,        type=int, 
                            help='select box model number 1~3')

    parser.add_argument('--bin_model',  default=1,        type=int, 
                            help='select bin model number 1~3')

    parser.add_argument('--load_model', default='12_9',   type=str,
                            help='load model')

    parser.add_argument('--save_model', default='PPO',    type=str,
                            help='save model name')
    
    parser.add_argument('--train_step', default='100000', type=int,
                            help='train step (min=500)')
    
    parser.add_argument('--episode',    default='100',    type=int,
                            help='predict episode')

    args = parser.parse_args()
    return args