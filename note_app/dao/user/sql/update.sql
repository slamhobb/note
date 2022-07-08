update user
    set viber_id = :viber_id,
        telegram_id = :telegram_id
    where id = :id;
   