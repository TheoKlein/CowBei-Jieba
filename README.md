# CowBei Jieba
下載指定粉絲專頁的所有貼文並使用[Jieba](https://github.com/fxsjy/jieba)進行斷詞頻率分析後生成文字雲。

建議可以使用 [Virtualenv](https://virtualenv.pypa.io/en/stable/) 隔離不同專案的套件。

Python3 only

## 安裝必須套件
```
$ pip3 install -r requirement.txt
```

## 新增粉絲專頁
在`main.py`第60行新增要分析的粉絲專頁ID數字或ID字串，可一次新增多個。後方需自訂字串作為輸出時的檔案命名。

例如：
```
fanpage = {
    # 'Page ID number or ID string': 'Custom Page Name'
    '576881715763166': '靠北輔大'
} 
```

## 執行程式
```
$ python3 main.py
```

此程式需要藉由Facebook Graph API存取粉絲專頁資料，程式運作時需要輸入Token，請至 `https://developers.facebook.com/tools/explorer` 取得你的個人權杖。

執行後會建立`tmp`資料夾，程式運作產生的資料全部會儲存在這裡。

注意，再次執行程式時，如果`tmp`資料夾存在會先將`tmp`資料夾刪除，若要保留資料請先複製到別處。

## 自訂忽略詞
如果有字詞不想被列入計算的話，可以在`data/ignore_dict.txt`中新增，一行一個詞，存檔後再次執行即可忽略該詞。

## 範例
![靠北輔大](靠北輔大.png)