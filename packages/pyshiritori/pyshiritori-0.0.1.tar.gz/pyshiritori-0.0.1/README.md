# pyshiritori
　Python でしりとりをするライブラリです。

# ドキュメント
NAME
    pyshiritori
        しりとりのライブラリです。漢字→ひらがなに pykakasi を利用しています、漢字を正しく読めない場合がありますがそのへんはご了承ください

        (例)
        >>> import pyshiritori
        >>> shiritori = pyshiritori.session(pyshiritori.Dict)
        >>> shiritori("りんご")
        (True, '小泉純一郎')
        >>> shiritori("牛")
        (True, '新入生歓迎会')
        >>> shiritori("イカ")
        (True, '関東')
        >>> shiritori("梅")
        (True, '眼')
        >>> shiritori("メダカ")
        (True, '南瓜')
        >>> shiritori("夜間")
        n(False, 0)

Dict がしりとり用の単語集として付属していますが、実際に Bot の一部として同じサーバーにいる方に使っていただいてみて集めたものの一部であり、不完全な部分などが多いかと思います。そのため実際に自分で作成することをおすすめいたします。


FUNCTIONS
    hantei(Str)
        その文字がひらがなかを判定し、ひらがなであれば清音の大きい文字で返します
        ひらがなでなければ、None を返します。

    saigo(mess)
        saigo(mess)
         messの最初の音を清音の大きい文字で返します。

    saisyo(mess)
        saisyo(mess)
         messの最後の音を清音の大きい文字で返します

    session(Dict)
        session(Dict)
        {最初の音を表すひらがなの清音にしたもの (拗音なども「よ」など大きい文字に直したもの) : {単語のset}} を Dict として取ります。Dict はひらがなの大きい清音すべてを含んでいる必要があります。 set_to_dict() を使用して作成することをおすすめします。
        しりとりのセッションの関数を返します。
        しりとりのセッションの関数
          引数
          ・しりとりでのあなたのターンの言葉をかえします
          返り値
          ・(True, ret_str) ret_str がしりとりへの答えです
          ・(False, 0) 「ん」で終わる言葉が送信されました、あなたの負けです (?)
          ・(False, 1) すでに出た言葉がしりとりに使われました
          ・(False, 2) しりとりにつかうのに適切ではない言葉 (記号のみなど) が送られました
          ・(False, 3) しりとりになっていません (前の言葉の最後と送られた言葉の最初の音が一致しません)
          ・(False, 4) 言葉がネタ切れです。私の負けです (?)
        一番最初は「しりとり」なので「り」で始まる言葉を送ってください。
 
    set_to_dict(Set)
        単語を集めた set を session() で使える形式の dict に変えます

# ライセンス
　このライブラリは GNU GPL v3 でライセンスされています。
![GPLv3 logo](https://www.gnu.org/graphics/gplv3-with-text-136x68.png)
