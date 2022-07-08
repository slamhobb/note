select
    id,
    login,
    viber_id,
    telegram_id
    from user
    where login = :login;
