PIN_API
=============

### Python Flask를 기반으로 한 Restful Api입니다.
### 데이터베이스 언어로 Peewee를 이용하고, flask_bcrypt를 이용해 패스워드를 암호화합니다.
### JWT 형식의 토큰 인증을 추가할 예정입니다.
### 모티브는 핀터레스트로, 이미지를 저장하는 Pin 모델과 Pin의 묶음인 Board 모델이 있습니다.

1. /hello
GET : 'name' 파라미터를 받고 {'name': name}을 json string 형식으로 리턴합니다. 파라미터 시험용

POST : {'message': 'hello, World!'}를 리턴합니다. json 스트링 시험용

2. /user
POST : 'username', 'email', 'password' 파라미터를 받고 그 정보를 DB의 User 테이블에 저장합니다.
        저장한 user의 정보(암호화된 패스워드를 포함)을 리턴합니다.

GET : 'username', 'password' 파라미터를 받고 해당하는 user 객체를 찾습니다.
       찾은 user의 정보(암호화되지 않은 패스워드를 포함)을 리턴합니다.

3. /pin/<name>
POST : 'img_url', 'description', 'board' 파라미터를 받고 name과 함께 그 정보를 DB의 Pin 테이블에 저장합니다.
        성공 메시지를 리턴합니다. (CREATE)
GET :  주어진 name을 가진 Pin의 정보를 리턴합니다. (READ)
PUT :  'name', 'img_url', 'description', 'board' 파라미터를 받고 주어진 name을 가진 Pin의 정보를 업데이트합니다.
        성공 메시지를 리턴합니다. (UPDATE)
DELETE : 주어진 name을 가진 Pin을 삭제합니다.
         성공 메시지를 리턴합니다.

4. /pin
GET : 모든 Pin 정보를 리턴합니다.


5. /board/<title>
POST : 'title', 'comment' 파라미터를 받고 그 정보를 DB의 Board 테이블에 저장합니다.
       성공 메시지를 리턴합니다.
GET :  주어진 title을 가진 Board의 정보를 리턴합니다.
PUT :  'title', 'comment' 파라미터를 받고 주어진 title을 가진 Board의 정보를 업데이트합니다.
       성공 메시지를 리턴합니다.
DELETE : 주어진 title을 가진 Board를 삭제합니다.
         성공 메시지를 리턴합니다.

6. /board
GET : 모든 Board 정보를 리턴합니다.

