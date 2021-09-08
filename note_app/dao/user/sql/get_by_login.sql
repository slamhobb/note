select
    id,
    login,
    viber_id
    from user
    where login = :login;
