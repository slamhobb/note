select
    id,
    login,
    viber_id,
    telegram_id
    from user
    where telegram_id = :telegram_id;
