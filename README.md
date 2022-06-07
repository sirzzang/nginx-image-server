# nginx-image-server

 Nginx, FastCGI 스크립트를 이용하여 이미지 업로드, 다운로드, 삭제 기능을 할 수 있도록 구현한 웹 서버


## Start Server

`docker-compose` 명령어를 통해 미디어 서비스 컨테이너를 실행한다. 8888 포트를 통해 미디어 서버 프로세스에 접근할 수 있다.

최초 구동 시, 이미지를 빌드한 후 컨테이너를 실행할 수 있도록 `docker-compose up`에 `--build` 옵션을 추가한 명령어를 입력한다.

```bash
$ cd common
$ cd MediaService
$ docker-compose up --build # 최초 실행 시 --build 옵션 추가
```

기존에 빌드한 이미지가 있는 경우, `docker-compose up`을 통해 실행한다.

```bash
$ cd common
$ cd MediaService
$ docker-compose up
```

### 포트 변경

미디어 서비스 포트를 변경하고 싶은 경우, `.env` 파일의 `MEDIA_PORT` 포트 값을 변경한다.