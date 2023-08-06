import random
from collections import defaultdict
from xhp_flow.nn.core import  Placeholder
import os,zipfile
from glob import glob
import numpy as np
import shutil

"""
使用拓扑排序找到网络节点的前向计算顺序（反向传播反过来就行）
"""

def toplogical(graph):
    sorted_graph_nodes = []

    while graph:
        all_nodes_have_inputs = set()
        all_nodes_have_outputs = set()

        for have_output_node, have_inputs in graph.items():
            all_nodes_have_outputs.add(have_output_node)  # 包括只有输出的节点 和既有输入又有输出的点
            all_nodes_have_inputs |= set(have_inputs)  # 有输入的点：包括既有输入和输出的点 和只有输入的点（末尾终点）
        need_removed_nodes = all_nodes_have_outputs - all_nodes_have_inputs  # 减去之后留下只有输出的节点

        if need_removed_nodes:
            node = random.choice(list(need_removed_nodes))  # 随机删去一个节点
            visited_next = [node]

            if len(graph) == 1: visited_next += graph[node]  # 当最后删到只留一个有输出的节点
            # 的时候，那么需要把这个节点对应的输出节点也加上，否则会漏掉这个点

            graph.pop(node)
            sorted_graph_nodes += visited_next

            for _, links in graph.items():
                if node in links: links.remove(node)  # 如果删除的节点在别的节点的连接关系内，那么把他从连接关系里删除
        else:
            break

    return sorted_graph_nodes


"""
根据feed_dict和网络节点的初始化结果,建立网络的连接关系
"""



def convert_feed_dict_graph(feed_dict):
    computing_graph = defaultdict(list)

    nodes = [n for n in feed_dict]

    while nodes:
        n = nodes.pop(0)  # 移除列表中的一个元素（默认最后一个元素），并且返回该元素的值

        if isinstance(n, Placeholder):
            n.value = feed_dict[n]
        if n in computing_graph: continue

        for m in n.outputs:
            computing_graph[n].append(m)  # 建立好网络连接关系
            nodes.append(m)

    return computing_graph


"""
根据网络的连接关系，进行拓扑排序。
"""

def toplogical_sort(feed_dict):
    graph = convert_feed_dict_graph(feed_dict)

    return toplogical(graph)


def forward(graph, monitor=False, train=True):
    for node in graph if train else graph[:-1]:
        if monitor: print('forward:{}'.format(node))
        node.forward()


def backward(graph, monitor=False):
    for node in graph[::-1]:
        if monitor: print('backward:{}'.format(node))
        node.backward()

"""
进行前向和反向传播计算
"""
def run_steps(graph_topological_sort_order, monitor=False, train=True):
    if train:
        forward(graph_topological_sort_order, monitor)
        backward(graph_topological_sort_order, monitor)
    else:
        forward(graph_topological_sort_order, monitor, train)


def optimize(graph, learning_rate=1e-2):
    for node in graph:
        if node.is_trainable:
            node.value = node.value.reshape((node.value.shape[0], -1))
            node.gradients[node] = node.gradients[node].reshape((node.gradients[node].shape[0], -1))
            node.value += -1 * node.gradients[node] * learning_rate


def compress(zip_file, input_dir):
    f_zip = zipfile.ZipFile(zip_file, 'w')
    for root, dirs, files in os.walk(input_dir):
        for f in files:
             # 获取文件相对路径，在压缩包内建立相同的目录结构
            abs_path = os.path.join(os.path.join(root, f))
            rel_path = os.path.relpath(abs_path, os.path.dirname(input_dir))
            f_zip.write(abs_path, rel_path, zipfile.ZIP_STORED)

def extract(zip_file,pwd=None):
    if pwd:
        pwd = pwd.encode()
    f_zip = zipfile.ZipFile(zip_file, 'r')
    # 解压所有文件到指定目录
    f_zip.extractall(zip_file.split(".")[0],pwd=pwd)

    #return txt_file


def save_model(save_path,model):

    save_path = save_path.split('.')[0]
    if not os.path.exists(save_path): #如果文件夹不存在，创建一个新的
        os.mkdir(save_path)

    for name, node in vars(model).items():
        if isinstance(node, Placeholder):
            if node.is_trainable:
                np.savetxt("{}/{}.txt".format(save_path,node.name), node.value)
    compress(os.getcwd() + '/{}.zip'.format(save_path), save_path, )
    shutil.rmtree(save_path)


def load_model(load_path,model):

    extract(load_path)
    load_path = load_path.split(".")[0]
    model_path = np.array(glob(load_path+"/*/*"))
    for name, node in vars(model).items():
        if isinstance(node, Placeholder):
            if node.is_trainable:
                for path in model_path:
                    if path.split(".")[0].split("/")[2] == node.name:
                        node.value = np.loadtxt(path)
    shutil.rmtree(load_path)
#load_model("mlp.zip",mlp)