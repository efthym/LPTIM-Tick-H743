# LPTIM-Tick-H743

I am using platform IO for development, so the directory structure is somewhat modified: I removed the Drivers directory (platform IO downloads these in its own filespace) and the Core/Startup directory (the startup file is again in platform IO filespace).
CMSIS_OS V2 is used instead of V1 of the original.

I use LPTIM2 for the FreeRTOS tick counter (in place of LPTIM1 in the original).
The system is clocked at 16MHz from the 64MHz HSI prescaled by 4.
LPTIM2 is clocked by the 32.768kHz LSE.

For the timing test, I use LPTIM3 (in place of LPTIM2 in the original) clocked by LSE and USART3 which connects to STlink (Virtual COM).

TODO: measure the current on the board.

*FreeRTOS Tick/Tickless via LPTIM*

Use LPTIM for the FreeRTOS tick instead of the SysTick Timer for ultra-low-power applications.

- No drift or slippage in kernel time
- Use STOP modes even while FreeRTOS timers are running or delays are underway
- For any STM32 with LPTIM (STM32L, STM32F, STM32G, STM32H, STM32U, STM32W)

This repository demonstrates integration and testing of the [lptimTick.c gist](https://gist.github.com/jefftenney/02b313fe649a14b4c75237f925872d72) on [Nucleo-L476RG](https://www.st.com/en/evaluation-tools/nucleo-l476rg.html) (STM32L476).  The project uses STM32CubeIDE and its integrated code-generation tool (STM32CubeMX).  However, lptimTick.c is compatible with any toolchain supported by FreeRTOS.

A separate repository, [LPTIM-Tick-U5](https://github.com/jefftenney/LPTIM-Tick-U5), is adapted to the STM32U family.

For a thorough evaluation, this project can be built without tickless idle, with the default tickless idle, or with the custom tickless idle provided by lptimTick.c.  See branches for additional evaluation options.

---

## Nucleo-L476RG Demo

Press the blue button to cycle between tests:
1. Maintain kernel time only.  LED blinks every 5 seconds.
2. Validate tick timing.  LED blinks every 2 seconds.
3. Stress test tick timing.  LED blinks every second.

Tests 2 and 3 display live test results to a serial terminal.  Connect to the STLink Virtual COM Port at 115200 8N1.  Additionally, the LED blinks twice (instead of just once) in case of test failure.

## Test Results
*Current readings shown are averages, *not* including the LED*

__With lptimTick.c (`configUSE_TICKLESS_IDLE 2`)__

- Test 1: 2μA, no drift
- Test 2: 55μA, no drift
- Test 3: 110μA, no drift

__Default tickless idle (`configUSE_TICKLESS_IDLE 1`)__

- Test 1: 3.70mA, trivial drift
- Test 2: 3.72mA, trivial drift
- Test 3: 3.74mA, trivial drift (with kernel v10.5.1 or newer)

__Tickless disabled (`configUSE_TICKLESS_IDLE 0`)__

- Test 1: 9.86mA, no drift
- Test 2: 9.86mA, no drift
- Test 3: 9.86mA, no drift

---

## Integrating lptimTick.c into your project

1. Add [lptimTick.c](https://github.com/jefftenney/LPTIM-Tick/blob/main/Core/Src/lptimTick.c) to your project folder, configuration, and/or makefile.
1. In FreeRTOSConfig.h, define `configUSE_TICKLESS_IDLE` to `2`, and eliminate the preprocessor definition for `xPortSysTickHandler`.  If using LSI instead of LSE, define `configTICK_USES_LSI` and `configLPTIM_REF_CLOCK_HZ` (typically `32000` or `37000`), too.
1. Update the [#include](https://github.com/jefftenney/LPTIM-Tick/blob/5ca1c2ee5878479d2c5c1bac3c8f6a6ae2dea7eb/Core/Src/lptimTick.c#L32) for your MCU.
1. Update the LPTIM [instance selection](https://github.com/jefftenney/LPTIM-Tick/blob/5ca1c2ee5878479d2c5c1bac3c8f6a6ae2dea7eb/Core/Src/lptimTick.c#L255-L257).  (For STM32WL users, [here](https://github.com/jefftenney/LPTIM-Tick/blob/5ca1c2ee5878479d2c5c1bac3c8f6a6ae2dea7eb/Core/Src/lptimTick.c#L289) too.)  LPTIM1 is the default.
1. Update the [initialization code](https://github.com/jefftenney/LPTIM-Tick/blob/5ca1c2ee5878479d2c5c1bac3c8f6a6ae2dea7eb/Core/Src/lptimTick.c#L275-L279) that is specific to both the MCU family and the LPTIM instance.

