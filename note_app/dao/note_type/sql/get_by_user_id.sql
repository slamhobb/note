select
    id,
    user_id,
    name
    from note_type
    where user_id = :user_id
        or user_id = 0;
