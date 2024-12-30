# 「勉強のためにOpen ID ConectのIDプロバイダー側をDjangoで実装する」サンプルコード
https://kamatimaru.hatenablog.com/entry/2024/12/29/000436

## 起動
```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```
ブラウザで以下のURLにアクセス

```
http://localhost:8000/sample/authorize/?response_type=code&scope=openid%20email&client_id=test&state=abcd&redirect_uri=http://localhost/callback&nonce=efgh
```

## 仮想環境解除
```sh
deactivate
```


## format
```sh
ruff check . --fix && ruff format .
```
