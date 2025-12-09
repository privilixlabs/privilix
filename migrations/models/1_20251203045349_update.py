from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "guild_settings" ADD "appeal_channelid" VARCHAR(32);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "guild_settings" DROP COLUMN "appeal_channelid";"""


MODELS_STATE = (
    "eJztmW1P2zAQx79KlVdMYmgNdJv2rkCBbtBOkD1o0xSZ5JpmOHYWO4Nq6nef7SbNc9pAgX"
    "brG2jOPsf3c+z75/JH86gNmO2dhi62tXetPxpBHogf2YbdloZ8PzFLA0fXWPV05l2uGQ+Q"
    "xYVxhDADYbKBWYHrc5cSYSUhxtJILdHRJU5iCon7KwSTUwf4GALR8P2HMLvEhjtg8aV/Y4"
    "5cyE1U3d501QxUq8knvmo5GqPgRPWXN702LYpDj+R9/AkfUzJ3EjOTVgcIBIiDnQpGzjUK"
    "OjbN5i0MPAhhPmE7MdgwQiHmqeCXJGJRImm6hDMVrofuTAzE4WNxua9PZyElAc96yQg+dy"
    "+PzrqXO/v6CxkJFUsyW6hB1KKrpqkaAnE0G0RBTqiq/w2Ixv1XQzM2JDiTB+oxeOqvXi0B"
    "VPSqJKraJNIE4U/qErBNxIscjwUL7npQzjLjmANqR5578Y81xRsAsocET6KdUEPX6F/0ro"
    "zuxUcZicfYL6wIdY2ebNGVdZKz7rzOLcR8kNaXvnHWkpetb8NBTxGkjDuBumPSz/imyTmh"
    "kFOT0FsT2alNG1tjMFN5+IxuUhtFGq6RdXOLAtvMtGROUBNTh7Hi+h9GricfLgEjBbe41N"
    "EJfEHtczHKeq7zNH52Y2u83hIQ1WkVsmxTwowB5+J+NciGBAwq/iwGp1LXVWrABfiixV8X"
    "ep7u5eh5iCBHTUQOJ51LI63K4mkUC7K5mV6HbVr/d9K6H8DIvWvCNPF4utSu7WmrQtpZgm"
    "inEmgnn9MxIk4oNmETgmmfJ2QIZGUQ28uoo3a1OGoXtJE4eERqNK0xIgRws11e5nsvrk9/"
    "4D/Odk+lz9BxgMlZ3Q9tlf8Wr2oTWRMQvh/aMt//GGsDRV2UkjmVUFyGWCSqpeiLYBCxys"
    "7ffJFj3eRBlUAU5gDdzlVTRviI8ERQwGfPY/fqqHvc06Y16ruh2IzfR0pkZupVpVpgxq9F"
    "zyctLcSgVFn2CS/fvCmP3BMk1yT34EQL9Kyy0pF3eam3D94cvN1/ffBWdFEzmVve1Gzi/s"
    "BYICM5CgT2huo847SZdaLVpxS5GxrLny3DbFq24kLA0snYqigdbAhDfblyZU21Ms8wAMTK"
    "GBpwV3EmJh6bwrCuCNn7amTqjzGrnYvu1xeZGuT5cHAad0+xPTofHuaYyvKskB6e37QAnH"
    "HcFoDXoACcXtb1qExt5rFdkP0LpfwJDcB1yAeYPLaYf7567wPl/IK3pdVJ/y4ErjXWSpR/"
    "1FIr/FHS51lkfyPFvxX7c26/IWAN9VXKZTNPO72zTOFY9KqWWJ1C8VhujSYi1S/L/xsCsL"
    "3UF/V2zRf1dvGLurgjB1LyPf391XBQ8eaeuORAfiIiwO+2a/HdFnYZ/7GeWGsoyqjrRWte"
    "n+bEkBzg8KHFuIeml+lfwgjDdQ=="
)
