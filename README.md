# join gdrive

## 背景

ブラウザ版Googleドライブから、ファイルサイズが大きいファイルをダウンロードした際に、分割されたzipファイルとしてダウンロードされてしまう。

例えば、次のファイル構成がGoogleドライブに存在した場合
```
 big_dir
  ├─ dir1
  │  ├─ big_file01
  │  ├─ big_file02
  │  └─ big_file03
  └─ dir2
     ├─ big_file04
     ├─ big_file05
     └─ big_file06
```
ブラウザ版Googleドライブから"big_dir"をダウンロードした場合、以下のように分割されたzipファイルとなる。
```
 big_dir.zip
 big_dir 1.zip
 big_dir 2.zip
 big_dir 3.zip
 big_dir 4.zip
```
これをunzipすると、以下のような構成として手に入る。
```
 big_dir
  └─ dir1
     └─ big_file01
     
 big_dir 1
  └─ dir1
     └─ big_file02
     
 big_dir 2
  └─ dir1
     └─ big_file03
     
 big_dir 3
  └─ dir2
     ├─ big_file04
     └─ big_file05
     
 big_dir 4
  └─ dir2
     └─ big_file06
```

これを元通りに再連結するには手作業の他なく、自動化のスクリプトをPythonで作成した。

## 使い方

`main.py` の再序盤にある `BASE_FILE_PATH` で対象となるディレクトリを指定する。 `OUTPUT_DIR_PATH` で出力先を指定する。

背景にある例で表すと、次のようになる。
この時、連結したいディレクトリをあらかじめひとつのディレクトリにまとめておく。つまり、`big_dir*` ディレクトリは全て `input`ディレクトリに格納している。
```python
BASE_FILE_PATH = "./input"
OUTPUT_DIR_PATH = BASE_FILE_PATH + "./output"
```

記述する必要があるのはその部分だけで、あとは実行すれば連結が行われる。

```bash
$ python main.py
```

## 注意点

ファイルサイズが大きいケースに使用するため、ディスクサイズ超過に注意。このスクリプトはcopy2を使ってファイルのコピーを行っているため、実行前の分割ディレクトリは残ったままとなる。
