# -*- coding: utf-8 -*-
#  pip install torch==1.7.0+cpu torchvision==0.8.1+cpu torchaudio===0.7.0 -f https://download.pytorch.org/whl/torch_stable.html 成功
#  pip install transformers==4.13.0 -i https://pypi.tuna.tsinghua.edu.cn/simple 
#  pip install --upgrade nni --ignore-installed -i https://pypi.tuna.tsinghua.edu.cn/simple 
#  pip install tkinter -i https://pypi.tuna.tsinghua.edu.cn/simple
#  pip install tensorboard -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn

from sklearn.metrics import f1_score
import torch
from torch import nn
from torch import optim
import transformers as tfs
import math
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
import numpy as np
import pandas as pd
from sklearn.metrics import f1_score
import warnings
import re
from transformers import BertTokenizer, BertModel
from transformers import BertConfig
from transformers import AutoTokenizer, AutoModel,AutoConfig
warnings.filterwarnings('ignore')
from tqdm import tqdm
from sklearn.model_selection import train_test_split
from collections import Counter
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
plt.rcParams["font.sans-serif"] = ['Simhei']
plt.rcParams["axes.unicode_minus"] = False
from pylab import *
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
import torch.optim as optim
from torch.utils.tensorboard.writer import SummaryWriter
from torch.utils.data import random_split
from sklearn.model_selection import train_test_split
from tqdm import tqdm

def data_process():
    data=pd.read_csv(" ",encoding='utf-8') #datasets
    # print(data.columns)
    data_sorce=data['content'].values
    data_label=data['classification'].values

    train_text_data_0=[]
    train_text_data_1=[]
    train_text_data__1=[]

    train_text_data_1_label=[]
    train_text_data_0_label=[]
    train_text_data__1_label=[]

    sum_idx = 0# 
    for idx,line in enumerate(data_sorce):
        if str(data_label[idx])=='0':
            if len(train_text_data_0)<11800:
                line1=re.findall(u'[\u4e00-\u9fa5]',str(line))
                if len(line1)>20:
                    sum_idx+=1
                    train_text_data_0.append(line)
                    train_text_data_0_label.append(int(data_label[idx])+1)

        if str(data_label[idx]) == '1':
            if len(train_text_data_1)<11800:
                line1 = re.findall(u'[\u4e00-\u9fa5]', str(line))
                if len(line1) > 20:
                        sum_idx += 1
                        train_text_data_1.append(line)
                        train_text_data_1_label.append(int(data_label[idx])+1)

        if str(data_label[idx]) == '-1':
            if len(train_text_data__1)<11800:
                line1 = re.findall(u'[\u4e00-\u9fa5]', str(line))
                if len(line1) > 20:
                        sum_idx += 1
                        train_text_data__1.append(line)
                        train_text_data__1_label.append(int(data_label[idx])+1)

        if sum_idx==35000:
                break
    train_text_data=train_text_data_0+train_text_data_1+train_text_data__1
    train_text_data_label=train_text_data_0_label+train_text_data_1_label+train_text_data__1_label

    train_y=[]
    train_x=[]
    for idx ,line in enumerate(train_text_data):
        if len(str(line))>5:
            train_x.append(line)
            train_y.append(train_text_data_label[idx])
    return train_text_data,train_text_data_label

train_text_data,train_text_data_label=data_process()


x_train, x_test, y_train, y_test = train_test_split(train_text_data,train_text_data_label, test_size=0.2, random_state=23)# 23

print(len(x_train))
print(len(x_test))
print(x_train[:3])

def read_batch_data(act, end):
    batch_train_inputs = x_train[act:end]
    batch_train_targets = y_train[int(act):int(end)]
    return batch_train_inputs, batch_train_targets

def test_read_batch_data(act, end):
    batch_test_inputs = x_test[act:end]
    batch_test_targets = y_test[int(act):int(end)]
    return batch_test_inputs, batch_test_targets

class BertClassificationModel(nn.Module):
    def __init__(self):
        super(BertClassificationModel, self).__init__()
        config = BertConfig.from_json_file('chinese_wwm_pytorch/bert_config.json')
        config.output_hidden_states = True
        config.output_attentions = True
        self.bert = BertModel.from_pretrained('chinese_wwm_pytorch', config=config)
        self.dense = nn.Linear(768,3)
        self.softmax=nn.Softmax()

    def forward(self, input_ids, attention_mask):
        bert_output = self.bert(input_ids, attention_mask=attention_mask)
        bert_cls_hidden_state = bert_output[0][:, 0, :]  # 
        linear_output = self.dense(bert_cls_hidden_state)
        return self.softmax(linear_output)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

epochs = 20 # 5 10 20
batch_size=16 # 8 16 32 64 #

bert_classifier_model = BertClassificationModel().to(device)
optimizer = torch.optim.ASGD(bert_classifier_model.parameters(), lr=0.01)

criterion = torch.nn.CrossEntropyLoss()  
criterion.to(device)
tokenizer = BertTokenizer('chinese_wwm_pytorch/vocab.txt')
best_acc=-1
def test(temp_model, batch_size):
    with torch.no_grad():
        y_pred = []
        y_true = []
        for i in range(0,4990, batch_size):  #4990 5000
            test_inputs, test_targets = test_read_batch_data(i, i + batch_size)
            labels = torch.tensor(test_targets).to(device)
            batch_tokenized = tokenizer.batch_encode_plus(test_inputs, truncation=True,pad_to_max_length=True,max_length=512)
            input_ids = torch.tensor(batch_tokenized['input_ids']).to(device)
            attention_mask = torch.tensor(batch_tokenized['attention_mask']).to(device)
            outputs = temp_model(input_ids, attention_mask)
            outputs = outputs.cpu().numpy()
            # print("outputs ",outputs )
            for t in np.array(outputs):
                t = np.argmax(t)
                y_pred.append(t)
            for ii in test_targets:
                y_true.append(ii)

        f1_s = f1_score(y_true, y_pred, average='macro')
        print("f1_score-", f1_s)
        Acc = accuracy_score(y_true, y_pred)
        print("Acc-", Acc)
    return Acc

for epoch in tqdm(range(epochs)):
    print("第", epoch, "个epoch")
    epoch_loss=[]
    for i in tqdm(range(1,29990, batch_size)):#  29990  30000
        inputs, targets = read_batch_data(i, i + batch_size)  
        labels = torch.tensor(targets).to(device)
        # inputs = torch.tensor(inputs).to(device)
        batch_tokenized = tokenizer.batch_encode_plus(inputs, truncation=True,pad_to_max_length=True,max_length=512)
        input_ids = torch.tensor(batch_tokenized['input_ids']).to(device)
        attention_mask = torch.tensor(batch_tokenized['attention_mask']).to(device)
        optimizer.zero_grad()
        outputs = bert_classifier_model(input_ids, attention_mask)
        loss = criterion(outputs, labels)
        print("loss",loss)
        epoch_loss.append(loss.item())
        loss.backward()
        optimizer.step()
    print("epoch_loss",np.mean(epoch_loss))
    test_acc=test(bert_classifier_model,batch_size)
    if test_acc>best_acc:
        best_acc=test_acc
        best_model=bert_classifier_model
        print("bset_acc-------------------------------------------------",best_acc)
        torch.save(best_model.state_dict(), 'best_TNEWStrainModel.pth')

model = BertClassificationModel()
model.load_state_dict(torch.load('best_TNEWStrainModel.pth'))
model.to(device)
model.eval()
y_pred = []
y_true = []
with torch.no_grad():
    for i in range(0,4990, batch_size):  #4990 5000
        test_inputs, test_targets = test_read_batch_data(i, i + batch_size)
        labels = torch.tensor(test_targets).to(device)
        batch_tokenized = tokenizer.batch_encode_plus(test_inputs, truncation=True,pad_to_max_length=True,max_length=512)
        input_ids = torch.tensor(batch_tokenized['input_ids']).to(device)
        attention_mask = torch.tensor(batch_tokenized['attention_mask']).to(device)

        outputs = model(input_ids, attention_mask)
        outputs = outputs.cpu().numpy()
        for t in np.array(outputs):
            t = np.argmax(t)
            y_pred.append(t)
        for ii in test_targets:
            y_true.append(ii)

Acc = accuracy_score(y_true, y_pred)
print("Acc",Acc)
Fa = f1_score(y_true, y_pred, average='macro')
print("Fa", Fa)

