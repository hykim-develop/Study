# flask 프레임워크 안에서 특정 기능을 로드 
from flask import Flask, render_template, request, redirect
# render_template -> templates 폴더 안에 html 문서를 가져오기 위한 기능
# request -> 유저가 보낸 데이터에 접근하기 위한 기능
# redirect -> 특정 주소로 이동

# db.py 안에 MyDB를 로드 
from db import MyDB
# querys 안에 user 모듈을 로드 
from querys import user

# Flask class 생성 -> 웹 서버를 구축 기능 
# class 생성시 생성자 함수 호출 
    # 필수 인자 1개 -> 현재 실행이 되는 파일의 이름(app.py)
    # 파일의 이름을 그대로 사용하게 되면 -> 파일의 이름이 변경이 될때 매번 수정 작업 필요
    # __name__ -> 현재 파일을 이름 
app = Flask(__name__)
db = MyDB()
# 서버가 처음 시작 시 table을 생성한다. 
db.sql_query(user.create_query)
# DB 서버와의 연결을 종료 
db.commit()

# 웹 서버의 api 목록들 생성(식당에서의 메뉴판을 생성)

# 데코레이션 ->  @함수 
# 네비게이션 함수 
# 특정 주소와 함수를 연결 
# 주소 -> base_url(127.0.0.1:5000) + sub_url(상대 주소) -> 이 주소로 요청이 들어왔을때 함수를 호출

# 127.0.0.1:5000/ -> 주소로 요청이 들어왔을 때
@app.route("/")
def index():
    # return "Hello Flask"
    # HTML로 하이퍼 링크 생성 
    # return "<a href='https://www.google.com'>Google</a>"
    # templates 폴더 안에 html 문서를 불러와서 되돌려준다. (render_template())
    return render_template("index.html")
    # render_template에서는 {%=변수명%}는 python 에서의 변수를 담겠다. 
    # {{python code}} code를 인식하여 조건에 맞는 경우에만 html를 추가 
    #                  반복문을 이용해서 html를 반복적으로 추가 



# 127.0.0.1:5000/second 주소로 요청이 들어왔을 때
@app.route('/second')
# 함수의 이름은 중복되면 안 된다. 
def second():
    return "Second Page"

# /login 주소를 생성 
@app.route('/login')
def login():
    # 유저가 보낸 데이터를 받아온다. (flask 프레임워크에서 기능을 불러와서 사용)
    # get 방식으로 보낸 데이터를 확인 
    print(request.args)
    # request.args 가 dict 형태 -> 각각의 key 값으로 데이터를 추출 
    print("유저가 입력한 ID : ", request.args['input_id'])
    print("유저가 입력한 password : ", request.args['input_pass'] )
    # DataBase server에 해당하는 아이디, 패스워드가 모두 일치하는 데이터가 존재하는가?
    # 조건문을 이용하여 로그인 성공 / 실패 
    if request.args['input_id'] == 'admin' and request.args['input_pass'] == '1234':
        # 로그인 성공 
        return "로그인 성공"
    else:
        return "ID, PASSWORD를 확인해주세요"

# /login2 주소를 생성 (post 방식)
# post 방식은 데이터를 숨겨서 보낸다 // 웹브라우져에서 주소창에 입력하여 확인이 불가능
@app.route('/login2', methods=['post'])
def login2():
    # 유저가 보낸 데이터를 확인 
    # post 방식에서는 request.form 에 데이터가 존재 
    print(request.form)
    _id = request.form['input_id']
    _pass = request.form['input_pass']
    # if _id == 'admin' and _pass == '1234':
    #     # 로그인이 성공한 경우에는 새로운 페이지를 보여준다.
    #     return render_template('main.html')
    # else:
    #     # 로그인이 실패한 경우에는 로그인 화면으로 되돌아간다. 
    #     # 특정 주소로 이동
    #     return redirect('/')
    # DB server의 회원 정보를 이용해서 로그인 기능 
    # user 모듈 안에 있는 login_query 로드 -> db.sql_query(인자로 사용, data들)
    # login_query에는 2개의 데이터가 필요 (id, password)
    sql_result = db.sql_query( user.login_query, _id, _pass )
    # DB_server와의 연결을 종료 
    db.commit()
    # id, pass를 모두 정확하게 입력했을때( DB에 데이터가 존재하면? ) -> 
    #  [{'id' : xxxx, 'password' : xxxx, 'name' : xxxx}] --> bool 형태로 변환 -> True
    # 데이터가 존재하지 않은 경우( 로그인 실패 ) -> () --> bool 형태로 변환 -> False
    print(sql_result)
    if sql_result:
        # 로그인이 성공했을 때는 특정 데이터를 html과 같이 유저에게 보낸다.
        # 로그인을 한 계정의 이름을 화면에 표시
        # 로그인을 한 계정의 이름은 -> 
        # sql_result : [{'id': 'admin', 'password': '1234', 'name': 'kim'}]
        # 리스트에서 특정 위치를 선택 -> sql_result[0] -> {'id': 'admin', 'password': '1234', 'name': 'kim'}
        # 딕셔너리에서 특정 키를 선택 -> sql_result[0]['name'] -> 'kim'
        sql_name = sql_result[0]['name']
        # render_template( 첫번째 인자는 html 문서, html 문서에서 사용할 변수명 = 데이터, ... ) -> html 문서를 문자형으로 변환
        return render_template('main.html')
    else:
        return redirect('/')
    



# 웹서버를 시작한다. (구동한다.) -> 함수의 return과 흡사 -> 
# run() 함수 아래의 주소 값들은 적용이 되지 않는다.
# run() 매개변수 
    # host 매개변수 -> 허용 가능 주소 목록 ( 기본값은 로컬의 pc에서만 접근 가능, 
    #                                   0.0.0.0으로 지정하면 모든 주소가 접근이 가능)
    # port 매개변수 -> 해당 웹서버의 포트 번호를 지정(5000번 기본값)
    # debug 매개변수 -> 디버그 모드를 사용할 것인가? (기본값 : False)
    #                   True 변경하면 개발 모드 변경 -> 파일은 수정이 됬을때 서버가 재시작
app.run(debug=True)
