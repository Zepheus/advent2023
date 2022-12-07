from typing import List, Optional, Dict
from dataclasses import dataclass

INPUT = "example"
PROMPT = "$"
INDENT_SPACE = 2
THRESHOLD = 100000

@dataclass
class Command:
    command: str
    param: Optional[str]
    output: List[str]  # Can be empty

@dataclass
class File:
    parent: "Directory"
    name: str
    size: int


@dataclass
class Directory:
    parent: Optional["Directory"]
    name: str
    child_directories: Dict[str, "Directory"]
    child_files: Dict[str, File]

    def size(self) -> int:
        total = 0
        for child in self.child_directories.values():
            total += child.size()
        
        for child in self.child_files.values():
            total += child.size

        return total

    def solution(self, threshold) -> int:
        total = 0
        if self.size() < threshold:
            total += self.size()
        
        for child in self.child_directories.values():
            total += child.solution(threshold)
        
        return total


def read_file(path):
    with open(path, 'r') as f:
        return f.readlines()

def parse(lines):
    commands = []
    current = None
    for line in lines:
        if line.startswith(PROMPT):
            if current != None:
                commands.append(current)
            
            splitted = line.split()

            current = Command(
                command=splitted[1], 
                param=None if len(splitted) <= 2 else splitted[2],
                output=[]
            )
        elif current is not None:
            current.output.append(line.rstrip())
        else:
            raise Exception("Output detected for non-command")

    # flush the last command as there is no more prompt
    if current != None:
        commands.append(current)
    return commands

def get_directory_through_path(root: Directory, path: str) -> Directory:
    splitted = path.split("/")
    current = root
    for path in splitted[1:]:
        current = root.child_directories.get(path)
    return current


def execute(commands: List[Command]):
    root = Directory(parent=None, name="/", child_directories={}, child_files={})
    cwd = root
    for command in commands:
        if command.command == "cd":
            if command.param == "/":
                cwd = root
            elif command.param == "..":
                cwd = cwd.parent
            else:
                # This is a directory name
                target_dir = cwd.child_directories.get(command.param)
                if target_dir is None:
                    target_dir =  Directory(
                            parent=cwd,
                            name=command.param,
                            child_directories={},
                            child_files={}
                        )
                    cwd.child_directories.update({
                        command.param: target_dir
                    })
                cwd = target_dir
        elif command.command == "ls":
            for line in command.output:
                splitted = line.split()
                if splitted[0] == "dir" and splitted[1] not in cwd.child_directories:
                    cwd.child_directories.update({
                        splitted[1]: Directory(
                            parent=cwd,
                            name=splitted[1],
                            child_directories={},
                            child_files={}
                        )
                    })
                else:
                    # This is a file
                    file_size = int(splitted[0])
                    filename = splitted[1]
                    if filename not in cwd.child_files:
                        cwd.child_files.update({
                            filename: File(parent=cwd, name=filename, size=file_size)
                        })
        else:
            raise Exception(f"Invalid command: {command.command}")
    return root

def print_directory(directory: Directory, indent: int = 0) -> None:
    padding = ' ' * (indent * INDENT_SPACE)
    print(f"{padding}- {directory.name} (dir)")
    for child_dir in directory.child_directories.values():
        print_directory(child_dir, indent=indent + 1)
    
    padding = ' ' * ((indent + 1) * INDENT_SPACE)
    for file in directory.child_files.values():
        print(f"{padding}- {file.name} (file, size={file.size})")


def main():
    inputs = read_file(INPUT)
    commands = parse(inputs)
    root = execute(commands=commands)
    #print_directory(root)
    result = root.solution(threshold=THRESHOLD)
    print(result)

if __name__ == "__main__":
    main()