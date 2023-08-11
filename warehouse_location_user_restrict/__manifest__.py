
{
    'name': 'Warehouse locations User Restrict Validate',
    'version': '6.0.0',
    'category': 'Warehouse',
    "author": 'Zero Systems',
    "company": 'Zero for Information Systems',
    "website": "https://www.erpzero.com",
    "email": "sales@erpzero.com",
    "sequence": 0,
    'license': 'OPL-1',
    'live_test_url': 'https://www.youtube.com/playlist?list=PLXFpENL3b6WU9TzMdawrHJsUBqMDXkcbn',
    'summary': """Warehouse Destination Location Users Approve""",
    'description': """Automatically Create Receipt/Delivery orders if any branch validates a 
                      Deliver Order/Receipt to the selected branch,Inter branch Stock Transfer, Stock Transfer,
                      Create counterpart Receipt/Delivery Orders between Branches""",
    'depends': ['base','stock'],
    'data': [
        'views/view.xml',
    ],
    'images': ['static/description/logo.PNG'],
    'installable': True,
    'auto_install': False,
    'application': False,
    "price": 50.0,
    "currency": 'EUR',
}
