import warnings

import redis
import fakeredis
from typing import Optional

from redis.client import Script
from redis.exceptions import NoScriptError

from redorm.settings import REDORM_URL

GET_SET_INDIRECT = """
local l = {}
local keys = redis.call('smembers', KEYS[2])
for _,k in ipairs(keys) do
    table.insert(l, redis.call('get', KEYS[1] .. k))
end
return l
"""

GET_KEY_INDIRECT = """
return {redis.call('get', redis.call('get', KEYS[1]))}
"""

UNIQUE_SAVE = """
local uniquecnt = ARGV[1]
local uniquenullcnt = ARGV[2]
local indexcnt = ARGV[3]
local indexnullcnt = ARGV[4]
local data = ARGV[5]
local uuid = ARGV[6]
local clsname = ARGV[7]

local beginunique = 8
local endofunique = beginunique+(uniquecnt*3)-1
-- Check uniqueness constraints, triples of field name, old value, new value
for i=beginunique,endofunique,3 do
     if redis.call('hexists', clsname .. ':key:' .. ARGV[i], ARGV[i+2]) == 1 then
         return redis.error_reply('Unique Violation: ' .. ARGV[i])
     end
end

-- Update unique hash maps
for i=beginunique,endofunique,3 do
    redis.call('hdel', clsname .. ':key:' .. ARGV[i], ARGV[i+1])
    redis.call('hset', clsname .. ':key:' .. ARGV[i], ARGV[i+2], uuid)
    redis.call('srem', clsname .. ':keynull:' .. ARGV[i], uuid)
end

local beginuniquenull = endofunique + 1
local endofuniquenull = beginuniquenull+(uniquenullcnt*2)-1
-- Update unique hash maps, pairs of field name, old value
for i=beginuniquenull,endofuniquenull,2 do
    redis.call('hdel', clsname .. ':key:' .. ARGV[i], ARGV[i+1])
    redis.call('sadd', clsname .. ':keynull:' .. ARGV[i], uuid)
end

local beginindex = endofuniquenull + 1
local endofindex = beginindex+(indexcnt*3)-1
-- Update index sets, triples of field name, old value, new value
for i=beginindex,endofindex,3 do
    -- Remove from old index
    redis.call('srem', clsname .. ':index:' .. ARGV[i] .. ':' .. ARGV[i+1], uuid)
    -- Remove from old null index in case was null
    redis.call('srem', clsname .. ':indexnull:' .. ARGV[i], uuid)
    -- Add to new index
    redis.call('sadd', clsname .. ':index:' .. ARGV[i] .. ':' .. ARGV[i+2], uuid)
end

local beginindexnull = endofindex + 1
local endofindexnull = beginindexnull+(indexnullcnt*2)-1
-- Update unique hash maps, pairs of field name, old value
for i=beginindexnull,endofindexnull,2 do
    -- Remove from old index
    redis.call('srem', clsname .. ':index:' .. ARGV[i] .. ':' .. ARGV[i+1], uuid)
    -- Add to null index
    redis.call('sadd', clsname .. ':indexnull:' .. ARGV[i], uuid)
end
redis.call('set', clsname .. ':member:' .. uuid, data)
redis.call('sadd', clsname .. ':all', uuid)
"""


class RedormClient:
    pool: redis.ConnectionPool
    client: redis.Redis
    get_set_indirect_script: Script
    get_key_indirect_script: Script
    unique_save_script: Script

    def __init__(self, redorm_url=REDORM_URL):
        self.server = None
        self.bind(redorm_url)

    def bind(self, url):
        if url:
            self.client = redis.Redis.from_url(url, decode_responses=True)
        else:
            warnings.warn(
                "Redorm was not provided a Redis URL and will fall back to the in-built incredibly slow fake redis. "
                "Set REDORM_URL environment variable to fix.",
                RuntimeWarning,
            )
            # Fake redis for developement
            self.client = fakeredis.FakeRedis(decode_responses=True)
        self.setup_scripts()

    def setup_scripts(self):
        self.get_key_indirect_script = self.client.register_script(GET_KEY_INDIRECT)
        self.get_set_indirect_script = self.client.register_script(GET_SET_INDIRECT)
        self.unique_save_script = self.client.register_script(UNIQUE_SAVE)

    def init_app(self, app):
        url = app.config.get("REDORM_URL")
        if url:
            self.bind(url)

    def unique_save(self, *args):
        try:
            return self.client.evalsha(self.unique_save_script.sha, *args)
        except NoScriptError:
            return self.client.eval(UNIQUE_SAVE, *args)


red = RedormClient()
