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

## API 호출


### POST images/upload

이미지 단건 업로드를 요청한다.

**Request**

- Request Header
  - `Content-Type`: `multipart/form-data`
- Request Body
  - 업로드할 이미지

**Response**

* 정상 처리

  ```json
  {
      "code": 200,
      "message": "File(s) successfully uploaded.",
      "data": {
          "file_name": "bts_jk.gif",
          "file_id": "b7436194d5034bb69767688807393e48"
      }
  }
  ```

* 에러

  * 이미지가 전송되지 않았을 때

    * Body가 비어 있는 경우: Nginx 400 Bad Request
      ```html
      <html>

      <head>
        <title>404 Not Found</title>
      </head>      
      <body>
        <center>
          <h1>404 Not Found</h1>
        </center>
        <hr>
        <center>nginx/1.20.2</center>
      </body>

      </html>
      ```

    * Body가 있으나, File type이 아닌 경우

      ```json
      {
          "code": 400,
          "message": "No file received."
      }
      ```
  
  * 업로드하려는 이미지 파일의 크기가 너무 큰 경우: nginx 413 request too large 에러
    ```html
    <html>

    <head>
      <title>413 Request Entity Too Large</title>
    </head>

    <body>
      <center>
        <h1>413 Request Entity Too Large</h1>
      </center>
      <hr>
      <center>nginx/1.20.2</center>
    </body>

    </html>
    ```
  
  * 여러 건의 이미지가 업로드된 경우

    ```json
    {
        "code": 400,
        "message": "Multiple file upload not allowed."
    }
    ```

  * 업로드된 이미지가 허용되지 않는 확장자인 경우

    ```json
    {
        "code": 400,
        "message": "File extension of file webp_jk.webp not allowed."
    }
    ```



### POST images/upload_many

이미지 다중 업로드를 요청한다.

**Request**

- Request Header
  - `Content-Type`: `multipart/form-data`
- Request Body
  - 업로드할 이미지들

**Response**

* 정상 처리

  ```json
  {
      "code": 200,
      "message": "File(s) successfully uploaded.",
      "data": [
          {
              "file_name": "jpeg_jk3.jpg",
              "file_id": "b3b2bc5b075f434692f71657afbae2c9"
          },
          {
              "file_name": "png_jk.png",
              "file_id": "20995dfcf94a49e7b6d34ccce744609c"
          },
          {
              "file_name": "png_bts.png",
              "file_id": "9d15ce7799dd499181bbc8cace4761b7"
          },
          {
              "file_name": "jpg_cat.jpg",
              "file_id": "5fd0f71238ed4086b9bb58859ac3b271"
          }
      ]
  }
  ```

* 에러

  * 이미지가 전송되지 않았을 때: [POST images/upload](#3-post-images/upload)와 동일

  * 1건의 이미지가 업로드된 경우

    ```json
    {
        "code": 400,
        "message": "Single file upload not allowed."
    }
    ```

  * 업로드된 이미지들 중 한 건의 이미지라도 허용되지 않는 확장자인 경우

    ```json
    {
        "code": 400,
        "message": "File extension of file webp_jk.webp not allowed."
    }
    ```

  * 업로드하려는 이미지 파일의 크기가 너무 큰 경우: nginx 413 request too large 에러
    ```html
    <html>

    <head>
      <title>413 Request Entity Too Large</title>
    </head>

    <body>
      <center>
        <h1>413 Request Entity Too Large</h1>
      </center>
      <hr>
      <center>nginx/1.20.2</center>
    </body>

    </html>
    ``` 
  

### GET images/:image_id

이미지 파일을 요청한다.

- 에러

  - 찾고자 하는 이미지 파일이 없을 경우

    ```html
    <html>
    
    <head>
    	<title>404 Not Found</title>
    </head>
    
    <body>
    	<center>
    		<h1>404 Not Found</h1>
    	</center>
    	<hr>
    	<center>nginx/1.20.2</center>
    </body>
    
    </html>
    ```

    

### POST images/delete/:image_id

이미지 파일 삭제를 요청한다.

- 정상 처리

  ```json
  {
      "code": 200,
      "message": "File 20995dfcf94a49e7b6d34ccce744609c successfully deleted."
  }
  ```

- 에러

  - 삭제하고자 하는 이미지 파일이 없을 경우

    ```json
    {
        "code": 400,
        "message": "File 20995dfcf94a49e7b6d34ccce744609c does not exists."
    }
    ```
