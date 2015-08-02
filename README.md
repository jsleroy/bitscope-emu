# bitscope-emu

Emulate BitScope hardware.

## Usage

Create two linked virtual ports.

```
socat PTY,link=$HOME/COM1 PTY,link=$HOME/COM2
```

Connect BitScope software to COM1.
Connect emulator to COM2.
