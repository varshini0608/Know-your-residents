import random,string
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import render_to_response,render
from pyramid.view import view_config
import datetime
from sqlalchemy.exc import DBAPIError
from sqlalchemy import and_
from sqlalchemy import func
from datetime import datetime
from ..models import MyModel
from ..models import Houseowner,complaint,deptgen
from pyramid.session import SignedCookieSessionFactory


@view_config(route_name='feedback', renderer='../templates/feedback.jinja2')
def my_view(request):
    try:
        query = request.dbsession.query(MyModel)
        one = query.filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'one': one, 'project': 'agrini'}

@view_config(route_name='fpwd',renderer='../templates/FPWD.jinja2')
def random_pwd(request):
    try:

        def rand_pass(size):
            generate_pass = ''.join([random.choice( string.ascii_uppercase + string.ascii_lowercase + string.digits)for n in range(size)])

            return generate_pass


        print("errorcheck")
        if request.POST.get('button1'):
           fl_id= request.params['flat_id']
           fl_id2=fl_id.split(",")
           print('fl_id2',fl_id2)
           for i in range(0,len(fl_id2)):
                pwd = rand_pass(6)
                obj=Houseowner()
                obj.username=fl_id2[i]
                obj.password=pwd
                obj.emailid='NA'
                request.dbsession.add(obj)


           return()
        else:
             return()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)




@view_config(route_name='signin', renderer='../templates/signup.jinja2')
def update_signin(request):
    try:
        if request.POST.get('signup'):
            print("check")
            fl_id= request.params['flat_id']
            print('fl_id',fl_id)
            em_id= request.params['email_id']
            print('email_id',em_id)
            upwd= request.params['upwd']
            print('upwd',upwd)
            obj=Houseowner()
            print("before_query")
            result=request.dbsession.query(Houseowner).filter(Houseowner.username==fl_id)
            for row in result:
                print(row.password)
                row.password=upwd
                row.emailid=em_id

            #session.query(User).filter(User.id==3).update({'name': 'user'})
            #request.dbsession.query(Houseowner).filter(and_(=u_id,obj.username==fl_id)).update({obj.emailid:em_id,obj.password:upwd})
            print("After_query")
            #getname=request.dbsession.query(login_models)
            #name=getname.name
            #pasword=getname.password
            #Sreturn Response('saved')
            #return render_to_response('../templates/login.jinja2',{}, request=request)
            return()
        else:
            return()


    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)


@view_config(route_name='complaint',renderer='../templates/raisecomplaints.jinja2')
def complaint_issue(request):
    try:
        session=request.session
        if request.POST.get('raise'):
            fl_id= request.params['flat_id']
            print('fl_id',fl_id)
            title= request.params['title']
            print('title',title)
            dept= request.params['department']
            print('dept',dept)
            issue= request.params['issue']
            print('issue',issue)
            obj=complaint()
            result=request.dbsession.query(Houseowner).filter(Houseowner.username==fl_id)
            for row in result:
                obj.u=row.houseownerid
            obj.title=title
            obj.dept_id=dept
            obj.issue=issue
            obj.allocate_by='NA'
            obj.complaint_status='NA'
            #obj.time_viewed='0000-01-01 00:00:00'
            #obj.time_alloc='2019-01-01 00:00:00'
            #obj.time_completed='2019-01-01 00:00:00'
            obj.reply='NA'
            request.dbsession.add(obj)
            print("entry_sucessfully")
            return Response(render('../templates/raisecomplaints.jinja2',{'error':'Submitted successfully...... !'},request=request))

        else:
            print('enter try')
            getdept=request.dbsession.query(deptgen).filter(deptgen.visible=='T').all()
            print('after try')
            return{'getdept':getdept,'flat_id':session['flat_id']}


    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)


'''def login(request):
    try:
        if request.POST.get('button1'):
            fl_id= request.params['flat_id']
            print('fl_id',fl_id)
            pas= request.params['password']
            print('pas',pas)
            result=request.dbsession.query(Houseowner).filter(and_(Houseowner.password==pas,Houseowner.username==fl_id))
            for row in result:
                print(row.password)
                print("login s")
            #return Response('login_sucessfull.............')
            if result=={}:
                return()
            else:
                return render_to_response('../templates/complaint.jinja2',{'foo':1, 'bar':2},request=request)
            #print('result.password',result.pwd)
            #print("login_sucessfull")
            #return Response('login_sucessfull.............')
        else:
            #return Response('login_failed.............please enter valied ')
            return()


    except DBAPIError:
            return Response(db_err_msg, content_type='text/plain', status=500)'''


@view_config(route_name='alloc', renderer='../templates/alloc.jinja2')
def alloc(request):
    try:
        if request.POST.get('admin'):
            print("check")
            is_id=request.params['id']
            print('id',is_id)
            fl_id= request.params['flat_id']
            print('fl_id',fl_id)
            alloc= request.params['aloc_by']
            print('alloc',alloc)
            state= request.params['status']
            print('state',state)
            areplay= request.params['replay']
            print('areplay',areplay)
            #obj=complaint()
            print("before_query")
            result=request.dbsession.query(complaint).filter(complaint.flat_id==fl_id,complaint.issue_id==is_id)
            for row in result:
                print(row.complaint_status)
                row.complaint_status=state
                row.allocate_by=alloc
                row.reply=areplay
                if state=='logged':
                    row.time_viewed=datetime.now()
                elif state=='assigned':
                    row.time_alloc=datetime.now()
                elif state=='completed':
                    row.time_completed=datetime.now()


            #session.query(User).filter(User.id==3).update({'name': 'user'})
            #request.dbsession.query(Houseowner).filter(and_(=u_id,obj.username==fl_id)).update({obj.emailid:em_id,obj.password:upwd})
            print("After_query")
            #getname=request.dbsession.query(login_models)
            #name=getname.name
            #pasword=getname.password
            #Sreturn Response('saved')
            #return render_to_response('../templates/login.jinja2',{}, request=request)
            return Response(render('../templates/alloc.jinja2',{'error':'Submitted successfully...... !'},request=request))
        else:
            #is_id=request.params['id']
            #print('id',id)

            #fl_id= request.params['flat_id']
            #print('fl_id',fl_id)
            id=request.matchdict.get('id')
            flat_id=request.matchdict.get('flat_id')
            return Response(render('../templates/alloc.jinja2',{'id':id,'flat_id':flat_id},request=request))


    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)

@view_config(route_name='fpass', renderer='../templates/forgotpass.jinja2')
def admin(request):
    try:
        if request.POST.get('button1'):
            print("check")
            fl_id= request.params['flat_id']
            print('fl_id',fl_id)
            em_id= request.params['email_id']
            print('em_id',em_id)
            upwd= request.params['upwd']
            print('upwd',upwd)
            #obj=complaint()
            print("before_query")
            result=request.dbsession.query(Houseowner).filter(and_(Houseowner.username==fl_id,Houseowner.emailid==em_id))
            for row in result:
                print(row.password)
                #row.complaint_status=state
                row.password=upwd

            #session.query(User).filter(User.id==3).update({'name': 'user'})
            #request.dbsession.query(Houseowner).filter(and_(=u_id,obj.username==fl_id)).update({obj.emailid:em_id,obj.password:upwd})
            print("After_query")
            #getname=request.dbsession.query(login_models)
            #name=getname.name
            #pasword=getname.password
            #Sreturn Response('saved')
            #return render_to_response('../templates/login.jinja2',{}, request=request)
            return()
        else:
            return()


    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)

@view_config(route_name='status', renderer='../templates/issue status.jinja2')



@view_config(route_name='status', renderer='../templates/issue status.jinja2')
def issue_record(request):
    details=[]
    try:
        #dept_id=request.query_string
        #print('dept_id',dept_id)
        dept_name=request.matchdict.get('dept_name')
        print('dept_name',dept_name)
        getDept=request.dbsession.query(deptgen).filter(deptgen.dept_name==dept_name).first()
        query = request.dbsession.query(complaint).filter(complaint.dept_id==getDept.dept_id).all()
        for row in query:
            det=[]
            det.append(row.issue_id)
            det.append(row.time_created)
            det.append(row.allocate_by)
            det.append(row.title)
            det.append(row.flat_id)
            det.append(row.issue)
            dept_id=row.dept_id
            getDept=request.dbsession.query(deptgen.dept_name).filter(deptgen.dept_id==dept_id).first()
            det.append(getDept.dept_name)
            det.append(row.complaint_status)
            det.append(row.time_completed)
            det.append(row.reply)
            details.append(det)

            #row.flat_id


    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'project': details}

@view_config(route_name='login',renderer='../templates/login.jinja2')
def login(request):
      if request.POST.get('button1'):
        session=request.session
        x = request.params['flat_id']
        z = request.params['password']
        session['flat_id']=x
        getUser = request.dbsession.query(Houseowner).filter(Houseowner.username==x,Houseowner.password==z).first()
        if getUser is not None:
               #session = request.session
               #session['user'] = x
               return Response(render('../templates/main.jinja2',{'user':x},request=request))
        '''for n in prof:
            if n.email == x and n.password == z:
               session = request.session
               session['user'] = x
               return Response(render('../templates/professor-chapters.jinja2',{'user':n.username},request=request))
        for n in admin:
            if n.username == x and n.schoolname == y and n.password == z:
               session = request.session
               session['user'] = x
               return Response(render('../templates/admin-link.jinja2',{},request=request))'''
        return Response(render('../templates/login.jinja2',{'error':'Username or password is incorrect !'},request=request))
      else:
        return {}
@view_config(route_name='adminlogin',renderer='../templates/adlogin.jinja2')
def adlogin(request):
    if request.POST.get('button1'):

        x = request.params['username']
        z = request.params['password']
        user="admin"
        pwd="adminpass"
        if user == x and pwd == z :
            #session = request.session
            #session['user'] = x
            return Response(render('../templates/admin.jinja2',{'user':'flat_id'},request=request))
        return Response(render('../templates/adlogin.jinja2',{'error':'Username or password is incorrect !'},request=request))
    else:
        return {}



@view_config(route_name='home',renderer='../templates/index.jinja2')
def l3(request):
    print("button function")

    return()

@view_config(route_name='l2',renderer='../templates/main.jinja2')
def button(request):
    print("button function")
    return{}

@view_config(route_name='status', renderer='../templates/monthwise.jinja2')
def month(request):
    details=[]
    try:
        #dept_id=request.query_string
        #print('dept_id',dept_id)
        dept_name=request.matchdict.get('dept_name')
        print('dept_name',dept_name)
        #getDept=request.dbsession.query(deptgen).filter(deptgen.dept_name==dept_name).first()
        query = request.dbsession.query(complaint).filter(complaint.timecreated.strftime("%B")==month.first()
        for row in query :
            det=[]
            det.append(row.issue_id)
            det.append(row.time_created)
            det.append(row.allocate_by)
            det.append(row.title)
            det.append(row.flat_id)
            det.append(row.issue)
            dept_id=row.dept_id
            getDept=request.dbsession.query(deptgen.dept_name).filter(deptgen.dept_id==dept_id).first()
		#time_created.strftime("%B")==
            det.append(getDept.dept_name)
            det.append(row.complaint_status)
            det.append(row.time_completed)
            det.append(row.reply)
            details.append(det)

         #   row.flat_id


    except DBAPIError:
        
        return Response(render('../templates/monthwise.jinja2',{'details':query},request=request))


@view_config(route_name='ui',renderer='../templates/userissue.jinja2')
def ui(request):
    try:
        if request.session['role']=='admin':
            details=[]
            try:
                query = request.dbsession.query(complaint).all()
                for row in query:
                    det=[]
                    det.append(row.issue_id)
                    det.append(row.time_created)
                    det.append(row.allocate_by)
                    det.append(row.title)
                    print(row.flat_id)
                    det.append(row.flat_id)
                    det.append(row.issue)
                    dept_id=row.dept_id
                    getDept=request.dbsession.query(deptgen.dept_name).filter(deptgen.dept_id==dept_id).first()
                    det.append(getDept.dept_name)
                    det.append(row.complaint_status)
                    det.append(row.time_completed)
                    det.append(row.reply)
                    details.append(det)

                    row.flat_id

            except DBAPIError:
                return Response(db_err_msg, content_type='text/plain', status=500)
            return {'project': details}
        raise Exception("Your Are Not a Admin")
    except:
        url=request.route_url('login')
        return HTTPFound(location=url)

@view_config(route_name='logstatus', renderer='../templates/log_status.jinja2')
def log_record(request):
    details=[]
    try:
        query = request.dbsession.query(Houseowner).all()
        for row in query:
            det=[]
            det.append(row.username)
            det.append(row.password)
            det.append(row.emailid)
            details.append(det)

            #row.flat_id


    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'project': details}

@view_config(route_name='view_complaint_admin', renderer='../templates/dept_wise_complaint.jinja2')
def view_complaint_admin_view(request):
    try:
        getDept=request.dbsession.query(deptgen).filter(deptgen.visible=='T').order_by(deptgen.dept_id).all()
        dept_raise=[]
        for i in getDept:
            dept_sub=[]
            dept_id=i.dept_id
            dept_name=i.dept_name
            raised_count=request.dbsession.query(func.count(complaint.complaint_status)).filter(complaint.dept_id==dept_id,complaint.complaint_status!='old').scalar()
            logged_count=request.dbsession.query(func.count(complaint.complaint_status)).filter(complaint.complaint_status=='logged',complaint.dept_id==dept_id).scalar()
            assigned_count=request.dbsession.query(func.count(complaint.complaint_status)).filter(complaint.complaint_status=='assigned',complaint.dept_id==dept_id).scalar()
            completed_count=request.dbsession.query(func.count(complaint.complaint_status)).filter(complaint.complaint_status=='completed',complaint.dept_id==dept_id).scalar()

            dept_sub.append(dept_name)
            dept_sub.append(raised_count)
            dept_sub.append(logged_count)
            dept_sub.append(assigned_count)
            dept_sub.append(completed_count)
            dept_raise.append(dept_sub)

        return{'dept_raise':dept_raise}


    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_Agrini_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
