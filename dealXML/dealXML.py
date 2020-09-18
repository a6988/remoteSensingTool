import xml.etree.ElementTree as ET
import os
import datetime as dt
import sys
import json

def extractOpensearch(xmlFile,pickUpName):
    '''
    検索総数、startIndex, itemsPerPageなどOpensearchタグの情報を取得する
    '''

    # xml nameSpaceの定義
    XMLnameSpace = 'http://a9.com/-/spec/opensearch/1.1/'

    # 木構造の取得
    root = ET.parse(xmlFile)

    # 取得したいところを取得
    
    res = root.find('./opensearch:{0}'.format(pickUpName),
            {'opensearch':XMLnameSpace})

    return int(res.text)
    
def getSearchNo(xmlFile):
    '''
    検索の数を取得する
    '''

    # 検索の数を示す全数、開始のインデックス、1ページあたりの数
    thisVars = ['totalResults','startIndex','itemsPerPage']
    thisResults = {}

    for thisVar in thisVars:
        thisResults[thisVar] = extractOpensearch(xmlFile, thisVar)

    return thisResults['totalResults'],thisResults['itemsPerPage']


if __name__ == '__main__':

    xmlFile = 'thistest.xml'
    print(getSearchNo(xmlFile))




