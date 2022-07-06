select
    id,
    user_id,
    birth_date,
    name
    from birthday
    where user_id = :user_id;
