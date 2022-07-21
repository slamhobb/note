select
    id,
    user_id,
    birth_date,
    name
    from birthday
    where abs(strftime('%m', birth_date)) = :month
        and abs(strftime('%d', birth_date)) = :day;
