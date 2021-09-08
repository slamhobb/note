delete from auth_token
    where user_id = :user_id
        and token = :token;
