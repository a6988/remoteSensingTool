import xml.etree.ElementTree as ET
import os
import datetime as dt
import sys
import json
import dealXML.dealXML
import pandas as pd

# 1ページの検索総数の設定(100が最大)
SEARCHMAX = 100

def makeSearchXML(settings:dict):
    '''
    検索ワードを指定し、検索結果が記載されたxmlファイルを取得する
    '''

    ## 検索開始時期(datetime型に変換)
    beginDate = dt.datetime.strptime(settings['beginDate'],'%Y-%m-%d')
    endDate = dt.datetime.strptime(settings['endDate'],'%Y-%m-%d')

    ## 緯度経度
    lats = settings['lats'].split(',')
    lons = settings['lons'].split(',')
    lats = [ float(x) for x in lats]
    lons = [ float(x) for x in lons]

    # beginpositionのformatを整える
    ## beginDate, endDateはdatetime.datetime型
    if type(beginDate) is dt.datetime and type(endDate) is dt.datetime:
        beginOfBEGINPOSTION = beginDate.isoformat(timespec='milliseconds') + 'Z'
        endOfBEGINPOSTION = endDate.isoformat(timespec='milliseconds') + 'Z'

        thisBEGINPOSTION = 'beginposition:[{0} TO {1}]'.format(
                beginOfBEGINPOSTION, endOfBEGINPOSTION)
    else:
        print("beginDateとendDateはdatetime型で与えてください")
        sys.exit()


    # 位置座標のformatを整える
    ## 入力を数値だけでしている場合、リストに変換する
    if type(lats) != list:
        lats = [lats]
    if type(lons) != list:
        lons = [lons]

    ## 緯度と経度の指定数の一致の確認
    if len(lats) != len(lons):
        print("緯度と経度の数が合っていません")
        sys.exit()

    ## 一つの組の場合はpoint、二つ以上はpolygon
    if len(lats) == 1:
        thisFOOTPRINT='footprint:\\"Intersects({0},{1})\\"'.format(lats[0], lons[0])
    else:

        # POLYGONの座標指定を作成
        thisPOLYGON = ""
        for thisLat, thisLon in zip(lats, lons):
            thisPOLYGON += str(thisLon) + " " + str(thisLat) + ","
        ## 最初と最後の座標を一致させる
        thisPOLYGON += str(lons[0]) + " " + str(lats[0])

        thisFOOTPRINT='footprint:\\"Intersects(POLYGON(({0})))\\"'.format(thisPOLYGON)

    # filenameの指定
    ## Sentinel2用に今は設定しているので、他のものを行う時は変更する必要あるかも。
    searchFilename = settings['searchFilename']
    thisFILENAME = 'filename:{0}'.format(searchFilename)

    # searchコマンドの作成
    searchCommand = thisBEGINPOSTION + " AND " + thisFOOTPRINT + " AND " + \
            thisFILENAME

    print(searchCommand)

    return searchCommand

def wgetXMLDownload(settings:dict,searchResultXML,thisLoopNo, itemPerPages):
    '''
    検索文に基づいた検索結果をXMLで取得
    '''

    # TODO CODAREPのアドレスは更新すること。
    accessSites={'OAH': 'https://scihub.copernicus.eu/dhus/search', #open Access Hub
            'CODA': 'https://coda.eumetsat.int/search', # Copernicus Open Access Hub
            'CODAREP':'hoge'}# Copernicus Open Access Hub Reprocessed

    # 設定の読取
    dataBaseName = settings['dataBase']                 # accessサイト名
    outputFileName = '{:0>3}_'.format(thisLoopNo) + settings['outputXML'] # 出力ファイル名
    userId = settings['userId']         # userId
    password = settings['password']     # パスワード

    # 今回のアクセスサイト
    accessSite = accessSites[dataBaseName]

    # 検索オプションとクエリ文開始記号の追加 
    ## 検索総数の指定、検索表示ページ番号の指定、クエリ文開始部分の追加
    thisStartNo = thisLoopNo * itemPerPages
    accessSite += '?rows={0}&start={1}&q='.format(SEARCHMAX,thisStartNo)
    ## 検索表示ページ番号の指定

    # 検索結果の取得
    thisExec = 'wget --user={1} --password={2} --no-check-certificate "{0}{3}" -O ./download/{4}'.format(accessSite, userId,password,searchResultXML,
            outputFileName)
    
    print(thisExec)
    os.system(thisExec)

    return
def parseAddress(xmlFile):
    '''
    xmlFileからダウンロードアドレスを抜き出す
    '''
    
    # 木構造の取得
    root = ET.parse(xmlFile)

    # entryという名前の要素を取得
    entries = root.findall('{http://www.w3.org/2005/Atom}entry')

    # entryの中のlinkの要素を取得
    # link要素は3つあるが、その内relがNoneのものにアドレスが格納されている。
    thisLinks = []
    thisTitles = []
    for entry in entries:

        # title(filenameとする)を取得
        thisTitle = entry.find('{http://www.w3.org/2005/Atom}title')
        thisTitles.append(thisTitle.text)

        # linkの取得
        for thisLink in entry.findall('{http://www.w3.org/2005/Atom}link'):
            if thisLink.get('rel') == None:
                thisLinks.append(thisLink.get('href'))

    return thisTitles, thisLinks



def wgetFileDownload(title, downloadLink, settings):
    '''
    wgetによるダウンロード
    '''

    # 設定の読み込み
    userId = settings['userId']         # userId
    password = settings['password']     # パスワード
    debugFlag = settings['debugFlag']   # デバッグにするかどうか

    # debugモード(dryrun)のオプションを追加するかどうか
    if debugFlag == True:
        dryrunOpt = '--spider'
    else:
        dryrunOpt = ''

    thisExec = 'wget --content-disposition --continue --no-check-certificate --user={0} --password={1} "{2}" {3} -O ./download/{4}.zip'.format(userId,password,downloadLink, dryrunOpt, title)
    print(thisExec)

    # Linuxの場合は$をエスケープ
    if os.name == 'posix': # linux系の場合
        thisExec = thisExec.replace('$','\$')
    os.system(thisExec)

    return


def test():

    userId = 'hoge'
    password = 'foo'
    outputFileName = 'test.xml'
    searchXML = "https://coda.eumetsat.int/odata/v1/Products?$filter=year(IngestionDate) eq 2019 and startswith(Name, 'S3A_OL_2_WFR')"
    # 検索結果の取得
    thisExec = 'wget --user={0} --password={1} --no-check-certificate "{2}" -O {3}'.format(userId,password,searchXML, outputFileName)

    print(thisExec)
    os.system(thisExec)

    return


def run(settingJson = 'setting.json'):
    '''
    Open Access Hubからsentinelのデータをダウンロードする
    検索開始・終了時期、検索場所のポイント及びポリゴン指定が可能
    setting.jsonに記載すること
    '''
    
    # 設定ファイルの読み込み
    with open(settingJson, encoding='utf-8') as f:
        settings = json.load(f)

    xmlFile = settings['outputXML']     # 検索結果出力file


    # 指定条件での検索結果をXMLファイルで取得
    ## 検索条件をクエリ化
    searchResultXML = makeSearchXML(settings)

    ## クエリをOpenAccessHubサーバに問い合わせ検索結果をXMLに保存
    wgetXMLDownload(settings,searchResultXML,thisLoopNo=0,itemPerPages=SEARCHMAX)

    ## 検索総数,ページ数などが入った結果数を取得
    ## 最初のファイルから読み出すことにするので'000_'を明示的に付記
    totalResults, itemPerPages = dealXML.dealXML.getSearchNo('./download/' +'000_' + xmlFile)

    ## ループ回数の算出
    loopNo = totalResults // itemPerPages

    # 検索総数分ループしてSEARCHMAXずつファイルを作成
    for thisLoopNo in range(0,loopNo+1):

        wgetXMLDownload(settings, searchResultXML,thisLoopNo, itemPerPages)
       
    # 検索結果XMLを読み込んで結果を取得し、それをdataFrameに格納する
    downloadTargetPd = pd.DataFrame(columns=['title','link'])

    for thisLoopNo in range(0,loopNo+1):
    #for thisLoopNo in range(0,loopNo):
        
        thisXMLFile = './download/' + '{:0>3}_'.format(thisLoopNo) + settings['outputXML']
        thisTitles, thisLinks = parseAddress(thisXMLFile)

        # 上記結果を行方向に一つのDataFrameにする
        tempPd = pd.DataFrame()
        tempPd['title'] = thisTitles
        tempPd['link'] = thisLinks

        downloadTargetPd = downloadTargetPd.append(tempPd)

    downloadTargetPd.index = range(0,len(downloadTargetPd))
    
    # ファイルのダウンロード
    for title, downloadLink in zip(downloadTargetPd['title'],
            downloadTargetPd['link']):
        wgetFileDownload(title, downloadLink, settings)

if __name__ == '__main__':

    run()
    # test()

