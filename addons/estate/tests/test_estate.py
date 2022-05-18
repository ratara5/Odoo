from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase, Form

# The CI will run these tests after all the modules are installed,
# not right after installing the one defining it.
@tagged('post_install', '-at_install')  # add `post_install` and remove `at_install`
class EstateTest(TransactionCase):

    @classmethod
    def setUpClass(cls):
        # add env on cls and many other things
        super(EstateTest, cls).setUpClass()

        # create the data for each tests. By doing it in the setUpClass instead
        # of in a setUp or in each test case, we reduce the testing time and
        # the duplication of code.
        ###BUYER
        cls.buyer=cls.env['res.partner'].create([
            {
            'name':'buyer'
            }
        ])

        ###PROPERTY...###
        cls.properties = cls.env['estate.property'].create([
            {
                'name': 'property_test_1',
                'expected_price': 100000,
                #It doesn't suitable to assign state to a property recently created, by default is new
                #it's posible assign garden (True) to a property recently created
            },
            {
                'name': 'property_test_2',
                'expected_price': 200000,
                #It doesn't asign state to a property recently created, by default is new
                #it's posible assign garden (True) to a property recently created
            },
            {
                'name': 'property_test_3',
                'expected_price': 300000,
                #It doesn't suitable to asign state to a property recently created, by default is new
                #it's posible to assign garden (True) to a property recently created
            },
            {
                'name': 'property_test_4',
                'expected_price': 400000,
                #It doesn't suitable to asign state to a property recently created, by default is new
                #it's posible to assign garden (True) to a property recently created
            }
        ])
        ###OFFER: An offer for each property...###
        cls.offers=cls.env['estate.property.offer'].create([
            {
                'partner_id':cls.buyer[0].id,
                'property_id':cls.properties[0].id,
                'price':110000
            },
            {
                'partner_id':cls.buyer[0].id,
                'property_id':cls.properties[1].id,
                'price':220000                
            },
            {
                'partner_id':cls.buyer[0].id,
                'property_id':cls.properties[2].id,
                'price':330000               
            },
            # logic too added as follows: if property state is canceled, doesn't allow create any offer
            {
                'partner_id':cls.buyer[0].id,
                'property_id':cls.properties[3].id,
                'price':440000               
            }
        ])
    
    ###...PROPERTY IS ONLY SOLD IF ANY OFFER ACCEPTED EXISTS...###
    def test_action_sell(self):
        """Test that everything behaves like it should when selling a property."""
        # self.properties.action_sold()
        # self.assertRecordValues(self.properties, [
        #    {'name': 'property_test_1', 'state': 'new'},
        #    {'name': 'property_test_2', 'state': 'offer_received'},
        #    {'name': 'property_test_3', 'state': 'sold'},
        #    {'name': 'property_test_4', 'state': 'canceled'} #Can I and/or Must I repeat this here and...
        # ])

        #error if doesn't exist any offer...
        with self.assertRaises(UserError):
            self.properties.action_sold()

        #...accept the offers...
        for offer in self.offers:
            offer.action_accept()

        #...now you can sell them...
        for property in self.properties:
            property.action_sold()

        #...and you can see that the state has changed
        self.assertRecordValues(self.properties, [
           {'name': 'property_test_1', 'state': 'sold'}, #Don't indicate the name 'name':'property_test_1'
           {'name': 'property_test_2', 'state': 'sold'},
           {'name': 'property_test_3', 'state': 'sold'},
           {'name': 'property_test_4', 'state': 'sold'} 
        ])

        #you cannot accept any offer for a sold property
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create([
                #create another offer for each property
                {
                    'partner_id':self.buyer[0].id,
                    'property_id':self.properties[0].id,
                    'price':120000
                },
                {
                    'partner_id':self.buyer[0].id,
                    'property_id':self.properties[1].id,
                    'price':230000
                },
                {
                    'partner_id':self.buyer[0].id,
                    'property_id':self.properties[2].id,
                    'price':340000
                },
                {
                    'partner_id':self.buyer[0].id,
                    'property_id':self.properties[3].id,
                    'price':450000
                }
            ])
 

    ###...TOTAL_AREA=LIVIG_AREA+GARDEN_AREA###
    def test_property_form(self):
        """Test that the total_area is computed like it should.""" #This will only be verificated for one property
        with Form(self.properties[0]) as prop:
            #by default: garden_area=0 and garden_orientation=False (or None?) 
            self.assertEqual(prop.garden_area,0)
            self.assertIs(prop.garden_orientation,False)
            prop.garden=True #changing garden to True...
            #...after change: garden_area=10 and garden_orientation='N'
            self.assertEqual(prop.garden_area, 10)
            self.assertEqual(prop.garden_orientation, "N")
            prop.garden=False #changing garden to False...
            #...after change: garden_area=0 and garden_orientation=False
            self.assertEqual(prop.garden_area, 0)
            self.assertIs(prop.garden_orientation, False)
    