__author__ = 'Ted Nyman'
__version__ = '0.1.0'
__license__ = 'MIT'

from bottle import route, request, response, view, send_file, run
import redis
import bottle
import string

# Bottle debug - remove in production!
bottle.debug(True)

# The main redis object
r = redis.Redis()

# returned_value defaults to empty string
returned_value = ""

# search result defaults to empty string
search_result = ""

# Set static file routing
@route('/static/:filename')
def static_file(filename):
    send_file(filename, root='../redweb/static')



# Home route
@route('/')
@view('central')
def template_keyvalue():
   db_size = r.dbsize()
  
   return dict(returned_value=returned_value, db_size=db_size, search_result=search_result)

"""
Actions for all data types
"""
 
@route('/delete/', method='POST')
@view('central')
def template_delete():

    key_delete = request.POST.get('key_delete', '').strip()
    r.delete(key_delete)
    db_size = r.dbsize()
	   
    return dict(db_size = db_size, returned_value=returned_value, search_result=search_result, key=key_delete)

@route('/delete/all/', method='POST')
@view('central')
def template_delete_all():

    delete_all = request.POST.get('delete_all', '').strip()
    r.flushdb()
    db_size = r.dbsize()

    return dict(db_size=db_size, search_result=search_result)

@route('/search/', method='POST')
@view('central')
def template_search():
    key = request.POST.get('key', '').strip()
    search_result = r.keys(key)
    db_size = r.dbsize()

    return dict(db_size=db_size, returned_value=returned_value, search_result=search_result)


"""
Strings
""" 

# SET | set a string value for a given key
@route('/strings/set/', method='POST')
@view('central')
def template_strings_set():
    key = request.POST.get('key', '').strip()
    value = request.POST.get('value', '').strip()
    r.set(key,value)
    db_size = r.dbsize()
 
    return dict(key=key, value=value, returned_value=returned_value, db_size=db_size, search_result=search_result)


# GET | return the string value of a key
@route('/strings/get/', method='POST')
@view('central')
def template_string_get():
    key = request.POST.get('key', '').strip()
    returned_value = r.get(key)	
    db_size = r.dbsize()
	
    return dict(key=key, returned_value=returned_value,  db_size=db_size, search_result=search_result)	


"""
Lists

"""

# RPUSH | append an element to the tail of a list
@route('/lists/rightpush/', method='POST')
@view('central')
def template_lists_rightpush():
    key = request.POST.get('key', '').strip()
    element = request.POST.get('element', '').strip()
    r.push(key,element)
    db_size = r.dbsize()
 
    return dict(key=key, element=element, returned_value=returned_value, db_size=db_size, search_result=search_result)


# LPUSH | append an element to the head of a list
@route('/lists/leftpush/', method='POST')
@view('central')
def template_lists_leftpush():
    key = request.POST.get('key', '').strip()
    element = request.POST.get('element', '').strip()
    r.push(key,element, tail=True)
    db_size = r.dbsize()
 
    return dict(key=key, element=element, returned_value=returned_value, db_size=db_size, search_result=search_result)


# LLEN | return the length of a list
@route('/lists/length/', method='POST')
@view('central')
def template_lists_length():
    key = request.POST.get('key', '').strip()
    llen = r.llen(key)
    db_size = r.dbsize()

    return dict(key=key, returned_value=llen, db_size=db_size, search_result=search_result)


# LRANGE | return a range of elements from a list
@route('/lists/range/', method='POST')
@view('central')
def template_lists_range():
    key = request.POST.get('key', '').strip()
    start = request.POST.get('start', '').strip()
    end = request.POST.get('end', '').strip()
    list_range = r.lrange(key, start, end)
    db_size = r.dbsize()

    return dict(key=key, list_range=list_range, returned_value=returned_value, db_size=db_size, search_result=search_result)

# LTRIM
# LINDEX
# LSET
# LREM


# LPOP | return and remove the first element of a list
@route('/lists/leftpop/', method='POST')
@view('central')
def template_lists_lpop():
    key = request.POST.get('key', '').strip()
    left_pop = r.pop(key)
    db_size = r.dbsize()

    return dict(key=key, returned_value=left_pop, db_size=db_size, search_result=search_result)


# RPOP | return and remove the last element of a list
@route('/lists/rightpop/', method='POST')
@view('central')
def template_lists_rpop():
    key = request.POST.get('key', '').strip()
    right_pop = r.pop(key, tail=True)
    db_size = r.dbsize()

    return dict(key=key, returned_value=right_pop, db_size=db_size, search_result=search_result)

# BLPOP
# BRPOP
# RPOPLPPUSH


"""
Sets
"""

# SADD | add a member to a set
@route('/sets/add/', method='POST')
@view('central')
def template_sets_add():
    key = request.POST.get('key', '').strip()
    member = request.POST.get('member', '').strip()
    set_add = r.sadd(key, member)
    db_size = r.dbsize()  
 
    return dict(key=key, member=member, returned_value=returned_value, db_size=db_size, search_result=search_result)      


# SREM | remove a member of a set
@route('/sets/remove/', method='POST')
@view('central')
def template_sets_remove():
    key = request.POST.get('key', '').strip()
    member = request.POST.get('member', '').strip()
    set_remove = r.srem(key, member)
    db_size = r.dbsize()  
  
    return dict(key=key, member=member, returned_value=returned_value, db_size=db_size, search_result=search_result)      


# SPOP
# SMOVE

# SCARD | return the cardinality for a set
@route('/sets/cardinality/', method='POST')
@view('central')
def template_sets_cardinality():
    key = request.POST.get('key', '').strip() 
    cardinality = r.scard(key)
    db_size = r.dbsize()

    return dict(key=key, returned_value=cardinality, db_size=db_size, search_result=search_result)

# SISMEMBER

# SINTER | for any number of sets, return the values that those sets all share
@route('/sets/intersection/', method='POST')
@view('central')
def template_sets_intersection():
    key = request.POST.get('key', '').strip()
    keys = string.split(key, ',')
    tuple_keys = tuple(keys)
    intersection = r.sinter('%s' % ' '.join(tuple_keys))
    db_size = r.dbsize()
  
    return dict(key=key, returned_value=intersection, db_size=db_size, search_result=search_result)


# SINTERSTORE

# SUNION
@route('/sets/union/', method='POST')
@view('central')
def template_sets_union():
    key = request.POST.get('key', '').strip()
    keys = string.split(key, ',')
    tuple_keys = tuple(keys)
    union = r.sunion('%s' % ' '.join(tuple_keys))
    db_size = r.dbsize()
  
    return dict(key=key, returned_value=union, db_size=db_size, search_result=search_result)


# SUNIONSTORE
# SDIFF
# SDIFFSTORE

# SMEMBERS | return all members of a set
@route('/sets/members/', method='POST')
@view('central')
def template_sets_members():
    key = request.POST.get('key', '').strip()
    members = r.smembers(key)
    db_size = r.dbsize()
  
    return dict(key=key, returned_value=members, db_size=db_size, search_result=search_result)


# SRANDMEMBER | return a random member of set, without removing it
@route('/sets/random/', method='POST')
@view('central')
def template_sets_srandom():
    key = request.POST.get('key', '').strip()
    random_member = r.srandmember(key)
    db_size = r.dbsize()
  
    return dict(key=key, returned_value=random_member, db_size=db_size, search_result=search_result)


"""
Sorted Sets
"""

# ZADD | add a member to a sorted set
@route('/zsets/add/', method='POST')
@view('central')
def template_zsets_add():
    key = request.POST.get('key', '').strip()
    member = request.POST.get('member', '').strip()
    score = request.POST.get('score', '').strip()
    zset_add = r.zadd(key, member, score)
    db_size = r.dbsize()  
 
    return dict(key=key, member=member, score=score, returned_value=returned_value, db_size=db_size, search_result=search_result)      


# ZREM | remove a member of a sorted set
@route('/zsets/remove/', method='POST')
@view('central')
def template_zsets_remove():
    key = request.POST.get('key', '').strip()
    member = request.POST.get('member', '').strip()
    zset_remove = r.zrem(key, member)
    db_size = r.dbsize()  
  
    return dict(key=key, member=member, returned_value=returned_value, db_size=db_size, search_result=search_result)      

# ZINCRBY
# ZCRANGE
# ZREVRANGE
# ZRANGEBYSCORE

# ZCARD | return the cardinality for a set
@route('/zsets/cardinality/', method='POST')
@view('central')
def template_zsets_cardinality():
    key = request.POST.get('key', '').strip() 
    cardinality = r.zcard(key)
    db_size = r.dbsize()

    return dict(key=key, returned_value=cardinality, db_size=db_size, search_result=search_result)

# ZSCORE
# ZREMRANGEBYSCORE


"""
Sorting, Persistence, Remote Server
"""

# SORT

# BGSAVE
# LASTSAVE
# SHUTDOWN
# BGREWRITEAOF

# INFO
# MONITOR
# SLAVE

#run it!
run()
