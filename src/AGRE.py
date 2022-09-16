import torch as t
import torch.nn as nn
import torch.optim as optim
import time
import numpy as np
from sklearn.metrics import roc_auc_score, accuracy_score

from src.evaluate import get_all_metrics
from src.load_base import get_records, load_kg


class AGRE(nn.Module):

    def __init__(self, args, n_entity, n_relation):

        super(AGRE, self).__init__()
        self.dim = args.dim
        self.p = args.p
        self.n_relation = n_relation
        self.path_len = args.path_len
        entity_embedding_matrix = t.randn(n_entity, args.dim)
        nn.init.xavier_uniform_(entity_embedding_matrix)
        relation_embedding_matrix = t.randn(n_relation + 1, args.dim)
        nn.init.xavier_uniform_(relation_embedding_matrix)
        self.entity_embedding_matrix = nn.Parameter(entity_embedding_matrix)
        self.relation_embedding_matrix = nn.Parameter(relation_embedding_matrix)

        # AGRE
        self.rnn = nn.RNN(2*args.dim, 2*args.dim, num_layers=1)
        self.weight_predict = nn.Linear(2*args.dim, 1)
        self.weight_path = nn.Parameter(t.randn(args.p, args.p))
        self.weight_attention = nn.Linear(2*args.dim, 1)

        # # # AGRE-r
        # self.rnn = nn.RNN(args.dim, args.dim, num_layers=1)
        # self.weight_predict = nn.Linear(args.dim, 1)
        # self.weight_path = nn.Parameter(t.randn(args.p, args.p))
        # self.weight_attention = nn.Linear(args.dim, 1)

    def forward(self, paths_list, relation_dict):
        '''
        AGRE
        :param paths_list:
        :param relation_dict:
        :return:
        '''

        embeddings_list = self.get_embedding(paths_list, relation_dict)

        embeddings = t.cat(embeddings_list, dim=0)

        h = self.rnn(embeddings)[0][-1]

        h = h.reshape(-1, self.p, 2*self.dim)
        h = t.relu(t.matmul(self.weight_path, h))
        #
        # attention
        attention = t.relu(self.weight_attention(h))  # (batch_size, p, 1)
        attention = t.softmax(attention, dim=1)
        final_hidden_states = (attention * h).sum(dim=1)

        #
        # # no attention
        # final_hidden_states = h.mean(dim=1)
        #
        predicts = t.sigmoid(self.weight_predict(final_hidden_states).reshape(-1))

        return predicts

    def get_embedding(self, paths_list, relation_dict):
        '''
        AGRE
        :param paths_list:
        :param relation_dict:
        :return:
        '''

        embeddings_list = []
        zeros = t.zeros(self.p, self.dim)
        if t.cuda.is_available():
            zeros = zeros.to(self.entity_embedding_matrix.data.device)

        for i in range(self.path_len+1):
            # i_relation_entity_embedding_list = []
            i_entity_embedding_list = []
            i_relation_embedding_list = []
            for paths in paths_list:

                if len(paths) == 0:
                    i_entity_embedding_list.append(zeros)
                    i_relation_embedding_list.append(zeros)
                    continue

                if i == self.path_len:
                    relation_embeddings = self.relation_embedding_matrix[[self.n_relation for path in paths]]
                else:
                    relation_embeddings = self.relation_embedding_matrix[[relation_dict[(path[i], path[i+1])] for path in paths]]

                entity_embeddings = self.entity_embedding_matrix[[path[i] for path in paths]]
                i_relation_embedding_list.append(relation_embeddings)
                i_entity_embedding_list.append(entity_embeddings)
            # (1, batch_size * p, 2*dim)

            relations_embeddings = t.cat(i_relation_embedding_list, dim=0)
            entities_embeddings = t.cat(i_entity_embedding_list, dim=0)
            embeddings = t.cat([entities_embeddings, relations_embeddings], dim=-1).reshape(1, -1, 2 * self.dim)
            embeddings_list.append(embeddings)
            # embeddings_list.append(entities_embeddings.reshape(1, -1, self.dim))
    #
        return embeddings_list
    #
    # def forward(self, paths_list, relation_dict):
    #     '''
    #     AGRE-r
    #     :param paths_list:
    #     :param relation_dict:
    #     :return:
    #     '''
    #
    #     embeddings_list = self.get_embedding(paths_list, relation_dict)
    #     embeddings = t.cat(embeddings_list, dim=0)
    #     h = self.rnn(embeddings)[0][-1]
    #     h = h.reshape(-1, self.p, self.dim)
    #     h = t.relu(t.matmul(self.weight_path, h))
    #     h = h.reshape(-1, self.p, self.dim)
    #     attention = t.relu(self.weight_attention(h))  # (batch_size, p, 1)
    #     attention = t.softmax(attention, dim=1)
    #     final_hidden_states = (attention * h).sum(dim=1)
    #
    #     predicts = t.sigmoid(self.weight_predict(final_hidden_states).reshape(-1))
    #
    #     return predicts
    #
    # def get_embedding(self, paths_list, relation_dict):
    #     '''
    #     AGRE-r
    #     :param paths_list:
    #     :param relation_dict:
    #     :return:
    #     '''
    #
    #     embeddings_list = []
    #     for i in range(self.path_len+1):
    #         i_entity_list = []
    #
    #         for paths in paths_list:
    #
    #             i_entity_list.extend([path[i] for path in paths])
    #
    #         embeddings_list.append(self.entity_embedding_matrix[i_entity_list].reshape(1, -1, self.dim))
    #
    #     return embeddings_list


def get_scores(model, rec, paths_dict, relation_dict, p):
    scores = {}
    model.eval()
    for user in (rec):

        pairs = [(user, item, -1) for item in rec[user]]
        paths_list, _, users, items = get_data(pairs, paths_dict, p)

        predict_list = model(paths_list, relation_dict).cpu().detach().numpy().tolist()

        item_scores = dict()
        i = 0
        for item in rec[user]:

            item_scores[item] = predict_list[i]
            i += 1

        sorted_item_scores = sorted(item_scores.items(), key=lambda x: x[1], reverse=True)
        scores[user] = [i[0] for i in sorted_item_scores]
    model.train()
    return scores


def eval_ctr(model, pairs, paths_dict, args, relation_dict):

    model.eval()
    pred_label = []
    paths_list, true_label, users, items = get_data(pairs, paths_dict, args.p)
    for i in range(0, len(pairs), args.batch_size):
        predicts = model(paths_list[i: i+args.batch_size], relation_dict)
        pred_label.extend(predicts.cpu().detach().numpy().tolist())
    model.train()

    true_label = [pair[2] for pair in pairs]
    auc = roc_auc_score(true_label, pred_label)

    pred_np  = np.array(pred_label)
    pred_np[pred_np >= 0.5] = 1
    pred_np[pred_np < 0.5] = 0
    pred_label = pred_np.tolist()
    acc = accuracy_score(true_label, pred_label)
    return round(auc, 3), round(acc, 3)


def get_data(pairs, paths_dict, p):
    paths_list = []
    label_list = []
    users = []
    items = []
    for pair in pairs:
        if len(paths_dict[(pair[0], pair[1])]):
            paths = paths_dict[(pair[0], pair[1])]
            users.append(pair[0])
            items.append(pair[1])
            if len(paths) >= p:
                indices = np.random.choice(len(paths), p, replace=False)
            else:
                indices = np.random.choice(len(paths), p, replace=True)

            paths_list.append([paths[i] for i in indices])
        else:
            paths_list.append([])

        label_list.append(pair[2])
    return paths_list, label_list, users, items


def train(args, is_topk=False):
    np.random.seed(555)
    data_dir = './data/' + args.dataset + '/'
    train_set = np.load(data_dir + str(args.ratio) + '_train_set.npy').tolist()
    eval_set = np.load(data_dir + str(args.ratio) + '_eval_set.npy').tolist()
    test_set = np.load(data_dir + str(args.ratio) + '_test_set.npy').tolist()
    test_records = get_records(test_set)
    entity_list = np.load(data_dir + '_entity_list.npy').tolist()
    relation_dict = np.load(data_dir + str(args.ratio) + '_relation_dict.npy', allow_pickle=True).item()
    _, _, n_relation = load_kg(data_dir)
    n_entity = len(entity_list)
    rec = np.load(data_dir + str(args.ratio) + '_rec.npy', allow_pickle=True).item()
    paths_dict = np.load(data_dir + str(args.ratio) + '_3_path_dict.npy', allow_pickle=True).item()

    model = AGRE(args, n_entity, n_relation+2)

    if t.cuda.is_available():
        model = model.to(args.device)

    optimizer = optim.Adam(model.parameters(), lr=args.lr, weight_decay=args.l2)
    criterion = nn.BCELoss()

    print(args.dataset + '-----------------------------------------')
    print('dim: %d' % args.dim, end=', ')
    print('p: %d' % args.p, end=', ')
    print('lr: %1.0e' % args.lr, end=', ')
    print('l2: %1.0e' % args.l2, end=', ')
    print('batch_size: %d' % args.batch_size)

    train_auc_list = []
    train_acc_list = []
    eval_auc_list = []
    eval_acc_list = []
    test_auc_list = []
    test_acc_list = []
    all_precision_list = []

    for epoch in range(args.epochs):
        loss_sum = 0
        start = time.clock()
        np.random.shuffle(train_set)
        paths, true_label, users, items = get_data(train_set, paths_dict, args.p)
        # print(len(train_set), len(paths))
        labels = t.tensor(true_label).float()
        if t.cuda.is_available():
            labels = labels.to(args.device)
        start_index = 0
        size = len(paths)
        model.train()
        while start_index < size:

            predicts = model(paths[start_index: start_index + args.batch_size],
                             relation_dict)
            loss = criterion(predicts, labels[start_index: start_index + args.batch_size])
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            loss_sum += loss.cpu().item()

            start_index += args.batch_size

        train_auc, train_acc = eval_ctr(model, train_set, paths_dict, args, relation_dict)
        eval_auc, eval_acc = eval_ctr(model, eval_set, paths_dict, args, relation_dict)
        test_auc, test_acc = eval_ctr(model, test_set, paths_dict, args, relation_dict)

        print('epoch: %d \t train_auc: %.3f \t train_acc: %.3f \t '
              'eval_auc: %.3f \t eval_acc: %.3f \t test_auc: %.3f \t test_acc: %.3f \t' %
              ((epoch + 1), train_auc, train_acc, eval_auc, eval_acc, test_auc, test_acc), end='\t')

        precision_list = []
        if is_topk:
            scores = get_scores(model, rec, paths_dict, relation_dict, args.p)
            precision_list = get_all_metrics(scores, test_records)[0]
            print(precision_list, end='\t')

        train_auc_list.append(train_auc)
        train_acc_list.append(train_acc)
        eval_auc_list.append(eval_auc)
        eval_acc_list.append(eval_acc)
        test_auc_list.append(test_auc)
        test_acc_list.append(test_acc)
        all_precision_list.append(precision_list)
        end = time.clock()
        print('time: %d' % (end - start))

    indices = eval_auc_list.index(max(eval_auc_list))
    print(args.dataset, end='\t')
    print('train_auc: %.3f \t train_acc: %.3f \t eval_auc: %.3f \t eval_acc: %.3f \t '
          'test_auc: %.3f \t test_acc: %.3f \t' %
          (train_auc_list[indices], train_acc_list[indices], eval_auc_list[indices], eval_acc_list[indices],
           test_auc_list[indices], test_acc_list[indices]), end='\t')

    print(all_precision_list[indices])

    return eval_auc_list[indices], eval_acc_list[indices], test_auc_list[indices], test_acc_list[indices]



