
create table apys
(
    index          bigint,
    platform       text,
    chain_name     text,
    pool_address   text,
    datetime_crawl timestamp,
    auto_compound  boolean,
    apr            double precision,
    lp_token_value double precision
);

create index ix_apys_index
    on apys (index);