# Тестовое задание processing image

# Endpoints
 - `POST` /images/ - дает ссылку
 - `POST` /images/upload/{s3_url}/ - обрабатывает эту ссылку
 - `GET` /projects/{id}/images/
 - `WebSocket` /ws/{project_id}/

# Documentation

## Info
Использовалось S3 от selectel + асинхронная библиотека aiobotocre

# Logic
В endpoint `POST` /images/ отправляется имя файла `filename` и id проекта `project` после чего дается ссылка с
параметрами которого нужно отправить `POST` запрос в этот `ulr` 

Example `POST` to `/images/` endpoint
```shell
curl -X 'POST''http://localhost:8000/images/?filename=image.jpg&project_id=3'
```

Response 
```shell
{
    "upload_link": "http://localhost:8000/images/upload/_url_of_the_s3__/",
    "params": {
        "key": "image.jpg",
        "x-amz-algorithm": "AWS4-HMAC-SHA256",
        "x-amz-credential": "b681c9f6asdfasdfasdf315d2/20240630/ru-1/s3/aws4_request",
        "x-amz-date": "12312340630T11393dsZ",
        "policy": "eyJleHBpcmasdfasdfasdfasdfasdfzJaIiwgImNvbmRpdGlvbnMiOiBbeyJidWNrZXQiOiAicHJvY2Vzcy1pbWFnZSJ9LCB7ImtleSI6ICJsaWJzX2ltYWdlLmpwZyJ9LCB7IngtYW16LWFsZ29yaXRobSI6ICJBV1M0LUhNQUMtU0hBMjU2In0sIHsieC1hbXotY3JlZGVudGlhbCI6ICJiNjgxYzlmNjRkZmI0NzU1YmQ3MDMwMWJiZjkzMTVkMi8yMDI0MDYzMC9ydS0xL3MzL2F3czRfcmVxdWVzdCJ9LCB7IngtYW16LWRhdGUiOiAiMjAyNDA2MzBUMTEzOTMyWiJ9XX0=",
        "x-amz-signature": "17a12ceasdfasdfasdfasdfasdfasdfasdfadasdasdfs3fdceb9e4c9266e4d3752760c18ea",
        "project_id": 2
    }
}
```
