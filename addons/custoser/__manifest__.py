{
    'name':'Customer Services',
    'version':'1.0',
    'description':'Module Services Customer to Customer',
    'depends':
    [
        'base',
        'web'
    ],
    'data':
    [
        'security/ir.model.access.csv',
        'views/customer_service_views.xml',
        'views/customer_service_timesheet_views.xml',
        'views/customer_service_tag_views.xml',
        'views/customer_service_project_views.xml',
        'views/customer_service_menus.xml'
    ],
    'installable':True,
    'application':True,
    'auto_install':False
}