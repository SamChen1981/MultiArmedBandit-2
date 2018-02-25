import argparse

from arm.arm import NormalDistributionArm
from bandit_algorithm.bandit_core import BanditCore
from bandit_algorithm.thompson_sampling import *
from utils.data_processing import calc_mean_log


def main():
    parser = argparse.ArgumentParser(description='Bandit Experiment')

    # setting of experiment
    parser.add_argument('--exp_num', type=int, default=1,
                        help='Number of experiments')
    parser.add_argument('--save_log', action='store_true',
                        help='Whether to save log')
    parser.add_argument('--show_log', action='store_true',
                        help='Whether to show log')
    parser.set_defaults(save_log=False)
    parser.set_defaults(show_log=False)

    args = parser.parse_args()

    # define arms
    arms = [NormalDistributionArm(1.0, 3.0),
            NormalDistributionArm(0.0, 0.3)]

    # define bandit algorithm
    algorithm = ThompsonSamplingGaussianPrior(len(arms))
    # algorithm = ThompsonSamplingGaussianSicqPrior(len(arms))
    arm_name = ''
    for i in range(len(arms)):
        arm_name += arms[i].name()
    save_path_root = '../data/' + arm_name + '/' + algorithm.__class__.__name__
    core = BanditCore(arms, algorithm, args)

    # run experiment
    print('----------Run Exp----------')
    for i in range(args.exp_num):
        print('Run Exp' + str(i))
        # define bandit algorithm
        save_path = save_path_root + '/Exp' + str(i)
        core.experiment(save_path)
        print('Finish Exp' + str(i))
        print('')

    # calculate mean values of log
    if args.save_log:
        print('----------Calc Mean of Log----------')
        calc_mean_log(save_path_root, 'regret')


if __name__ == '__main__':
    main()