#!/usr/bin/env python
# pylint: disable=W0201
import sys
import argparse
import yaml
import numpy as np

# torch
import torch
import torch.nn as nn
import torch.optim as optim


# torchlight
import torchlight as torchlight
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"   # avoid env conflict

import torch.nn.functional as F
class FocalLoss(nn.Module):
    def __init__(self, alpha=1, gamma=2):
        super(FocalLoss, self).__init__()
        self.alpha = alpha
        self.gamma = gamma

    def forward(self, inputs, targets):
        BCE_loss = F.cross_entropy(inputs, targets, reduction='none')
        pt = torch.exp(-BCE_loss)
        F_loss = self.alpha * (1 - pt) ** self.gamma * BCE_loss
        return F_loss.mean()


class Processor():
    """
        Base Processor
    """

    def __init__(self, argv=None):

        self.load_arg(argv)
        self.init_environment()
        self.load_model()
        self.load_weights()
        self.gpu()
        self.load_data()
        self.load_optimizer()



    def load_arg(self, argv=None):
        parser = self.get_parser()

        # load arg form config file
        p = parser.parse_args(argv)
        if p.config is not None:
            # load config file
            with open(p.config, 'r') as f:
                default_arg = yaml.load(f, Loader=yaml.FullLoader)

            # update parser from config file
            key = vars(p).keys()
            for k in default_arg.keys():
                if k not in key:
                    print('Unknown Arguments: {}'.format(k))
                    assert k in key

            parser.set_defaults(**default_arg)

        self.arg = parser.parse_args(argv)

    def load_model(self):
        self.model = self.io.load_model(self.arg.model,
                                        **(self.arg.model_args))

    def load_weights(self):
        if self.arg.weights:
            self.model = self.io.load_weights(self.model, self.arg.weights,
                                              self.arg.ignore_weights)

    def gpu(self):
        # move modules to gpu
        self.model = self.model.to(self.dev)
        for name, value in vars(self).items():
            cls_name = str(value.__class__)
            if cls_name.find('torch.nn.modules') != -1:
                setattr(self, name, value.to(self.dev))

        # model parallel
        if self.arg.use_gpu and len(self.gpus) > 1:
            self.model = nn.DataParallel(self.model, device_ids=self.gpus)


    def init_environment(self):
        self.io = torchlight.IO(
            self.arg.work_dir,
            save_log=self.arg.save_log,
            print_log=self.arg.print_log)
        self.io.save_arg(self.arg)

        # gpu
        if self.arg.use_gpu:
            gpus = torchlight.visible_gpu(self.arg.device)
            torchlight.occupy_gpu(gpus)
            self.gpus = gpus
            self.dev = "cuda:0"
        else:
            self.dev = "cpu"

        self.result = dict()
        self.iter_info = dict()
        self.epoch_info = dict()
        self.meta_info = dict(epoch=0, iter=0)

    def load_optimizer(self):
        self.optimizer = optim.SGD(
                        self.model.parameters(),
                        lr=self.arg.base_lr,
                        momentum=0.9,
                        nesterov=True,
                        weight_decay=0.0001)

    def load_data(self):
        # Feeder = import_class(self.arg.feeder)
        from feeder.feeder import Feeder
        # if 'debug' not in self.arg.train_feeder_args:
        #     self.arg.train_feeder_args['debug'] = self.arg.debug
        self.data_loader = dict()
        # print(dataset.shape)
        # train_dataset = dataset[:35]
        # test_dataset  = dataset[35:]
        if self.arg.phase == 'train':
            self.data_loader['train'] = torch.utils.data.DataLoader(
                dataset = Feeder(phase='train'),
                batch_size=self.arg.batch_size,
                shuffle=True,
                num_workers=0,
                drop_last=False)
        # if self.arg.test_feeder_args:
        self.data_loader['test'] = torch.utils.data.DataLoader(
            dataset = Feeder(phase='test'),
            batch_size=self.arg.test_batch_size,
            shuffle=False,
            num_workers=self.arg.num_worker * torchlight.ngpu(
                self.arg.device))

    def show_epoch_info(self):
        for k, v in self.epoch_info.items():
            self.io.print_log('\t{}: {}'.format(k, v))
        if self.arg.pavi_log:
            self.io.log('train', self.meta_info['iter'], self.epoch_info)

    def show_iter_info(self):
        if self.meta_info['iter'] % self.arg.log_interval == 0:
            info ='\tIter {} Done.'.format(self.meta_info['iter'])
            for k, v in self.iter_info.items():
                if isinstance(v, float):
                    info = info + ' | {}: {:.4f}'.format(k, v)
                else:
                    info = info + ' | {}: {}'.format(k, v)

            self.io.print_log(info)

            if self.arg.pavi_log:
                self.io.log('train', self.meta_info['iter'], self.iter_info)

    # def train(self):
    #     for _ in range(100):
    #         self.iter_info['loss'] = 0
    #         self.show_iter_info()
    #         self.meta_info['iter'] += 1
    #     self.epoch_info['mean loss'] = 0
    #     self.show_epoch_info()

    def train(self):
        # print(len(self.data_loader['train']))
        for batch_idx, (data, label) in enumerate(self.data_loader['train']):
            # get data
            data = data.float().to(self.dev)
            label = label.long().to(self.dev)
            data_train = data.clone()
            output = self.model(data_train)
            # if batch_idx == 0 and epoch == 0:
            #     self.train_writer.add_graph(self.model, output)

            # CE loss
            # loss = self.loss_CE(output, label)
            # Focal Loss
            criterion = FocalLoss(alpha=1, gamma=2)
            loss = criterion(output, label)
            # backward
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

    def test(self):
        # print(len(self.data_loader['train']))
        with torch.no_grad():
            total_correct = 0
            total_samples = 0
            for batch_idx, (data, label) in enumerate(self.data_loader['test']):
                # get data
                data = data.float().to(self.dev)
                label = label.long().to(self.dev)
                data_test = data.clone()
                output = self.model(data_test)

                _, predict_label = torch.max(output.data, 1)
                # if batch_idx == 0 and epoch == 0:
                #     self.train_writer.add_graph(self.model, output)
                print(f"label={label}, predicted label={predict_label}")
                # loss = self.loss_CE(output, label)
                correct = (predict_label == label).sum().item()
                total_correct += correct
                total_samples += label.size(0)
            accuracy = total_correct / total_samples * 100
            print(f'Accuracy: {accuracy:.2f}%')

    def start(self):
        self.io.print_log('Parameters:\n{}\n'.format(str(vars(self.arg))))

        # training phase
        if self.arg.phase == 'train':
            self.loss_CE = nn.CrossEntropyLoss().to(self.dev)
            for epoch in range(self.arg.start_epoch, self.arg.num_epoch):
                self.meta_info['epoch'] = epoch

                # training
                self.io.print_log('Training epoch: {}'.format(epoch))
                output_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                self.model.train()
                self.train()
                self.io.print_log('Done.')

                # save model
                if ((epoch + 1) % self.arg.save_interval == 0) or (
                        epoch + 1 == self.arg.num_epoch):
                    filename = 'epoch{}_model.pt'.format(epoch + 1)
                    self.io.save_model(self.model, filename)

                # evaluation
                if ((epoch + 1) % self.arg.eval_interval == 0) or (
                        epoch + 1 == self.arg.num_epoch):
                    self.io.print_log('Eval epoch: {}'.format(epoch))
                    self.test()
                    self.io.print_log('Done.')
        # test phase
        elif self.arg.phase == 'test':

            # the path of weights must be appointed
            if self.arg.weights is None:
                raise ValueError('Please appoint --weights.')
            self.io.print_log('Model:   {}.'.format(self.arg.model))
            self.io.print_log('Weights: {}.'.format(self.arg.weights))

            # evaluation
            self.io.print_log('Evaluation Start:')
            self.test()
            self.io.print_log('Done.\n')

            # save the output of model
            if self.arg.save_result:
                result_dict = dict(
                    zip(self.data_loader['test'].dataset.sample_name,
                        self.result))
                self.io.save_pkl(result_dict, 'test_result.pkl')

    # @staticmethod
    def get_parser(add_help=False):

        #region arguments yapf: disable
        # parameter priority: command line > config > default
        parser = argparse.ArgumentParser( add_help=add_help, description='Base Processor')

        parser.add_argument('-w', '--work_dir', default='./work_dir/tmp', help='the work folder for storing results')
        parser.add_argument('-c', '--config', default="./config/cfg.yaml", help='path to the configuration file')

        # processor
        parser.add_argument('--phase', default='train', help='must be train or test')
        parser.add_argument('--save_result', type=str2bool, default=False, help='if ture, the output of the model will be stored')
        parser.add_argument('--start_epoch', type=int, default=0, help='start training from which epoch')
        parser.add_argument('--num_epoch', type=int, default=80, help='stop training in which epoch')
        parser.add_argument('--use_gpu', type=str2bool, default=True, help='use GPUs or not')
        parser.add_argument('--device', type=int, default=0, nargs='+', help='the indexes of GPUs for training or testing')

        # visulize and debug
        parser.add_argument('--log_interval', type=int, default=100, help='the interval for printing messages (#iteration)')
        parser.add_argument('--save_interval', type=int, default=10, help='the interval for storing models (#iteration)')
        parser.add_argument('--eval_interval', type=int, default=5, help='the interval for evaluating models (#iteration)')
        parser.add_argument('--save_log', type=str2bool, default=True, help='save logging or not')
        parser.add_argument('--print_log', type=str2bool, default=True, help='print logging or not')
        parser.add_argument('--pavi_log', type=str2bool, default=False, help='logging on pavi or not')

        # feeder
        parser.add_argument('--feeder', default='feeder.feeder', help='data loader will be used')
        parser.add_argument('--num_worker', type=int, default=4, help='the number of worker per gpu for data loader')
        parser.add_argument('--train_feeder_args', default=dict(), help='the arguments of data loader for training')
        parser.add_argument('--test_feeder_args', default=dict(), help='the arguments of data loader for test')
        parser.add_argument('--batch_size', type=int, default=256, help='training batch size')
        parser.add_argument('--test_batch_size', type=int, default=256, help='test batch size')
        parser.add_argument('--debug', action="store_true", help='less data, faster loading')

        # model
        parser.add_argument('--model', default=None, help='the model will be used')
        parser.add_argument('--model_args', default=dict(), help='the arguments of model')
        parser.add_argument('--weights', default=None, help='the weights for network initialization')
        parser.add_argument('--ignore_weights', type=str, default=[], nargs='+', help='the name of weights which will be ignored in the initialization')
        #endregion yapf: enable

        parser.add_argument('--weight_decay', default=0.0001)
        parser.add_argument('--base_lr', default=0.1)
        parser.add_argument('--step', default=[10, 50])


        return parser

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def import_class(name):
    components = name.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


def main():
    # parser = get_parser()

    # # load arg form config file
    # p = parser.parse_args()
    # if p.config is not None:
    #     with open(p.config, 'r') as f:
    #         default_arg = yaml.safe_load(f)
    #     key = vars(p).keys()
    #     for k in default_arg.keys():
    #         if k not in key:
    #             print('WRONG ARG:', k)
    #             assert (k in key)
    #     parser.set_defaults(**default_arg)

    # arg = parser.parse_args()

    processor = Processor()
    processor.start()


if __name__ == '__main__':
    main()