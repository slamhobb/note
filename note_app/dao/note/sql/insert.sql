insert into note(
    user_id,
    text,
    note_type_id,
    create_date,
    modify_date,
    hidden)
    values(
        :user_id,
        :text,
        :note_type_id,
        :create_date,
        :modify_date,
        :hidden);
