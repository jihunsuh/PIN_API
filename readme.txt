Python Flask를 기반으로 한 Restful Api입니다.
데이터베이스 언어는 Peewee를 이용하고, 인증 방식은 Token을 사용합니다.
bcrypt를 이용해 패스워드를 암호화합니다.
모티브는 핀터레스트로, 이미지를 저장하는 Pin 모델과 Pin의 묶음인 Board 모델이 있습니다.

/home
POST : 'hey!'를 리턴합니다. 서버 시험용

/hello
GET : 'name' 파라미터를 받고 그 name을 json string 형식으로 리턴합니다. 파라미터 시험용
POST : {'message': 'hello, World!'}를 리턴합니다. json 스트링 시험용'

/token
GET : token을 발급하고 그 토큰을 리턴합니다. 토큰 발급용

/user
POST : 'id', 'email', 'password' 파라미터를 받고 그 정보를 DB의 User 테이블에 저장합니다.
        저장한 user의 정보(암호화된 패스워드를 포함)을 리턴합니다.
GET : 'id', 'password' 파라미터를 받고 해당하는 user 객체를 찾습니다.
        찾은 user의 정보(암호화되지 않은 패스워드를 포함)을 리턴합니다.


/pin
POST : CREATE 'name', 'img_url', 'description', 'board' 파라미터를 받고 그 정보를 DB의 Pin 테이블에 저장합니다.
        저장한 Pin의 정보를 리턴합니다.
GET :  READ 'name'파라미터를 받고 그 name을 가진 Pin의 정보를 리턴합니다.
PUT :  UPDATE 'name', 'img_url', 'description', 'board' 파라미터를 받고 주어진 name을 가진 Pin의 정보를 업데이트합니다.
        업데이트한 Pin의 정보를 리턴합니다.
DELETE : 'name' 파라미터를 받고 그 name을 가진 Pin을 삭제합니다.
        pin을 리턴합니다.

/board
POST : CREATE 'title', 'comment' 파라미터를 받고 그 정보를 DB의 Board 테이블에 저장합니다.
        저장한 Board의 정보를 리턴합니다.
GET :  READ 'title'파라미터를 받고 그 title을 가진 Board의 정보를 리턴합니다.
PUT :  UPDATE 'title', 'comment' 파라미터를 받고 주어진 title을 가진 Board의 정보를 업데이트합니다.
        업데이트한 Board의 정보를 리턴합니다.
DELETE : 'title' 파라미터를 받고 그 title을 가진 Board를 삭제합니다.
        board를 리턴합니다.

/pin/list
POST : 모든 pin들을 보여줍니다.

/board/list
BOARD : 모든 board들을 보여줍니다.

