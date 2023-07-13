import requests, os

BASE_URL = os.getenv('MEMO_URL').split('/memo?')[0]
OPENID = os.getenv('MEMO_URL').split('/memo')[1]

def get_system_status():
    return requests.get(f"{BASE_URL}/status" + OPENID)

def get_system_setting():
    return requests.get(f"{BASE_URL}/system/setting" + OPENID)

def upsert_system_setting(system_setting):
    return requests.post(f"{BASE_URL}/system/setting" + OPENID, json=system_setting)

def vacuum_database():
    return requests.post(f"{BASE_URL}/system/vacuum" + OPENID)

def signin(username, password):
    data = {
        "username": username,
        "password": password
    }
    return requests.post(f"{BASE_URL}/auth/signin" + OPENID, json=data)

def signin_with_sso(identity_provider_id, code, redirect_uri):
    data = {
        "identityProviderId": identity_provider_id,
        "code": code,
        "redirectUri": redirect_uri
    }
    return requests.post(f"{BASE_URL}/auth/signin/sso" + OPENID, json=data)

def signup(username, password):
    data = {
        "username": username,
        "password": password
    }
    return requests.post(f"{BASE_URL}/auth/signup" + OPENID, json=data)

def signout():
    return requests.post(f"{BASE_URL}/auth/signout" + OPENID)

def create_user(user_create):
    return requests.post(f"{BASE_URL}/user" + OPENID, json=user_create)

def get_myself_user():
    return requests.get(f"{BASE_URL}/user/me" + OPENID)

def get_user_list():
    return requests.get(f"{BASE_URL}/user" + OPENID)

def get_user_by_id(id):
    return requests.get(f"{BASE_URL}/user/{id}" + OPENID)

def upsert_user_setting(upsert):
    return requests.post(f"{BASE_URL}/user/setting" + OPENID, json=upsert)

def patch_user(user_patch):
    return requests.patch(f"{BASE_URL}/user/{user_patch['id']}" + OPENID, json=user_patch)

def delete_user(user_delete):
    return requests.delete(f"{BASE_URL}/user/{user_delete['id']}" + OPENID)

def get_all_memos(memo_find=None):
    query_list = []
    if memo_find and memo_find.get("offset"):
        query_list.append(f"offset={memo_find['offset']}")
    if memo_find and memo_find.get("limit"):
        query_list.append(f"limit={memo_find['limit']}")
    query_string = "&".join(query_list)
    url = f"{BASE_URL}/memo{OPENID}&{query_string}" if query_string else f"{BASE_URL}/memo{OPENID}"
    return requests.get(url)

def get_memo_list(memo_find=None):
    query_list = []
    if memo_find and memo_find.get("creatorId"):
        query_list.append(f"creatorId={memo_find['creatorId']}")
    if memo_find and memo_find.get("rowStatus"):
        query_list.append(f"rowStatus={memo_find['rowStatus']}")
    if memo_find and memo_find.get("pinned"):
        query_list.append(f"pinned={memo_find['pinned']}")
    if memo_find and memo_find.get("offset"):
        query_list.append(f"offset={memo_find['offset']}")
    if memo_find and memo_find.get("limit"):
        query_list.append(f"limit={memo_find['limit']}")
    query_string = "&".join(query_list)
    url = f"{BASE_URL}/memo{OPENID}{query_string}" if query_string else f"{BASE_URL}/memo" + OPENID
    return requests.get(url)

def get_memo_stats(user_id):
    return requests.get(f"{BASE_URL}/memo{OPENID}&creatorId={user_id}/stats")

def get_memo_by_id(id):
    return requests.get(f"{BASE_URL}/memo/{id}{OPENID}")

def create_memo(memo_create):
    return requests.post(f"{BASE_URL}/memo" + OPENID, json=memo_create)

def patch_memo(memo_patch):
    return requests.patch(f"{BASE_URL}/memo/{memo_patch['id']}" + OPENID, json=memo_patch)

def pin_memo(memo_id):
    data = {
        "pinned": True
    }
    return requests.post(f"{BASE_URL}/memo/{memo_id}/organizer" + OPENID, json=data)

def unpin_memo(memo_id):
    data = {
        "pinned": False
    }
    return requests.post(f"{BASE_URL}/memo/{memo_id}/organizer" + OPENID, json=data)

def delete_memo(memo_id):
    return requests.delete(f"{BASE_URL}/memo/{memo_id}" + OPENID)

def get_shortcut_list(shortcut_find=None):
    query_list = []
    if shortcut_find and shortcut_find.get("creatorId"):
        query_list.append(f"creatorId={shortcut_find['creatorId']}")
    query_string = "&".join(query_list)
    url = f"{BASE_URL}/shortcut?{query_string}" + OPENID if query_string else f"{BASE_URL}/shortcut" + OPENID
    return requests.get(url)

def create_shortcut(shortcut_create):
    return requests.post(f"{BASE_URL}/shortcut" + OPENID, json=shortcut_create)

def patch_shortcut(shortcut_patch):
    return requests.patch(f"{BASE_URL}/shortcut/{shortcut_patch['id']}" + OPENID, json=shortcut_patch)

def delete_shortcut_by_id(shortcut_id):
    return requests.delete(f"{BASE_URL}/shortcut/{shortcut_id}" + OPENID)

def get_resource_list():
    return requests.get(f"{BASE_URL}/resource" + OPENID)

def get_resource_list_with_limit(resource_find=None):
    query_list = []
    if resource_find and resource_find.get("offset"):
        query_list.append(f"offset={resource_find['offset']}")
    if resource_find and resource_find.get("limit"):
        query_list.append(f"limit={resource_find['limit']}")
    query_string = "&".join(query_list)
    url = f"{BASE_URL}/resource?{query_string}" + OPENID if query_string else f"{BASE_URL}/resource" + OPENID
    return requests.get(url)

def create_resource(resource_create):
    return requests.post(f"{BASE_URL}/resource" + OPENID, json=resource_create)

def create_resource_with_blob(form_data):
    return requests.post(f"{BASE_URL}/resource/blob" + OPENID, files=form_data)

def patch_resource(resource_patch):
    return requests.patch(f"{BASE_URL}/resource/{resource_patch['id']}" + OPENID, json=resource_patch)

def delete_resource_by_id(id):
    return requests.delete(f"{BASE_URL}/resource/{id}" + OPENID)

def get_memo_resource_list(memo_id):
    return requests.get(f"{BASE_URL}/memo/{memo_id}/resource" + OPENID)

def upsert_memo_resource(memo_id, resource_id):
    data = {
        "resourceId": resource_id
    }
    return requests.post(f"{BASE_URL}/memo/{memo_id}/resource" + OPENID, json=data)

def delete_memo_resource(memo_id, resource_id):
    return requests.delete(f"{BASE_URL}/memo/{memo_id}/resource/{resource_id}" + OPENID)

def get_tag_list(tag_find=None):
    query_list = []
    if tag_find and tag_find.get("creatorId"):
        query_list.append(f"creatorId={tag_find['creatorId']}")
    query_string = "&".join(query_list)
    url = f"{BASE_URL}/tag?{query_string}" + OPENID if query_string else f"{BASE_URL}/tag" + OPENID
    return requests.get(url)

def get_tag_suggestion_list():
    return requests.get(f"{BASE_URL}/tag/suggestion" + OPENID)

def upsert_tag(tag_name):
    data = {
        "name": tag_name
    }
    return requests.post(f"{BASE_URL}/tag" + OPENID, json=data)

def delete_tag(tag_name):
    data = {
        "name": tag_name
    }
    return requests.post(f"{BASE_URL}/tag/delete" + OPENID, json=data)

def get_storage_list():
    return requests.get(f"{BASE_URL}/storage" + OPENID)

def create_storage(storage_create):
    return requests.post(f"{BASE_URL}/storage" + OPENID, json=storage_create)

def patch_storage(storage_patch):
    return requests.patch(f"{BASE_URL}/storage/{storage_patch['id']}" + OPENID, json=storage_patch)

def delete_storage(storage_id):
    return requests.delete(f"{BASE_URL}/storage/{storage_id}" + OPENID)

def get_identity_provider_list():
    return requests.get(f"{BASE_URL}/idp" + OPENID)

def create_identity_provider(identity_provider_create):
    return requests.post(f"{BASE_URL}/idp" + OPENID, json=identity_provider_create)

def patch_identity_provider(identity_provider_patch):
    return requests.patch(f"{BASE_URL}/idp/{identity_provider_patch['id']}" + OPENID, json=identity_provider_patch)

def delete_identity_provider(id):
    return requests.delete(f"{BASE_URL}/idp/{id}" + OPENID)


