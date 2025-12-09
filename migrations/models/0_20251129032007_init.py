from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "guild" (
    "guild_id" VARCHAR(32) NOT NULL PRIMARY KEY,
    "name" VARCHAR(200) NOT NULL,
    "joined_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "guild_settings" (
    "prefix" VARCHAR(5) NOT NULL DEFAULT '.',
    "language" VARCHAR(10) NOT NULL DEFAULT 'en',
    "modlog_channelid" VARCHAR(32),
    "suggestion_channelid" VARCHAR(32),
    "guild_id" VARCHAR(32) NOT NULL PRIMARY KEY REFERENCES "guild" ("guild_id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "mod_logs" (
    "case_id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "target_id" VARCHAR(32) NOT NULL,
    "mod_id" VARCHAR(32) NOT NULL,
    "action" VARCHAR(20) NOT NULL,
    "reason" TEXT NOT NULL,
    "timestamp" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "guild_id" VARCHAR(32) NOT NULL REFERENCES "guild" ("guild_id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztmW1P2zAQx79KlVcgMUQDBbR3BcrWAe0E2YaYpsgk1zQjsUPsjFao3322mzTPaQMF2o"
    "030Jx9ju/n2PfP5VFxiQkO3f4U2I6pfGw8Khi5wH+kG7YaCvK82CwMDN06sqc163JLmY8M"
    "xo0D5FDgJhOo4dseswnmVhw4jjASg3e0sRWbAmzfB6AzYgEbgs8bfv7iZhubMAIaXXp3+s"
    "CGzETl7XVbzkC26mzsyZbjIfJPZX9x01vdIE7g4qyPN2ZDgmdOfGbCagEGHzEwE8GIuYZB"
    "R6bpvLmB+QHMJmzGBhMGKHBYIvgFiRgEC5o2ZlSG66KR7gC22JBf7qqTaUhxwNNeIoLv7c"
    "vjz+3LjV11U0RC+JJMF6oXtqiyaSKHQAxNB5GQY6ryfw2iUf/l0IwMMc74gXoJnurOzgJA"
    "ea9SorJNII0R/iY2BlNHLM/xhLNgtgvFLFOOGaBm6Lkd/VhRvD4gs4+dcbgTKuhq3YvOld"
    "a++CoicSm9dyShttYRLaq0jjPWjf3MQswGafzoap8b4rJx0+91JEFCmeXLO8b9tBtFzAkF"
    "jOiYPOjITGzayBqBmYjDZ3CX2CjCcIuMuwfkm3qqJXWC6g6xKM2v/1Hoenp2CQ6ScPNLHZ"
    "7AF8Q856Os5jpPomc3skbrLQARlZQhSzfFzCgwxu9XgayPQSP8z3xwMnVdJQacgy9c/FWh"
    "56puhp6LMLLkRMRwwrkw0rIsnkQxJ5vryXV4T+v/Tlr3fBjYozpMY4/XS+3KtrIspK0FiL"
    "ZKgbayOd1B2Ar4JqxDMOnzigwBLw1icxF11CwXR82cNuIHD0+NujFEGINTb5cX+T6J6+sf"
    "+C+z3RPpM7AsoGJWT0Nb5v8f460h/fKaJ5PO8ksRqRm5HF0eDMJG0UGRfRtftTxWpmS42U"
    "cPs/SeytA8PB4UsOkz2b46bp90lEmFTKypiiLhXKCHEpq6XAlF+v3tNJCBKBRKoC5mxRs4"
    "4ZF5gsSaZB6ccIHeVP9Y4i4f1Obewd7h7v7eIe8iZzKzHFRs4m5Pm6N3GPI59poyMuW0ng"
    "WN5acWsRtq5+l3himG/AAJ31gXZRh7rCdDdbG6WkVZLcvQB0SLGGowKjkTY491YVhVLetc"
    "a6lCWcRq46J9vZkqlp33e5+i7gm2x+f9owxTUUfk0sP16lYqU47vlcoVqFRurVwJZT2P7Z"
    "zsnyvlT4kPtoXPYPzSYv7tCpPPlPNz3paWJ/3b4NvGUClQ/mFLpfBHcZ83kf21FP+72J9x"
    "+wM+ramvEi7redqprUUqnLxXucRq5aqcYmvUEaleUf5fE4DNhT79Nis+/Tbzn375HRnggg"
    "+/X676vZI399glA/Ib5gH+NG2DbTUcm7Jfq4m1gqKIulq0ZvVpRgyJAY6eW4x7bnqZ/AXG"
    "U1S3"
)
