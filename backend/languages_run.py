FILENAME_RUN = "Main"
INPUT_FILENAME = "input.txt"

commands = {
    ".py": {
        "image": "python:3",
        "run": ["/bin/bash", "-c",
                f"python {FILENAME_RUN}.py < {INPUT_FILENAME}"],
    },

    ".java": {
        "image": "openjdk:11",
        "run": [
            "/bin/bash", "-c",
            f"javac {FILENAME_RUN}.java && java {FILENAME_RUN} < {INPUT_FILENAME}"
        ]
    },

    ".rb": {
        "image": "ruby:3",
        "run": [
            "/bin/bash", "-c",
            f"ruby {FILENAME_RUN}.rb"
        ]
    },

    ".cpp": {
        "image": "gcc",
        "run": [
            "/bin/bash", "-c",
            f"g++ -o {FILENAME_RUN} {FILENAME_RUN}.cpp && ./{FILENAME_RUN} < {INPUT_FILENAME}"
        ]
    }
}
