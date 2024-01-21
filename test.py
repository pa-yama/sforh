print("hello")


#よく使うコマンドを下記にコメントとして記載しておきます。

#仮想環境有効化コマンド
#C:\Users\kanat\env\Scripts\activate

#ランサーバーコマンド
#python manage.py runserver

#管理画面で仕様するユーザーを作成
#python manage.py createsuperuser

#DBのテーブルの設計図を作るコマンド
#python manage.py makemigrations

#DBのテーブルの設計図からテーブルを作成するコマンド
#python manage.py migrate


#マイグレーション状況を確認する。
#python manage.py showmigrations SforH


#下記は参考

#djangoプロジェクトを作成する。
#django-admin startproject config

#djangoアプリを作成する。
#python manage.py startapp SforH


#git練習のためにコメント追加


#reactサーバの起動
#npm start

#nodemoduleの追加
#npm i 



#npm ビルド
#npm run build



#react-scripts build

#webpack利用
#webpack --mode production


#うまくいったパターン
#webpack --config webpack.config.js

'''
module.exports = {
  mode: 'production',
  
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader"
        }
      }
    ]
  }
};


'''