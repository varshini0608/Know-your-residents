def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('alloc', '/alloc/{id}/{flat_id}')
    #config.add_route('alloc', 'alloc1')
    config.add_route('login', 'login')
    config.add_route('complaint', 'complaint')
    config.add_route('fpwd', 'fpwd')
    config.add_route('signin', 'signin')
    config.add_route('fpass', 'fpass')
    config.add_route('status', '/status/{dept_name}')
    config.add_route('adminlogin', 'adlogin')
    config.add_route('l2', 'choise')
    config.add_route('ui', 'ui')
    config.add_route('logstatus', 'logstatus')
    config.add_route('view_complaint_admin', 'view_complaint_admin')
    config.add_route('feedback', 'feedback')
    config.add_route('month', 'month')
    config.add_route('issues', 'issues')
    config.add_route('userissues', 'userissues')


    
