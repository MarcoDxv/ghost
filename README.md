# ~ Ghost ~
Dis is a programmin language uwu... <br/>
You can only use it on linux.

## Installation
I don't know how to install it :( <br/> 
To use it I think you need [nasm](https://www.nasm.us/) an [ld](https://linux.die.net/man/1/ld)

### Hello, World
```
13 "Hello, World" 1 1 syscall3.
0 60 syscall1.
```
##### or
```
import "std.ghost"

13 "Hello, World" display.
0 exit.
```
##### and compile with...
```
python3 ./ghost.py hello.ght -r hello --debug
./hello
```

### What I want to Implement
I want my language to be: <br/>
 [-] Turing-Complete ( [turing-machine](https://en.wikipedia.org/wiki/Turing_machine) and  [rule110](https://en.wikipedia.org/wiki/Rule_110) ) <br/>
 [-] Crossplatform ( can work on [Linux](https://en.wikipedia.org/wiki/Linux), [MacOS](https://en.wikipedia.org/wiki/MacOS) an [Windows](https://en.wikipedia.org/wiki/Microsoft_Windows) ) <br/>
 [-] Optimized <br/>
 [-] [Self-Hosted](https://en.wikipedia.org/wiki/Self-hosting_(compilers)) <br/>

## License
MIT
