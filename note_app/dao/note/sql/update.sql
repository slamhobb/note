update note
    set text = :text,
        note_type_id = :note_type_id,
        modify_date = :modify_date
    where user_id = :user_id
        and id = :id;
