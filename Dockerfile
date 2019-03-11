## Dockerfileには、ベースとするDockerイメージに対して実行する内容を記述します。
# FROMで、ベースとするDockerイメージを指定します。
FROM kikagaku/handson:v3.0


# RUNは、OSのコマンドを実行する際に使用します。
RUN mkdir /code

# WORKDIR 命令セットは Dockerfile で RUN 、 CMD 、 ENTRYPOINT 、 COPY 、
# ADD 命令実行時の作業ディレクトリ（working directory）を指定します。
WORKDIR /code

# ADD 命令は <ソース> にある新しいファイルやディレクトリをコピー、あるいはリモートの URL からコピーします。
# それから、コンテナ内のファイルシステム上にある 送信先 に指定されたパスに追加します。
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/

## ssh
# ENV 命令は、環境変数 <key> と 値 <value> のセットです。
# 以下のsshパスワードは、今回のDockerイメージのrootユーザで使うもの。
ENV SSH_PASSWD "root:kikagaku"
RUN apt-get update \
        && apt-get install -y --no-install-recommends dialog \
        && apt-get update \
        && apt-get install -y --no-install-recommends openssh-server \
        && echo "$SSH_PASSWD" | chpasswd

COPY sshd_config /etc/ssh/
COPY init.sh /usr/local/bin/

RUN chmod u+x /usr/local/bin/init.sh
# EXPOSE 命令は、特定のネットワーク・ポートをコンテナが実行時にリッスンすることを Docker に伝えます。
EXPOSE 5000 2222

# ENTRYPOINT はコンテナが実行するファイルを設定します。
ENTRYPOINT ["init.sh"]
