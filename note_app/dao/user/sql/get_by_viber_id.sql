select
    id,
    login,
    viber_id,
    telegram_id
    from user
    where viber_id = :viber_id;
