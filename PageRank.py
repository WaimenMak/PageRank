# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 21:16:26 2019

@author: Max-Mai
"""

# -*- coding: GBK -*-


from urllib.request import urlopen#用于获取网页
from bs4 import BeautifulSoup#用于解析网页
import numpy as np



        
UN_Page = {'A':['B','C','D'],'B':['A','C'],'C':['D'],'D':[]}
    
def explore(P):
    t_new = []
    html = urlopen(P)
    bsObj = BeautifulSoup(html, 'html.parser')
    t1 = bsObj.find_all('a')
    c = 0
    for t2 in t1:
        t3 = t2.get('href')
        if t3 != None and 'https' in t3 and '.jpg' not in t3 and 'morvanzhou' in t3 and 'twitter' not in t3 and 'api' not in t3 and c<=6:
        # if t3 != None and 'https' in t3 and '.jpg' not in t3  and c <= 6:
            t_new.append(t3)
            c += 1
    return t_new  

def build_mat(P,page_dict = {}):
    href_list = explore(P)
    if len(href_list)==0 and (P not in page_dict.keys()):
        page_dict[P] = href_list
        return page_dict
    elif P in page_dict.keys():
        return page_dict
    page_dict[P] = href_list
    for i in range(len(href_list)):
        build_mat(href_list[i],page_dict)
    return page_dict
        
def build_mat2(P,page_dict = {}):
    href_list = explore2(P,UN_Page)
    if len(href_list)==0 and (P not in page_dict.keys()):
        page_dict[P] = href_list
        return page_dict
    elif P in page_dict.keys():
        return page_dict
    page_dict[P] = href_list

    for i in range(len(href_list)):
        build_mat2(href_list[i],page_dict)

    return page_dict
        
def turn_to_mat(page_dict):
    Page = list(page_dict.keys())
    l = len(page_dict.keys())
    Mat = np.zeros([l,l])
    m = 0
    for key in page_dict.keys():
        for href in page_dict[key]:
            for n in range(l):
                if href == Page[n]:
                    Mat[m][n] = 1
        m += 1
    return Mat

def explore2(P,Page):
    return Page[P]



def PageRank(Graph):
    alpha = 0.85
    iter = 0
    #转化为概率转移矩阵
    row_num = Graph.shape[0]
    v = 1/row_num* np.ones([row_num,1])   #初始迭代向量

    for i in range(row_num):
        sum = np.sum(Graph[:,i])
        if sum != 0:
            for j in range(row_num):
                Graph[j, i] = Graph[j, i]/sum
        else:
            Graph[:, i] = 1/row_num * np.ones([row_num])           #解决deadends
    G = alpha * Graph + (1-alpha)/row_num *np.ones([row_num,row_num]) #平滑处理，解决spidertrap

    while(iter < 200):
        v = np.dot(G,v)
        iter += 1

    return v


if __name__ == "__main__":
    P = 'A'
    #p = explore2(P,Page)
    # P = 'http://www.dgut.edu.cn/'
    p = build_mat2(P)    #网页连接情况
    # p = build_mat(P)
    print(p)
    G = turn_to_mat(p)  #化为邻接矩阵
    print(G.T)
    Rank = PageRank(G.T)
    print(Rank)