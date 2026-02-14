from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "guild" (
    "guild_id" VARCHAR(32) NOT NULL PRIMARY KEY,
    "name" VARCHAR(200) NOT NULL,
    "joined_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
        CREATE TABLE IF NOT EXISTS "mod_logs" (
    "case_id" SERIAL NOT NULL PRIMARY KEY,
    "target_id" VARCHAR(32) NOT NULL,
    "mod_id" VARCHAR(32) NOT NULL,
    "action" VARCHAR(20) NOT NULL,
    "reason" TEXT NOT NULL,
    "timestamp" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "resolved" BOOL NOT NULL DEFAULT False,
    "guild_id" VARCHAR(32) NOT NULL REFERENCES "guild" ("guild_id") ON DELETE CASCADE
);
        ALTER TABLE "guild_settings" DROP COLUMN "suggestion_channelid";
        DROP TABLE IF EXISTS "web_sessions";
        ALTER TABLE "guild_settings" ADD CONSTRAINT "fk_guild_se_guild_199bfc55" FOREIGN KEY ("guild_id") REFERENCES "guild" ("guild_id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "guild_settings" DROP CONSTRAINT IF EXISTS "fk_guild_se_guild_199bfc55";
        ALTER TABLE "guild_settings" ADD "suggestion_channelid" VARCHAR(32);
        DROP TABLE IF EXISTS "guild";
        DROP TABLE IF EXISTS "mod_logs";"""


MODELS_STATE = (
    "eJztmVtvmzAUgP9KxFMnddVCm23aW9KlW7YmmVp20aYJOXBCWI2dgVkbTfnvsx0IYC6BNW"
    "2TrS9tOPYBn+9gnwu/NY/agIOjN6GLbe1V67dGkAf8R3bgsKWh+TwRCwFDEyxnOuspk4D5"
    "yGJcOEU4AC6yIbB8d85cSriUhBgLIbX4RJc4iSgk7s8QTEYdYDPw+cC371zsEhtuIIgv51"
    "fm1AVlofLxpitXIEdNtpjLkdMZ8s/kfPHQiWlRHHpE1Zkv2IyStRJfmZA6QMBHDOyUMWKt"
    "kdGxaLVuLmB+COsF24nAhikKMUsZX5OIRYmg6RIWSHM9dGNiIA6b8ctjfbkyKTF4NUtY8K"
    "l7cfq2e3FwrD8RllDukpWjRtGILoeW8haIodVNJOSEqvzfgGg8fzs0Y0GCM3mh7oKn/uxZ"
    "DaB8VilROSaQJgh/UJeAbSKW5/ias2CuB8UsM4oKUDvSPIp/7CheH5A9JngR7YQKusZg2L"
    "80usMPwhIvCH5iSahr9MWILqULRXrwXHHE+iatzwPjbUtctr6OR31JkAbM8eUTk3nGV02s"
    "CYWMmoRem8hObdpYGoNZisNnepXaKEIwQdbVNfJtMzOSOUFNTJ0gyPu/F6mevb8AjCTcvK"
    "ujE3hI7XN+l9308zJ+d2Np7G8BiOq0DFl2KGEWAGP8eRXIxgQMyv9sBidD12XqhhvwRc7f"
    "FXqe7in0PESQIxcibieUCy0ti+JpFBuiuZn2w2NY/3fC+tyHqXvThGmicX+hXTvStoW0U4"
    "NopxRoR43pGBEn5JuwCcG0zj0yBLI1iO062VG7PDlq53IjfvDw0GhaM0QI4Ga7vEj3r7je"
    "/4F/N9s9wcqPdUD477AW6f7HWBukfPlcRwljeTfEWYx0xYAbg4hVdECoVfiuxa+yDIaLfX"
    "S9DuuZyMzN40YBW72P3cvT7uu+tqxIDxtmQ3HCXJAHpXLp8gwoztsfLvexUACFqc+AsOLN"
    "m9JQ3iDhE+XFiRz0oHmPI57yVG+fvDh5efz85CWfIleylryo2MSDkbEhz2HI59gbpo8Zpf"
    "1sZGw/pIjd0Dg+PzLMhmUrrlRrB2OrpLbdE4Z6vX5aRTtNZegDCooYGnBTciYmGvvCsKpL"
    "1v9iZBpkMauDYffLk0yT7Hw8ehNPT7E9PR/3FKaif8hTD2/etEOZUXzsUO5AhzK7VQKKf0"
    "HBod2jFAMiZfslUVN8OuF6d+XGpnlV/T3TG4/PMy7rDdRN8XHY6/PSVfqKT3JXSWmcX+xa"
    "N2o/I2GuktpYHZ1RH1yHvIfFXddHD9fjPbxdhbShAN1eNdUF37VmWkExFY0cVtVSKJnzIJ"
    "VUoyLqsX5ac/sFftAwZU2p7Odpp3fqNIv5rPKstZNrGIut0QBiNH0/AbZrfUVvV3xFb+e/"
    "ovMnMiAF39DfXY5HJc2QREUB+ZFwA7/ZrsUOW9gN2PfdxFpBUVhdXQeoKb+SX4ob9G7b37"
    "xteFn+Ae1OvQ4="
)
