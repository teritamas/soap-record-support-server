# soap-record-support-server

## QuickStart

はじめにプロジェクトのルートに`.env`ファイルを用意し、各認証情報を設定します。

```
ENV=dev
HTTP_PORT=8010

LINE_CHANNEL_ACCESS_TOKEN={Lineのチャンネルのアクセストークン}
LINE_CHANNEL_SECRET={Lineのチャンネルのシークレット}

CRED_PATH={Firebaseのサービスアカウントの認証キーを格納したパス}
FIREBASE_DATABASE_URL={FirebaseのデータベースのURL}

COTOHA_CLIENT_ID={CotohaのclientId}
COTOHA_CLIENT_SECRET={Cotohaのsecret}
```

その後、下記のコマンドでアプリケーションを起動します。

```sh
docker-compose up -d
```

下記のURLにswaggerDocsが公開されるので、APIの利用方法を確認してください。

- localhost:8010/docs
