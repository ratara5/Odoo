# -*- coding: utf-8 -*-
# More info at https://www.odoo.com/documentation/master/reference/module.html

{
    "name": "Real Estate",
    "depends": [
        "base",
        "web",
    ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/estate_property_offer_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_views.xml",
        "views/res_users_views.xml",
        "views/estate_menus.xml",
        "data/property_tag.xml",
        "data/estate.property.type.csv",
        "data/estate_offer.xml",
        "data/estate_property.xml",
        "report/estate_property_templates.xml",
        "report/estate_property_reports.xml"

    ],
    
    "application": True,
}
