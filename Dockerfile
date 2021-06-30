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

# del ssh for heroku
# ## ssh
# # MY_SSH_PASSWDはdocker build時に--build-arg オプションで指定
# ARG MY_SSH_PASSWD
# ENV SSH_PASSWD ${MY_SSH_PASSWD}
# RUN apt-get update \
#         && apt-get install -y --no-install-recommends dialog \
#         && apt-get update \
#         && apt-get install -y --no-install-recommends openssh-server \
#         && echo "$SSH_PASSWD" | chpasswd
# COPY sshd_config /etc/ssh/
COPY init.sh /usr/local/bin/

RUN chmod u+x /usr/local/bin/init.sh

# ENTRYPOINT はコンテナが実行するファイルを設定します。
ENTRYPOINT ["init.sh"]
#SHELL ["/bin/bash", "-c"] # 開発・デバッグ用。コンテナ起動時にWebアプリを起動しないので注意。
