update birthday
    set birth_date = @birth_date,
        name = @name
    where id = :id
        and user_id = :user_id;
