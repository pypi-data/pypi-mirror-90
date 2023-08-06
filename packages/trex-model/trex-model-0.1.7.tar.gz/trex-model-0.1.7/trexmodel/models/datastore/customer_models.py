'''
Created on 5 Jan 2021

@author: jacklok
'''
from google.cloud import ndb
from trexmodel.models.datastore.ndb_models import BaseNModel, DictModel, FullTextSearchable
from trexmodel.models.datastore.user_models import User
from trexmodel.models.datastore.merchant_models import MerchantAcct
import trexmodel.conf as model_conf
from trexlib.utils.security_util import generate_user_id, hash_password
from trexlib.utils.string_util import random_number, is_not_empty
import logging
from trexlib.utils.common.cache_util import cache


logger = logging.getLogger('root')


class Customer(BaseNModel, DictModel, FullTextSearchable):
    '''
    parent is User
    '''
    
    merchant_acct               = ndb.KeyProperty(name="merchant_acct", kind=MerchantAcct)
    merchant_reference_code     = ndb.StringProperty(name="merchant_reference_code", required=False)
    registered_datetime         = ndb.DateTimeProperty(required=False, auto_now_add=True)
    modified_datetime           = ndb.DateTimeProperty(required=False, auto_now=True)
    
    #---------------------------------------------------------------------------
    # User denormalize fields
    #---------------------------------------------------------------------------
    name                        = ndb.StringProperty(required=False)
    mobile_phone                = ndb.StringProperty(required=False)
    email                       = ndb.StringProperty(required=False)
    
    birth_date                  = ndb.DateProperty(required=False, indexed=False) 
    gender                      = ndb.StringProperty(required=False)
    reference_code              = ndb.StringProperty(required=True)
    
    fulltextsearch_field_name   = 'name'
    
    dict_properties     = ['name', 'mobile_phone', 'email', 'gender', 'birth_date', 'reference_code', 'merchant_reference_code', 'registered_datetime', 'modified_datetime']
    
    @property
    def registered_user_acct(self):
        return User.fetch(self.key.parent().urlsafe())
    
    @property
    def registered_merchant_acct(self):
        return MerchantAcct.fetch(self.merchant_acct.urlsafe())
    
    
    
    @classmethod
    @cache.memoize(timeout=60)
    def get_by_merchant_reference_code(cls, merchant_reference_code):
        return cls.query(cls.merchant_reference_code==merchant_reference_code).get()
    
    @classmethod
    def create(cls, merchant_acct=None, name=None, email=None, mobile_phone=None,
               password=None):
        
        created_user = User.create(name=name, email=email, mobile_phone=mobile_phone, 
                           password=password)
        
        created_user.put()
        
        return cls.create_from_user(merchant_acct, created_user)
    
    @classmethod
    def create_from_user(cls, merchant_acct, user_acct):
        
        created_customer = cls(parent=user_acct.create_ndb_key(), name=user_acct.name, email=user_acct.email, 
                           mobile_phone=user_acct.mobile_phone, gender=user_acct.gender, reference_code=user_acct.reference_code,
                           merchant_acct = merchant_acct.create_ndb_key()
                           )
        
        created_customer.put()
        
        return created_customer
    
    @classmethod
    def list_merchant_customer(cls, merchant_acct, offset=0):
        query = cls.query(ndb.AND(cls.merchant_acct==merchant_acct.create_ndb_key()))
        
        return cls.list_all_with_condition_query(query, offset)
    
    @classmethod
    def count_merchant_customer(cls, merchant_acct, offset=0, ):
        query = cls.query(ndb.AND(cls.merchant_acct==merchant_acct.create_ndb_key()))
        
        return cls.count_with_condition_query(query)
    
    @classmethod
    def search_merchant_customer(cls, merchant_acct, name=None, email=None, mobile_phone=None, 
                                 offset=0, start_cursor=None, limit=model_conf.MAX_FETCH_RECORD):
        
        query = cls.query(ndb.AND(cls.merchant_acct==merchant_acct.create_ndb_key()))
        
        if is_not_empty(email):
            query = query.filter(cls.email==email)
            
        elif is_not_empty(mobile_phone):
            query = query.filter(cls.mobile_phone==mobile_phone)
        
            
        if is_not_empty(name):
            search_text_list = name.split(' ')
        else:
            search_text_list = None
        
        total_count                         = cls.full_text_count(search_text_list, query, limit)
        
        (search_results, next_cursor)       = cls.full_text_search(search_text_list, query, offset=offset, 
                                                                   start_cursor=start_cursor, return_with_cursor=True, 
                                                                   limit=limit)
        
        return (search_results, total_count, next_cursor)
    
  
    