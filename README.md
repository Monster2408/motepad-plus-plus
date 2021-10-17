# MotePad++
## やることリスト
##### タブ
- [x] タブを閉じるボタン作成
    - タブに×ボタンの画像を設置(右側)
- [ ] タブを大量に生成した際にはみ出た分のタブの表示方法検討
    - 左右矢印設置やプルダウンリスト作成などが想定される
- [ ] ファイル保存時に名前を付けてもタブの名前が新しい名前に変化しない[^1].
##### ショートカット
- [ ] 名前を付けて保存(`Ctrl` + `Alt` + `S`)
- [ ] 上書き保存(`Ctrl` + `S`)
    - パス式ファイルでない場合(新規作成のみ?)には名前を付けて保存を実行する
- [x] 新規作成(`Ctrl` + `N`)
- [x] タブを閉じる(`Ctrl` + `W`)
    - 最後の1つのタブを閉じた場合は`新規文書1`を発行する
##### ツールバー実装
- [x] なぜかアイコンが適応されない問題を修正
- [ ] 新規作成ボタン追加
- [ ] 上書き保存ボタン追加
- [ ] 名前を付けて保存を追加
##### ステータスバーを実装
- [x] ステータスバー自体のフレームを用意
- テキスト入力中に以下のステータスを表示する
    - [ ] 何行目を編集中か
    - [ ] 全体の文字列(空白を除いた文字数)
    - [ ] 文字コードを表示[^2].
##### ファイル保存
- [ ] ファイル未保存時にデータが消えることを留意していない
    - せめて警告出して「はい」で削除，「いいえ」で閉じないとする
- 名前を付けて保存時のタブについて(タブを参照)

[^1]: タブタイトルの変更は`tabWidget.configure(text = 'myNewText')`を使う？
[^2]: 文字コードの指定システムが必須という一番めんどいやつでありんす