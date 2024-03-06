from constants import FILENAME_RUN, INPUT_TEST_FILENAME


commands_standard = {
    "python.3": {
        "image": "python:3",
        "run": [
            "/bin/bash", "-c",
            f"python3 {FILENAME_RUN}.py < {INPUT_TEST_FILENAME}"
        ],
    },

    ".java": {
        "image": "openjdk:11",
        "run": [
            "/bin/bash", "-c",
            f"javac {FILENAME_RUN}.java < {INPUT_TEST_FILENAME}"
        ]
    },

    ".rb": {
        "image": "ruby:3",
        "run": [
            "/bin/bash", "-c",
            f"ruby {FILENAME_RUN}.rb < {INPUT_TEST_FILENAME}"
        ]
    },

    ".cpp": {
        "image": "gcc",
        "run": [
            "/bin/bash", "-c",
            f"g++ -std=c++17 -o {FILENAME_RUN} {FILENAME_RUN}.cpp < {INPUT_TEST_FILENAME}"
        ]
    }
}

commands_standard[".py"] = commands_standard["python.3"]
