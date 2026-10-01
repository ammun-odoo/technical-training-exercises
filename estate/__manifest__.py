{
    "name": "Real Estate",
    "author": "ammun", 
    "summary": """ A test module focused on real estate. """,
    "version": "20.0.0.0.0",
    "license": "OEEL-1",
    "depends": ["base"],
    "application": True, # Makes the module an app discoverable in the app store
    "data": [
        # Security
        "security/res_groups.xml", 
        # "security/ir.model.access.csv", #<=== ONLY Odoo < 20.0, the latest 20.0 version merged this with rules into ir.access!
        "security/ir.access.csv",
        # Views -- Must be defined before menus since you need to call it through the menus
        "views/estate_property_views.xml",
        "views/estate_property_offer_views.xml",
        # Menus
        "views/estate_menu.xml",
    ],
    "demo": ["demo/demo.xml"],
}