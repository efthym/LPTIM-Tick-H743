Import("env")

#
# Dump build environment (for debug)
# print(env.Dump())

# Replace assembler with C compiler as is done in ~/.platformio/platforms/ststm32/builder/frameworks/stm32cube.py
env.Replace(
    AS="$CC",
    ASCOM="$ASPPCOM"
)

# Provide flags to linker as they are not passed on from the compiler flags.
env.Append(
  LINKFLAGS=[
      "-mfloat-abi=hard",
      "-mfpu=fpv5-d16",
      "-lnosys"
  ]
)
