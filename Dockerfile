## Dockerfileには、ベースとするDockerイメージに対して実行する内容を記述します。
# FROMで、ベースとするDockerイメージを指定します。
FROM tiangolo/uwsgi-nginx:python3.6

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

COPY init.sh /usr/local/bin/

RUN chmod u+x /usr/local/bin/init.sh

# ENTRYPOINT はコンテナが実行するファイルを設定します。
ENTRYPOINT ["init.sh"]
#SHELL ["/bin/bash", "-c"] # 開発・デバッグ用。コンテナ起動時にWebアプリを起動しないので注意。
