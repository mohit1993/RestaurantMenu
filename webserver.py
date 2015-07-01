from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from database_setup import Base,Restaurant,MenuItem,User,LoginSessions
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import re
import Cookie

engine = create_engine('sqlite:///restaurantmenu.db')
DBSession = sessionmaker(bind = engine)
session = DBSession()


def login_required(request,function):
    pass

class webserverHandler(BaseHTTPRequestHandler):

    def check_login(self):
            if "Cookie" in self.headers:
                    data = Cookie.SimpleCookie(self.headers["Cookie"])
                    id = data['id'].value
                    loggeduser = session.query(LoginSessions).filter_by(user_id = id)
                    if loggeduser.count() == 1:
                            return loggeduser.one().user.username
                    else:
                            return "NotLoggedIn"

            return "NotLoggedIn"

    def do_GET(self):
        try:
            if re.compile("/restaurant/\d+$").match(self.path):
                objid = re.compile("/restaurant/([0-9]+)$").match(self.path).group(1)

                self.send_response(200)
                self.send_header('content-type','text/html')
                self.end_headers()

                data = session.query(MenuItem).filter_by(restaurant_id = objid)
                print data
                if data.count() is 0:
                        self.send_response(404)
                        self.end_headers()
                        return
                try:
                    output = "<html><body>Welcome to %s" % (session.query(Restaurant).filter_by(id = objid).one().name)
                except:
                    self.send_response(404)
                    self.end_headers()
                    return
                
                for x in data:
                        i = "<br>%s. %s <br>%s<br>%s<br><a href = '#'>Edit</a>   <a href = '#'>Delete</a><br>" % (x.id,x.name,x.description,x.price)
                        output += i

                output += "<br><br><a href = '%s/create/menuitem'>New Item</a>" %(self.path)
                output += "</body></html>"

                self.wfile.write(output)
                return

            if self.path.endswith("/create/restaurant"):
                self.send_response(200)
                self.send_header('content-type','text/html')
                self.end_headers()
                output = ''
                output += "<html><body><h3>Create a new Restaurant</h3>"
                output += "<form method = 'POST' action = '/create/restaurant'\
                enctype = 'multipart/form-data'>"

                output += "<h3>Name</h3><input type = 'text' name = 'name'>"
                output += "<input type = 'submit' value = 'Create'/></form>"

                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith('/logout'):
                self.send_response(200)
                self.send_header('content-type','text/html')
                self.end_headers()

                output = ''
                output += "<html><body><h3>Logout</h3>"
                output += "<form method = 'POST' action = '/logout'\
                enctype = 'multipart/form-data' onsubmit = 'return confirm('Are you sure about logging out')'>"
                output += "<input type = 'submit' value = 'Yes'/></form>"

                output += "</body></html>"

                self.wfile.write(output)
                return 

            if self.path.endswith("/create/menuitem"):
                self.send_response(200)
                self.send_header('content-type','text/html')
                self.end_headers()
                restaurantid = re.compile("/restaurant/(?P<id>[0-9]+)/create/menuitem$").match(self.path).group('id')
                restname = session.query(Restaurant).filter_by(id = restaurantid)
                if restname.count() is 0:
                    self.send_response(301)
                    self.send_header('Location','/create/restaurant')
                    self.end_headers()
                    return

                output = ""
                output += "<html><body><h3>Create a new Restaurant</h3>"
                output += "<form method = 'POST' action = '%s'\
                        enctype = 'multipart/form-data'>" %(self.path)

                output += "<h3>Name</h3><input type = 'text' name = 'name'>"
                output += "<h3>Description</h3><input type = 'text' name = 'description'>"
                output += "<h3>Price</h3><input type = 'text' name = 'price'>"
                output += "<input type = 'submit' value = 'Create'/></form>"

                output += "</body></html>"

                self.wfile.write(output)
                return


            if self.path.endswith("/restaurant"):
                self.send_response(200)
                self.send_header('content-type','text/html')
                self.end_headers()

                output = ""
                output += "<html><body><h1>Welcome to Pymato</h1><br>"
                username = self.check_login()
                print username
                if username is not "NotLoggedIn":
                    output += "<br>Logged in as %s<br><br><br>" %(username)
                data = session.query(Restaurant).all()
                for obj in data:
                    i = "<h4>%s.<a href = '/restaurant/%s'>%s</a></h4><br>"\
                            %(obj.id,obj.id,obj.name)
                    output += i

                output += "<a href = '/create/restaurant'>Create</a>"
                output += "</body></html>"

                self.wfile.write(output)
                print "Served the list of restaurants"
                return


            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('content-type','text/html')
                self.end_headers()

                output = ""
                output += "<html><body>&#16HOLA! <a href = '/hello'>Back to\
                Hello</a>"

                output += "<form method = 'POST' enctype='multipart/form-data'\
                action = '/hello'><h2>What would you like to say? </h2><input name\
                = 'message' type = 'text' value = 'Enter your message'><input type\
                = 'submit' value = 'Submit'></form>"

                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/register"):
                    
                    print self.end_headers
                    if self.check_login() is not "NotLoggedIn":
                        self.send_response(302)
                        self.send_header('content-type','text/html')
                        self.send_header('location','/restaurant')
                        self.end_headers()
                        return

                    output = ""
                    output += "<html><body>Register to Restaurant<br>"
                    output += "<form action = '/register' method = 'POST' enctype = 'multipart/form-data'>"
                    output += "<br>username <input type = 'text' name = 'username' placeholder = 'enter a unique username'>"
                    if "error" in self.headers:
                        output += " Username already exists"
                    output += "<br>password <input type = 'password' name = 'password'>"
                    #output += "confirm password <input type = 'password' name = 'confirm'>"
                    output += "<input type = 'submit' value = 'register'>"
                    output += "</form>"

                    output += "</body></html>"
                    self.send_response(200)
                    self.send_header('content-type','text/html')
                    self.end_headers()

                    self.wfile.write(output)
                    return

            if self.path.endswith("/login"):
                self.send_response(200)
                self.send_header('content-type','text/html')
                self.end_headers()

                output = ""
                output += "<html><body>Login to Restaurant<br>"
                output += "<form action = '/login' method = 'POST' enctype = 'multipart/form-data'>"
                output += "<br>username <input type = 'text' name = 'username'>"
                output += "<br>password <input type = 'password' name = 'password'>"
                output += "<input type = 'submit' value = 'SignIn'>"
                output += "</form>"
                
                output += "</body></html>"

                self.wfile.write(output)
                return

        except IOError:
            self.send_error(404,"File Not Found %s" % self.path)


    def do_POST(self):
        try:
            if self.path.endswith('/logout'):
                res = self.check_login()
                if res is not 'NotLoggedIn':
                    id = session.query(User).filter_by(username = res).one().id
                    session.query(LoginSessions).filter_by(user_id = id).delete()
                    session.commit()

                self.send_response(302)
                self.send_header('content-type','text/html')
                self.send_header('location','/restaurant')
                self.end_headers()

                return

            if self.path.endswith("/create/menuitem"):
                    ctype,pdict = cgi.parse_header(self.headers.getheader('content-type'))
                    if ctype == 'multipart/form-data':
                            fields = cgi.parse_multipart(self.rfile,pdict)

                    postcontent = fields.get('name')
                    postcontent += fields.get('description')
                    postcontent += fields.get('price')
                    restid = re.compile('/restaurant/([0-9]+)/').match(self.path).group(1)
                    rest = session.query(Restaurant).filter_by(id = restid).one()
                    newitem = MenuItem(name = postcontent[0],description = postcontent[1],price = postcontent[2],restaurant = rest)
                    session.add(newitem)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type','text/html')
                    self.send_header('location','/restaurant/%s' %(restid))
                    self.end_headers()
                    return


            if self.path.endswith("/create/restaurant"):
                    ctype,pdict = cgi.parse_header(self.headers.getheader('content-type'))
                    if ctype == 'multipart/form-data':
                            fields = cgi.parse_multipart(self.rfile,pdict)

                    postcontent = fields.get('name')

                    newrest = Restaurant(name = postcontent[0])
                    session.add(newrest)
                    session.commit()

                    self.send_response(301)
                    self.send_header('content-type','text/html')
                    self.send_header('location','/restaurant')
                    self.end_headers()
                    return

            if self.path.endswith("/register"):
                    ctype,pdict = cgi.parse_header(self.headers.getheader('content-type'))
                    if ctype == 'multipart/form-data':
                            fields = cgi.parse_multipart(self.rfile,pdict)

                    data = fields.get('username')
                    data += fields.get('password')

                    indb = session.query(User).filter_by(username = data[0])
                    if indb.count() == 1:
                        self.send_response(302)
                        self.send_header('content-type','text/html')
                        self.send_header('error','Username already exists')
                        self.send_header('location','/register')
                        self.end_headers()
                        return

                    obj = User()
                    obj.username = data[0]
                    obj.password = data[1]
                    session.add(obj)
                    session.commit()

                    self.send_response(302)
                    self.send_header('content-type','text/html')
                    self.send_header('location','/login')
                    self.end_headers()
                    return

            if self.path.endswith("/login"):
                    ctype,pdict = cgi.parse_header(self.headers.getheader('content-type'))
                    if ctype == 'multipart/form-data':
                            fields = cgi.parse_multipart(self.rfile,pdict)

                    data = fields.get('username')
                    data += fields.get('password')

                    user = session.query(User).filter_by(username = data[0])
                    if user.count() == 1:
                        if user.one().password == data[1]:
                            newsession = LoginSessions(user = user.one())
                            session.add(newsession)
                            session.commit()
                            c = Cookie.SimpleCookie()
                            c['id'] = user.one().id
                            self.send_response(301)
                            self.send_header('content-type','text/html')
                            self.send_header('Set-Cookie',c.output(header = ''))
                            self.send_header('location','/restaurant')
                            self.end_headers()
                                    
                    return

        except IOError:
            self.send_response(404,"Input Data incorrect")

def main():
    try:
        port = 8080
        server = HTTPServer(('',port),webserverHandler)
        print "Web server running at port %s" % port
        server.serve_forever()

    except KeyboardInterrupt:
        print "^C entered,stopping web server...."
        server.socket.close()


if __name__ == "__main__":
    main()
