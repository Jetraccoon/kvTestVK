box.cfg{}

local space_name = 'users'
local space = box.space[space_name]
if space == nil then
    local users_space = box.schema.space.create('users', {
        format = {
            {name = 'user_id', type = 'unsigned'},
            {name = 'username', type = 'string'},
            {name = 'password', type = 'string'},
        }
    })

    users_space:create_index('primary', {
        parts = {'user_id'}
    })

    users_space:create_index('username', {
        unique = true,
        parts = {'username'}
    })

    local username = 'admin'
    local password = 'presale'

    local user_id = users_space:count() + 1
    users_space:insert{user_id, username, password}
else
    print('Space ' .. space_name .. ' already exists.')
end
local kv_store_space_name = 'kv_store'
local kv_store_space = box.space[kv_store_space_name]
if kv_store_space == nil then
    print('Creating space ' .. kv_store_space_name)
    local kv_store_space = box.schema.space.create('kv_store', {
        format = {
            {name = 'key', type = 'string'},
            {name = 'value', type = 'string'},
        }
    })
    kv_store_space:create_index('primary', {
        parts = {'key'}
    })
else
    print('Space ' .. kv_store_space_name .. ' already exists.')
end