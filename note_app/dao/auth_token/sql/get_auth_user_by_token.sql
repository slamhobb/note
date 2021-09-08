select
    t.user_id,
    u.login
    from auth_token as t
        join user as u on
            t.user_id = u.id
    where t.token = :token;
