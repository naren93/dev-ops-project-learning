Normal method via cli -
build -
g++ 001-gettingstarted.cpp -o 001-gettingstarted
execute - 
./001-gettingstarted

Build and run as task -
For C++ development on Mac, there are several ways to automate the compile and run process. Here are two recommended approaches:

1. **Using VS Code Tasks**

Create a `tasks.json` file in your .vscode folder:

````json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "build and run",
            "type": "shell",
            "command": "g++ '${file}' -o '${fileDirname}/${fileBasenameNoExtension}' && '${fileDirname}/${fileBasenameNoExtension}'",
            "group": {
                "kind": "build",
                "isDefault": true
            }
        }
    ]
}
````

2. **Using a Makefile**

Create a Makefile in your project directory:

````makefile
CC=g++
CFLAGS=-Wall

%: %.cpp
	$(CC) $(CFLAGS) $< -o $@
	./$@
````

**How to use:**

1. For VS Code Tasks:
   - Press `Cmd + Shift + B` to run the default build task
   - Or use the Terminal menu: Terminal → Run Build Task

2. For Makefile:
   - Just type `make filename` (without .cpp extension) in terminal

The VS Code tasks approach is recommended as it integrates well with the IDE and provides a smoother development experience.