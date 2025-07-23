\c postgres
CREATE EXTENSION IF NOT EXISTS dblink;
DO
$$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'reward_tasks') THEN
            PERFORM dblink_exec('dbname=postgres user=' || current_user, 'CREATE DATABASE reward_tasks');
        END IF;
    END
$$;
\c auth