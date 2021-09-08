select
    id,
    user_id,
    text,
    note_type_id,
    create_date,
    modify_date
    from note
    where user_id = :user_id
        and id = :id;
