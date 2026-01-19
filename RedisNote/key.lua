-- 锁的key
local key = KEYS[1]

-- 当前线程标识
local threadId = ARGV[1]

-- 获取锁中的线程标识 get key
local id = redis.call('get', key)

-- compare the threadId and the id

if (id == threadId) then
    -- 如果一致，就释放 del key
    return redis.call('del', key)
end

return 0