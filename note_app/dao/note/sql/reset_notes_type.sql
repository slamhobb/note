update note
    set note_type_id = 1,
        modify_date = :date
    where user_id = :user_id
        and note_type_id = :note_type_id;
