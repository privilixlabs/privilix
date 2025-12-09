from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "feature_settings" (
    "suggestions" INT NOT NULL DEFAULT 0,
    "modlogs" INT NOT NULL DEFAULT 0,
    "appeals" INT NOT NULL DEFAULT 0,
    "guild_id" VARCHAR(32) NOT NULL PRIMARY KEY REFERENCES "guild" ("guild_id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "feature_settings";"""


MODELS_STATE = (
    "eJztml1z2jgUhv8Kw1U6k2aKE9rO3kFKWtoAO4m722mn4xH2wbiRJWrLmzAd/vtKwsa2/I"
    "GdkARa37ThSMeWHn29euFX26UWYP/kfeBgq/1X61ebIBf4H+mC41YbLRZxWAQYmmJZ095U"
    "mfrMQybjwRnCPvCQBb7pOQvmUMKjJMBYBKnJKzrEjkMBcX4GYDBqA5uDxwu+fedhh1hwB3"
    "70cXFjzBxQGipfbziyBbLUYMuFLDmfI+9C1hcvnRomxYFL1JzFks0p2STxlomoDQQ8xMBK"
    "dEa0Nex0FFq3mweYF8CmwVYcsGCGAswSna9IxKRE0HQI82V3XXRnYCA2m/OPp9pq3aW4w+"
    "taogf/9K7OP/Sujk61F6InlA/JeqDGYYkmi1byEYih9UMk5Jiq/L8G0aj+bmhGgRhnPKEe"
    "g6f26lUFoLxWIVFZJpDGCH9Qh4BlIJbl+I6zYI4L+SxTiQpQK8w8if7YU7weIGtC8DJcCS"
    "V09eFocK33Rn+Lnri+/xNLQj19IEo0GV0q0aPXykBsHtL6d6h/aImPra+T8UASpD6zPfnG"
    "uJ7+tS3ahAJGDUJvDWQlFm0UjcCsxOYzu0ksFBGYIvPmFnmWkSpJ7aAGprbvZ8e/H6ZefL"
    "oCjCTc7FCHO/CIWpf8Kfs5zqto7kbRaLwFIKrRImTpopiZD4zx95UgmxDQKf9nOzh5dF0n"
    "HrgFXzj4+0AvuY3MALFATN8dILlYP+swoYgJ5GquMqVcRJAtGyIeJ5Jzh79I2iRRbJE4Rn"
    "JyNlrn99E6Cw9mzl0dpnHG0+md9kl7V0i7FYh2C4F2VaGDEbEDvgjrEEzmPCFDIDuD2Kki"
    "GTvFirGTEYx84+F6wTDniBDA9VZ5Xu69uD79hv84yz2hKQLbBl+06n5oi/IbvLKMn5qA8P"
    "3Q5uX+wVhrXDOy+lpRCdlhiGSiHIoh7wwiZt7+qzo/+yYPigQiD3vodqOaUsKHd493Cth6"
    "Pvauz3vvBu1VyZWkptiMLmk5MjNxfysWmNFd8fmkpYl8yFWWQ8LyF28iQ5lBYkyUiRMO0L"
    "PKSlu85aXWOXtz9vb09dlbXkW2ZBN5U7KIh2N9i4xkyOPYa6rzVNJhmme7P1LEaqgtfxqG"
    "6WPZjKyAyoexWWAeHAhDrZqHW2Lhqgw9QH4eQx3uCvbEOONQGJY5s4MvesqUjVgdjXpfXq"
    "SM2cvJ+H1UPcH2/HLSV5gKz5pLD3dR1xVPJTau+B644slh3Q9n6jC37Yzs3yrlL6gHjk0+"
    "wfKxxfzz+b0PlPNbbku7k/6qp55zBcix3YuvAqHf37jNv6nbHNtJeV/pUIoBkW1GlJ+Dd8"
    "pTH2uF15101TVGfzK5TB1x/aEqIj6P+oOro45Ezis561Uf3cdU+7Qu1ERWAzTP2asLNJHV"
    "AG08vcP19HrgOeY87zwPS0qPcRTXeZbDu5aV17h4G27/gefXNE4SKYd5jdG6Vb4R5rWKvZ"
    "Nu5lthsTRqQAyrHybATqXfD3ZKfj/Yyf5+kL+RAcn59eDH68m4wJKPUxSQnwnv4DfLMdlx"
    "Czs++76fWEsoil6Xu1Gq8XScdjnEA/oPPZEferys/geekawa"
)
