
import sys

# ---------- LANGUAGE MAPPING ----------
# Based on: "Meet the Microshit Binbows 11"
TOKENS = {
    "Meet": ">",
    "the": "<",
    "Microshit": "+",
    "Binbows": "-",
    "11": ".",
    "MeetMeet": ",",
    "thethe": "[",
    "MicroshitMicroshit": "]",
}

# ---------- TRANSLATION STEP ----------
def translate_to_bf(source: str) -> str:
    bf = []
    words = source.strip().split()

    for w in words:
        if w not in TOKENS:
            raise ValueError(f"Unknown token: {w}")
        bf.append(TOKENS[w])

    return "".join(bf)


# ---------- BRAINFUCK INTERPRETER ----------
def run_brainfuck(code: str):
    tape = [0] * 30000
    ptr = 0
    pc = 0
    output = ""
    loop_stack = []

    while pc < len(code):
        cmd = code[pc]

        if cmd == ">":
            ptr += 1

        elif cmd == "<":
            ptr -= 1

        elif cmd == "+":
            tape[ptr] = (tape[ptr] + 1) % 256

        elif cmd == "-":
            tape[ptr] = (tape[ptr] - 1) % 256

        elif cmd == ".":
            output += chr(tape[ptr])

        elif cmd == ",":
            tape[ptr] = ord(input("Input a character: ")[0])

        elif cmd == "[":
            if tape[ptr] == 0:
                depth = 1
                while depth:
                    pc += 1
                    if code[pc] == "[":
                        depth += 1
                    elif code[pc] == "]":
                        depth -= 1
            else:
                loop_stack.append(pc)

        elif cmd == "]":
            if tape[ptr] != 0:
                pc = loop_stack[-1]
            else:
                loop_stack.pop()

        pc += 1

    return output


# ---------- COMPILER MAIN ----------
def compile_file(input_path, output_bf_path=None, run=False):
    with open(input_path, "r") as f:
        src = f.read()

    bf_code = translate_to_bf(src)

    if output_bf_path:
        with open(output_bf_path, "w") as f:
            f.write(bf_code)
        print(f"✔ Program saved to: {output_bf_path}")

    if run:
        print("Program output:")
        print(run_brainfuck(bf_code))


# ---------- COMMAND LINE USAGE ----------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  compiler.py <input.txt>                  (translate only)")
        print("  compiler.py <input.txt> <output.bf>      (write BF file)")
        print("  compiler.py <input.txt> --run            (execute)")
        sys.exit(1)

    input_path = sys.argv[1]

    if len(sys.argv) == 2:
        # translate only, print BF to stdout
        with open(input_path, "r") as f:
            print(translate_to_bf(f.read()))
    elif len(sys.argv) == 3 and sys.argv[2] == "--run":
        compile_file(input_path, run=True)
    else:
        output_path = sys.argv[2]
        compile_file(input_path, output_path, run=False)
