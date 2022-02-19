from ast import parse
from email.mime import base
from pydoc import classname
import sys
import os
from typing import List, Final


class Error(Exception):
    pass


class InvalidArguments(Error, TypeError):
    pass


def main(args: List[str]):
    if len(args) != 1:
        raise InvalidArguments(
            "Usage: python3 generateAST.py <output directory>")

    outputDir: str = args[0]
    defineAst(outputDir, "Expr", [
        "Binary   : Expr left, Token operator, Expr right",
        "Grouping : Expr expression",
        "Literal  : Object value",
        "Unary    : Token operator, Expr right"
    ])


def defineAst(outputDir: str, basename: str, types: List[str]):
    path: Final[str] = outputDir + '/' + basename + '.java'
    buffer: str = "/* \n  This file was automatically generated using generateAST.py. \n  Do not manually edit this file! \n*/\n"
    buffer += "package com.andydudley.lox;"
    buffer += "\n"
    buffer += "import java.util.List;"
    buffer += "\n"
    buffer += "abstract class " + basename + " {"

    # Interfaces
    buffer += defineVisitor(basename, types)

    # Create subclasses for types
    for type in types:
        classname: str = type.split(":")[0].strip()
        fields: str = type.split(":")[1].strip()
        buffer += defineType(basename, classname, fields)

    # abstract methods
    buffer += "\n\n"
    buffer += "    abstract <R> R accept(Visitor<R> visitor);"
    buffer += "}"

    print(os.getcwd())
    with open(path, 'w+') as f:
        print(f.name)
        f.write(buffer)


def defineType(basename: str, classname: str, fields_string: str):
    fields = parseFields(fields_string)

    buffer = "\n"
    # Subclass
    buffer += f"    static class {classname} extends {basename} {{\n"
    # Constructor
    buffer += f"        {classname}({fields_string}) {{\n"
    for type, name in fields:
        buffer += f"            this.{name} = {name};\n"
    buffer += f"        }}\n"

    # Instance variables
    for type, name in fields:
        buffer += f"        final {type} {name};\n"

    # methods
    buffer += f"\n"
    buffer += f"\n        @Override"
    buffer += f"\n        <R> R accept(Visitor<R> visitor) {{"
    buffer += f"\n            return visitor.visit{classname}{basename}(this);"
    buffer += f"\n        }}\n"

    buffer += f"    }}\n"
    return buffer


def defineVisitor(basename: str, types: List[str]):
    buffer = "\n"
    buffer += "    interface Visitor<R> {"
    for type in types:
        typename: str = type.split(":")[0].strip()
        buffer += f"\n        R visit{typename}{basename}({typename} {basename.lower()});"
    buffer += "\n    }"
    return buffer


def parseFields(fields_string: str):
    fields: List[str] = []
    for field in fields_string.split(","):
        fields.append(field.split())

    return fields


if __name__ == '__main__':
    main(sys.argv[1:])
