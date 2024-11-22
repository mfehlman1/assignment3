"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_user_email

url_signer = URLSigner(session)

@action('index')
@action.uses('index.html', db, session, auth.user)
def index():
    return dict(
        # For example...
        load_data_url=URL('load_data', signer=url_signer), 
        # Add other things here.
        add_item_url= URL('add_item', signer=url_signer),
        update_item_url = URL('update_item', signer=url_signer),
        delete_item_url = URL('delete_item', signer=url_signer)
    )

@action('load_data')
@action.uses(db, auth.user)
def load_data():
    # Complete.
    items = db(db.shopping_list.user_id == auth.current_user.get('id')).select(orderby=[db.shopping_list.is_purchased, ~db.shopping_list.id])
    return dict(items=items.as_list())

# You can add other controllers here.
@action('add_item', method=['POST'])
@action.uses(db, auth.user)
def add_item():
    item_name = request.json.get('item_name')
    if item_name:
        item_id = db.shopping_list.insert(item_name=item_name, user_id=auth.current_user.get('id'))
        db.commit()
        return dict(status='success', item_id=item_id, message='Item added successfully') 
    else:
        return dict(status='error', message='Please insert an item with its name')

@action('update_item', method=['POST'])
@action.uses(db, auth.user)
def update_item():
    item_id = request.json.get('item_id')
    is_purchased = request.json.get('is_purchased')
    if item_id is not None and is_purchased is not None:
        db(db.shopping_list.id == item_id).update(is_purchased=is_purchased)
        db.commit()
        return dict(status='success', message='Item updated successfully')
    else:
        return dict(status='error',message='Incorrect item id or purchase status')


@action('delete_item', method=['POST'])
@action.uses(db, auth.user)
def delete_item():
    item_id = request.json.get('item_id')
    if item_id:
        db(db.shopping_list.id == item_id).delete()
        db.commit()
        return dict(status='success', message='Item deleted successfully')
    else:
        return dict(status='error', message='Incorrect item id')