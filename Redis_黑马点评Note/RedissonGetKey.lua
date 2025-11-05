local key = KEYS[1];
local threadId = ARGV[1];
local releaseTime = ARGV[2];

if (redis.call('exists', key) == 0) then
    -- 不存在，获取锁
    redis.call('hset', key, threadId, '1');
    -- 设置有效期
    redis.call('expire', key, ,releaseTime);
    return 1;
end;

-- 锁已经存在，判断threadId是否是自己
if (redis.call('hexists', key, threadId) == 1) then

    -- 存在，获取锁，重入次数 + 1
    redis.call('hincrby', key, threadId, '1');

    -- 设置有效期
    redis.call('expire', key, releaseTime);

    return 1;
end;

-- fail to get the key, because the key isn't myself
return 0;