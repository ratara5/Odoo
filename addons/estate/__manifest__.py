{
    'name': "Real Estate Advertisement",
    'version': '1.0',
    'depends': ['base'],
    'author': "Author Name",
    'category': 'Category',
    'description': """
    Real Estate Advertisement description text
    """,
    # data files always loaded at installation
    'data': ['security/ir.model.access.csv',
            'security/security.xml',
            'views/estate_property_views.xml',
            'views/estate_property_menus.xml',
            'views/res_users_views.xml'
            
        
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
        
    ],
}