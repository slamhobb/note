insert into note(
    user_id,
    text,
    note_type_id,
    create_date,
    modify_date)
    values(
        :user_id,
        :text,
        :note_type_id,
        :create_date,
        :modify_date);
