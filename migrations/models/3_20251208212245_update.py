from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "mod_logs" ADD "resolved" INT NOT NULL DEFAULT 0;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "mod_logs" DROP COLUMN "resolved";"""


MODELS_STATE = (
    "eJztmltz2jgUx78Kw1M6k80UJ7SdfYOUtGwDdBL3Mu10PMI+GG9kidpyE6bDd19J2NiWL9"
    "gJSaDrlwSOdGTpd3T565jfbZdagP2Td4GDrfbfrd9tglzgH9IFx602WixiszAwNMWypr2p"
    "MvWZh0zGjTOEfeAmC3zTcxbMoYRbSYCxMFKTV3SIHZsC4vwMwGDUBjYHjxd8/8HNDrHgDv"
    "zo6+LGmDmgdFQ+3nBkD2SpwZYLWXI+R96FrC8eOjVMigOXqD6LJZtTsnHiPRNWGwh4iIGV"
    "GIzoazjoyLTuNzcwL4BNh63YYMEMBZglBl+RiEmJoOkQ5svhuujOwEBsNudfT7XVekjxgN"
    "e1xAg+967O3/eujk61F2IklIdkHahxWKLJopVsAjG0bkRCjqnK/zWIRvV3QzMyxDjjCfUY"
    "PLWXLysA5bUKicoygTRG+C91CFgGYlmObzkL5riQzzLlqAC1Qs+T6MOe4vUAWROCl+FKKK"
    "GrD0eDa703+ihG4vr+TywJ9fSBKNGkdalYj14pgdg00voy1N+3xNfWt8l4IAlSn9mefGJc"
    "T//WFn1CAaMGobcGshKLNrJGYFZi85ndJBaKMEyReXOLPMtIlaR2UANT2/ez8e+Hrhcfrg"
    "AjCTcb6nAHHlHrkreyn3FeRXM3skbxFoCoRouQpYtiZj4wxp9XgmxCQKf8z3Zw8ui6TjS4"
    "BV8Y/H2gl9xGZoBYIKbvDpBcrNs6TChiArmaq0wpFxFky46I5oRzbviLpE0SxRaJYyQnZ6"
    "N1/hyts/Bg5tzVYRp7PJ3eaZ+0d4W0W4FotxBoVxU6GBE74IuwDsGkzxMyBLIziJ0qkrFT"
    "rBg7GcHINx6uFwxzjggBXG+V5/nei+vTb/iPs9wTmiKwbfBFr+6Htsi/wSvL+KkJCN8PbZ"
    "7v/xhrjWtGVl8rKiEbhkgmylAM+WAQMfP2XzXzs2/yoEggcrOHbjeqKSV8+PD4oICt52Pv"
    "+rz3dtBelVxJaorN6JKWIzMT97digRndFZ9PWprIh1xlOSQsf/EmPJQZJGKiTJwwQM8qK2"
    "3xlL+0ztnrszenr87e8CqyJxvL65JFPBzrW2QkQx7HXlOdp5wOM3m2+yNFrIba8qdhmD6W"
    "zSgVUPkwNguSBwfCUKuWwy1J4aoMPUB+HkMd7gr2xNjjUBiWZWYHX/VUUjZidTTqfX2RSs"
    "xeTsbvouoJtueXk77CVOSsufRwF3Wz4inHJiu+B1nx9FLxKf4FOZt2n1IMiBStl9hNiemU"
    "+z1WGOvqquprpj+ZXKZC1h+qi+LTqD+4OurIWPFKzlqURvpi35J9h3kSZm5SW29HF9QDxy"
    "YfYPnY96PnS6EfP+yGtOUCurvblPqaIudWlfMmo/h2Fb5CaRL4f2gCP87Q5b0lKzt/FM/m"
    "CMrLSNeFmvBqgOYlS+sCTXg1QJs06eGmSXvgOeY87zwPS0qPcRTXeZbDu1Z2tEmMbrj9As"
    "+vmYtKuBzmNUbrVnnJzmsVp6O6mRftYmnUgBhWP0yAnUo/yeyU/CSzk/1JJn8iA5Lzg8x/"
    "rifjgrccsYsC8hPhA/xuOSY7bmHHZz/2E2sJRTHq8gSfmss7TieORAP9h57IDz1eVv8BOh"
    "0YKg=="
)
