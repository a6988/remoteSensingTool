# Corpernics ダウンロード自動化ツール

## はじめに

このツールはSentinelシリーズのリモートセンシングデータを公開している[Corpernics Open Access Hub]()から、
検索とダウンロードを自動で実行するためのプログラムです。

## 依存関係

* `wget`		: 1.15以上
* `python`	: 3.7.2で動作確認
* `pandas`	: 1.0.5で動作確認

また、Open Access HubおよびCopernicus Online Data Accessのユーザ登録のID、パスワードが必要になります。

## 概要

Sentinel2を始めとするデータは[Open Access Hub](https://scihub.copernicus.eu)からダウンロードできます。
Sentinel3の海色データなどは[Copernicus Online Data Access](https://coda.eumetsat.int/#/home)からダウンロードできます。

上記サイトから検索しデータを手動でダウンロードすることは可能ですが、複数のファイルをダウンロードしたい場合は手間ですので、
本プログラムを作成しました。

このプログラムは、

1. 設定ファイルに記載された情報に基づいて検索文を作成
1. wgetで検索結果をxmlファイルで取得
1. 上記xmlファイルから個別の検索結果のアドレスを取得、ダウンロードの実行

を行います。

pythonでコーディングしており、ダウンロードにはwgetを呼び出すようにしています。


## 使い方

### 実行方法

```
python corpernicsDownload.py
```

ダウンロードされた検索リストのxmlファイル及び各データはフォルダ直下の`download`フォルダに保存されます。
実行前にフォルダを作成しておいて下さい。

### 設定ファイルの記載方法

`settings.json`にJSON形式で設定を記入して下さい。現在以下の項目が設定できます。

|設定ファイル名|説明|
|-------------|-----|
|searchFilename|ダウンロードファイル名の検索方法 <br> ex. Sentinel-2 : `S2*_MSIL2A*` <br> Sentinel-3 : `S3*WRR*` |
|dataBase |	Corpernicus frameworkのdatabase名 <br>Open Access Hub : OAH <br>Copernicus Open Access Hub : CODA |
|beginDate| 検索開始時期(YY-MM-DDで記述)(センサーの取得時期)|
|endDate| 検索終了時期(YY-MM-DDで記述)(センサーの取得時期) |
|lats|場所の緯度(複数点の指定可能。その場合はポリゴンの端点となる。最後に開始地点を指定すること|
|lons|場所の経度|
|userId|Open Access HubもしくはOpen Data Access HubのuserId|
|password|Open Access HubもしくはOpen Data Access Hubのpassword|
|outputXML|	検索結果を格納するXMLファイル名の指定|
|debugFlag|	デバッグ用フラグ。Trueの場合はwgetをドライランして実際にダウンロードしない|

付属のsettings.jsonも御参照下さい。

## 免責

使用について何か問題が発生した場合でも一切責任をとりませんので、ご了承の上お使い下さい。


